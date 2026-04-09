"""
4-Phase Ramping System.
Auto-calculates rep phase based on start date.
Provides phase-appropriate targets and checkpoint alerts.
"""

from datetime import date, datetime


PHASE_MAP = {
    "phase_1_month_1": {"label": "Phase 1 (Month 1)", "day_range": (0, 30)},
    "phase_2_month_2": {"label": "Phase 2 (Month 2)", "day_range": (31, 60)},
    "phase_3_month_3": {"label": "Phase 3 (Month 3)", "day_range": (61, 90)},
    "phase_4_fully_ramped": {"label": "Phase 4 (Fully Ramped)", "day_range": (91, 9999)},
}

CHECKPOINTS = [30, 60, 90]


def get_ramping_phase(start_date_str: str) -> str:
    """Return the ramping phase key based on days since start."""
    start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    days = (date.today() - start).days

    if days <= 30:
        return "phase_1_month_1"
    elif days <= 60:
        return "phase_2_month_2"
    elif days <= 90:
        return "phase_3_month_3"
    return "phase_4_fully_ramped"


def get_days_since_start(start_date_str: str) -> int:
    start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    return (date.today() - start).days


def check_checkpoints(reps: dict) -> list[str]:
    """
    Check if any rep hits a ramping checkpoint (day 30, 60, 90).
    Returns list of alert strings.

    Args:
        reps: Dict of rep configs with 'start_date' keys.
              Example: {"Jane Smith": {"start_date": "2026-03-01"}}
    """
    alerts = []
    for rep_name, config in reps.items():
        start_str = config.get("start_date")
        if not start_str:
            continue
        days = get_days_since_start(start_str)
        for cp in CHECKPOINTS:
            if days == cp:
                phase = get_ramping_phase(start_str)
                alerts.append(
                    f"RAMPING CHECKPOINT: {rep_name} hat Tag {cp} erreicht "
                    f"(jetzt {PHASE_MAP[phase]['label']}). Performance-Review fällig!"
                )
    return alerts


def traffic_light(actual: float, target: float, green_pct: float = 1.0, yellow_pct: float = 0.8) -> str:
    """Return GRÜN/GELB/ROT based on actual vs target."""
    if target == 0:
        return "GRÜN"
    ratio = actual / target
    if ratio >= green_pct:
        return "GRÜN"
    elif ratio >= yellow_pct:
        return "GELB"
    return "ROT"
