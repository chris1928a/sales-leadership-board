#!/usr/bin/env python3
"""
Sales Leadership Board - HubSpot Edition
Daily run: Mo-Fr 18:00 CET

Usage:
    python main_hubspot.py               # Full run
    python main_hubspot.py --dry-run     # Print only, no Sheets/Telegram
    python main_hubspot.py --date 2026-04-09  # Specific date
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

from crm.hubspot import HubSpotClient
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

    date_str = None
    for i, arg in enumerate(sys.argv):
        if arg == "--date" and i + 1 < len(sys.argv):
            date_str = sys.argv[i + 1]

    # --- Step 1: Collect daily data from HubSpot ---
    client = HubSpotClient(os.getenv("HUBSPOT_API_KEY"))
    daily_data = client.collect_daily(date_str=date_str, rep_names=rep_names)

    log.info(f"Collected data for {len(daily_data)} reps")

    # --- Step 2: Run Gap-Detection Matrix per rep ---
    for rep_name, metrics in daily_data.items():
        rep_cfg = config["reps"].get(rep_name, {})

        if rep_cfg.get("ramping_level") == "auto" and rep_cfg.get("start_date"):
            phase = get_ramping_phase(rep_cfg["start_date"])
        else:
            phase = rep_cfg.get("ramping_level", "phase_4_fully_ramped")

        targets = config["targets"].get(phase, config["targets"]["phase_4_fully_ramped"])
        diagnosis = diagnose(metrics, targets=targets, phase=phase)

        log.info(
            f"{rep_name} [{phase}]: {diagnosis['main_diagnosis']} "
            f"(Activity: {diagnosis['activity_status']}, Outcomes: {diagnosis['outcome_status']})"
        )
        log.info(f"  Coaching focus: {diagnosis['coaching_focus']}")
        for sub in diagnosis.get("sub_diagnoses", []):
            log.info(f"  Sub: {sub}")

    # --- Step 3: Check ramping checkpoints ---
    alerts = check_checkpoints(config["reps"])
    for alert in alerts:
        log.warning(alert)

    # --- Step 4: Output ---
    if not DRY_RUN:
        log.info("Writing to Google Sheets...")
        log.info("Sending Telegram briefing...")
    else:
        log.info("[DRY RUN] Skipping Sheets + Telegram")

    log.info("Done.")


if __name__ == "__main__":
    main()
