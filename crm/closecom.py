"""
Close.com API Client for Sales Leadership Board.
Pulls calls, emails, meetings per rep per day.
"""

import os
import time
import base64
import logging
import requests
from datetime import datetime, timedelta

log = logging.getLogger("slb.closecom")

CLOSE_BASE = "https://api.close.com/api/v1"

# Machine/IVR patterns to filter out non-human calls
_AUTO_PATTERNS = [
    "automated", "ivr", "press 1", "voicemail", "mailbox",
    "anrufbeantworter", "bandansage", "kein anschluss",
    "rufnummer nicht vergeben", "power dialer", "predictive dialer",
]


class CloseComClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._req_count = 0

    def _headers(self):
        token = base64.b64encode(f"{self.api_key}:".encode()).decode()
        return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    def _get(self, endpoint: str, params: dict = None) -> dict:
        self._req_count += 1
        if self._req_count % 80 == 0:
            time.sleep(15)  # Rate limit: pause every 80 requests
        r = requests.get(f"{CLOSE_BASE}/{endpoint}", headers=self._headers(), params=params)
        r.raise_for_status()
        return r.json()

    def _get_with_retry(self, endpoint: str, params: dict = None, retries: int = 3) -> dict:
        for attempt in range(retries):
            try:
                return self._get(endpoint, params)
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise
                wait = 2 ** attempt
                log.warning(f"API call failed (attempt {attempt+1}): {e}. Retry in {wait}s")
                time.sleep(wait)

    def _paginate(self, endpoint: str, date_from: str, date_to: str) -> list:
        results, skip = [], 0
        while True:
            params = {
                "date_created__gte": date_from,
                "date_created__lt": date_to,
                "_skip": skip,
                "_limit": 100,
            }
            data = self._get_with_retry(f"{endpoint}/", params)
            results.extend(data["data"])
            if not data.get("has_more", False):
                break
            skip += 100
        return results

    def get_tracked_users(self, rep_names: list[str]) -> dict:
        """Map Close.com user IDs to rep names."""
        data = self._get_with_retry("user/")
        tracked = {}
        for u in data["data"]:
            full_name = f"{u['first_name']} {u['last_name']}"
            for rn in rep_names:
                if rn.lower() in full_name.lower() or full_name.lower() in rn.lower():
                    tracked[u["id"]] = full_name
                    break
        return tracked

    def get_lead_name(self, lead_id: str) -> str:
        try:
            return self._get_with_retry(f"lead/{lead_id}/").get("display_name", "Unknown")
        except Exception:
            return "Unknown"

    @staticmethod
    def _is_machine_call(call: dict) -> bool:
        combined = " ".join([
            (call.get("note") or "").lower(),
            (call.get("disposition") or "").lower(),
            (call.get("source") or "").lower(),
        ])
        return any(p in combined for p in _AUTO_PATTERNS)

    def collect_daily(self, date_str: str = None, rep_names: list[str] = None) -> dict:
        """
        Pull all call, email, meeting data for a single day.
        Returns dict keyed by rep name with metrics.
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

        if not rep_names:
            rep_names = list(self.get_tracked_users([]).values())

        users = self.get_tracked_users(rep_names)
        log.info(f"Collecting {date_str} for reps: {list(users.values())}")

        calls = self._paginate("activity/call", date_str, date_to)
        emails = self._paginate("activity/email", date_str, date_to)
        meetings = self._paginate("activity/meeting", date_str, date_to)

        stats = {}
        for uid, name in users.items():
            stats[name] = {
                "calls": 0,
                "calls_connected": 0,
                "call_durations": [],
                "connected_durations": [],
                "emails_sent": 0,
                "emails_received": 0,
                "meetings_booked": 0,
                "call_details": [],
            }

        # Process calls
        for c in calls:
            uid = c.get("user_id") or c.get("created_by")
            if uid not in users:
                continue
            if c.get("direction") not in ("outbound", "outgoing"):
                continue
            if self._is_machine_call(c):
                continue

            name = users[uid]
            s = stats[name]
            dur = c.get("duration") or 0
            s["calls"] += 1
            s["call_durations"].append(dur)

            if dur > 30:  # Connected = duration > 30 seconds
                s["calls_connected"] += 1
                s["connected_durations"].append(dur)

            s["call_details"].append({
                "duration": dur,
                "lead_id": c.get("lead_id"),
                "note": c.get("note", ""),
                "recording_url": c.get("recording_url"),
                "created_at": c.get("date_created"),
            })

        # Process emails
        for e in emails:
            uid = e.get("user_id") or e.get("created_by")
            if uid not in users:
                continue
            name = users[uid]
            if e.get("direction") == "outgoing":
                stats[name]["emails_sent"] += 1
            else:
                stats[name]["emails_received"] += 1

        # Process meetings
        for m in meetings:
            uid = m.get("user_id") or m.get("created_by")
            if uid not in users:
                continue
            stats[users[uid]]["meetings_booked"] += 1

        # Calculate derived metrics
        for name, s in stats.items():
            s["connect_rate"] = (
                round(s["calls_connected"] / s["calls"] * 100, 1)
                if s["calls"] > 0 else 0
            )
            s["avg_call_duration"] = (
                round(sum(s["call_durations"]) / len(s["call_durations"]))
                if s["call_durations"] else 0
            )
            s["avg_connected_duration"] = (
                round(sum(s["connected_durations"]) / len(s["connected_durations"]))
                if s["connected_durations"] else 0
            )

        return stats
