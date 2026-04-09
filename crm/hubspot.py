"""
HubSpot API Client for Sales Leadership Board.
Pulls calls, emails, meetings per rep per day.
"""

import logging
import requests
from datetime import datetime, timedelta

log = logging.getLogger("slb.hubspot")

HUBSPOT_BASE = "https://api.hubapi.com"


class HubSpotClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get(self, endpoint: str, params: dict = None) -> dict:
        r = requests.get(f"{HUBSPOT_BASE}/{endpoint}", headers=self._headers(), params=params)
        r.raise_for_status()
        return r.json()

    def _paginate(self, endpoint: str, params: dict = None) -> list:
        results = []
        after = None
        while True:
            p = dict(params or {})
            p["limit"] = 100
            if after:
                p["after"] = after
            data = self._get(endpoint, p)
            results.extend(data.get("results", []))
            paging = data.get("paging", {}).get("next")
            if not paging:
                break
            after = paging.get("after")
        return results

    def get_owners(self) -> dict:
        """Map HubSpot owner IDs to names."""
        data = self._get("crm/v3/owners")
        return {
            str(o["id"]): f"{o.get('firstName', '')} {o.get('lastName', '')}".strip()
            for o in data.get("results", [])
        }

    def collect_daily(self, date_str: str = None, rep_names: list[str] = None) -> dict:
        """
        Pull all engagement data for a single day from HubSpot.
        Returns dict keyed by rep name with metrics.
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        dt = datetime.strptime(date_str, "%Y-%m-%d")
        ts_from = int(dt.timestamp() * 1000)
        ts_to = int((dt + timedelta(days=1)).timestamp() * 1000)

        owners = self.get_owners()

        stats = {}
        for owner_id, name in owners.items():
            if rep_names and not any(rn.lower() in name.lower() for rn in rep_names):
                continue
            stats[name] = {
                "owner_id": owner_id,
                "calls": 0,
                "calls_connected": 0,
                "call_durations": [],
                "connected_durations": [],
                "emails_sent": 0,
                "emails_received": 0,
                "meetings_booked": 0,
                "call_details": [],
            }

        # --- Calls ---
        calls = self._paginate("crm/v3/objects/calls", {
            "properties": "hs_call_direction,hs_call_duration,hs_call_disposition,"
                          "hs_call_recording_url,hs_timestamp,hubspot_owner_id",
            "filterGroups": [{
                "filters": [{
                    "propertyName": "hs_timestamp",
                    "operator": "BETWEEN",
                    "highValue": str(ts_to),
                    "value": str(ts_from),
                }]
            }],
        })

        for c in calls:
            props = c.get("properties", {})
            owner_id = props.get("hubspot_owner_id")
            name = owners.get(str(owner_id))
            if not name or name not in stats:
                continue

            direction = (props.get("hs_call_direction") or "").upper()
            if direction != "OUTBOUND":
                continue

            dur = int(props.get("hs_call_duration") or 0)
            s = stats[name]
            s["calls"] += 1
            s["call_durations"].append(dur)

            if dur > 30:
                s["calls_connected"] += 1
                s["connected_durations"].append(dur)

            s["call_details"].append({
                "duration": dur,
                "recording_url": props.get("hs_call_recording_url"),
                "disposition": props.get("hs_call_disposition"),
                "created_at": props.get("hs_timestamp"),
            })

        # --- Emails ---
        emails = self._paginate("crm/v3/objects/emails", {
            "properties": "hs_email_direction,hs_timestamp,hubspot_owner_id",
            "filterGroups": [{
                "filters": [{
                    "propertyName": "hs_timestamp",
                    "operator": "BETWEEN",
                    "highValue": str(ts_to),
                    "value": str(ts_from),
                }]
            }],
        })

        for e in emails:
            props = e.get("properties", {})
            owner_id = props.get("hubspot_owner_id")
            name = owners.get(str(owner_id))
            if not name or name not in stats:
                continue
            direction = (props.get("hs_email_direction") or "").upper()
            if direction == "EMAIL":
                stats[name]["emails_sent"] += 1
            else:
                stats[name]["emails_received"] += 1

        # --- Meetings ---
        meetings = self._paginate("crm/v3/objects/meetings", {
            "properties": "hs_timestamp,hubspot_owner_id",
            "filterGroups": [{
                "filters": [{
                    "propertyName": "hs_timestamp",
                    "operator": "BETWEEN",
                    "highValue": str(ts_to),
                    "value": str(ts_from),
                }]
            }],
        })

        for m in meetings:
            props = m.get("properties", {})
            owner_id = props.get("hubspot_owner_id")
            name = owners.get(str(owner_id))
            if not name or name not in stats:
                continue
            stats[name]["meetings_booked"] += 1

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
            del s["owner_id"]

        return stats
