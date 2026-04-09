#!/usr/bin/env python3
"""
Sales Leadership Board - Close.com Edition
Daily run: Mo-Fr 18:00 CET

Usage:
    python main_closecom.py              # Full run
    python main_closecom.py --dry-run    # Print only, no Sheets/Telegram
    python main_closecom.py --date 2026-04-09  # Specific date
"""

import os
import sys
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("slb")

from crm.closecom import CloseComClient
from scoring.gap_matrix import diagnose, diagnose_weakest_dimension
from scoring.call_scorer import score_call
from training.ramping import get_ramping_phase, check_checkpoints
from training.objection_library import match_objection

DRY_RUN = "--dry-run" in sys.argv


def load_config():
    with open("config/targets.json") as f:
        return json.load(f)


def main():
    config = load_config()
    rep_names = list(config["reps"].keys())

    # Parse optional date argument
    date_str = None
    for i, arg in enumerate(sys.argv):
        if arg == "--date" and i + 1 < len(sys.argv):
            date_str = sys.argv[i + 1]

    # --- Step 1: Collect daily data from Close.com ---
    client = CloseComClient(os.getenv("CLOSE_API_KEY"))
    daily_data = client.collect_daily(date_str=date_str, rep_names=rep_names)

    log.info(f"Collected data for {len(daily_data)} reps")

    # --- Step 2: Run Gap-Detection Matrix per rep ---
    for rep_name, metrics in daily_data.items():
        rep_cfg = config["reps"].get(rep_name, {})

        # Determine ramping phase
        if rep_cfg.get("ramping_level") == "auto" and rep_cfg.get("start_date"):
            phase = get_ramping_phase(rep_cfg["start_date"])
        else:
            phase = rep_cfg.get("ramping_level", "phase_4_fully_ramped")

        # Get phase-specific targets
        targets = config["targets"].get(phase, config["targets"]["phase_4_fully_ramped"])

        # Run diagnosis
        diagnosis = diagnose(metrics, targets=targets, phase=phase)

        log.info(
            f"{rep_name} [{phase}]: {diagnosis['main_diagnosis']} "
            f"(Activity: {diagnosis['activity_status']}, Outcomes: {diagnosis['outcome_status']})"
        )
        log.info(f"  Coaching focus: {diagnosis['coaching_focus']}")
        for sub in diagnosis.get("sub_diagnoses", []):
            log.info(f"  Sub: {sub}")

        # --- Step 3: Score individual calls (if recordings available) ---
        for call in metrics.get("call_details", []):
            if call.get("recording_url"):
                # In production: transcribe via Deepgram, then score via Claude
                # score = score_call(transcript, rep_name, company, duration)
                log.info(f"  Call to score: {call['duration']}s, has recording")

    # --- Step 4: Check ramping checkpoints ---
    alerts = check_checkpoints(config["reps"])
    for alert in alerts:
        log.warning(alert)

    # --- Step 5: Write to Google Sheets + send Telegram ---
    if not DRY_RUN:
        log.info("Writing to Google Sheets...")
        # In production: write_dashboard(daily_data, os.getenv("GOOGLE_SHEET_ID"))
        log.info("Sending Telegram briefing...")
        # In production: send_telegram(daily_data, alerts)
    else:
        log.info("[DRY RUN] Skipping Sheets + Telegram")

    log.info("Done.")


if __name__ == "__main__":
    main()
