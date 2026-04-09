"""
Gap-Detection Matrix: 2-axis diagnosis for individualized coaching.
Replaces simple if/elif chains with Activity x Outcomes classification.
"""


MATRIX = {
    ("RED", "RED"):     ("EFFORT_GAP",      "Aktivität drastisch erhöhen. Calls + Emails auf Target bringen."),
    ("RED", "YELLOW"):  ("EFFORT_GAP",      "Mehr Aktivität bringt überproportionale Ergebnisse."),
    ("RED", "GREEN"):   ("EFFICIENCY_STAR",  "Gute Ergebnisse bei wenig Aktivität. Volumen erhöhen."),
    ("YELLOW", "RED"):  ("SKILL_GAP",       "Aktivität ok, Ergebnisse schwach. Qualität verbessern."),
    ("YELLOW", "YELLOW"):("PLATEAU",        "Leicht unter Target. Sowohl Aktivität als auch Qualität steigern."),
    ("YELLOW", "GREEN"): ("EFFICIENCY_STAR", "Gute Conversion. Mehr Aktivität bringt überproportionale Ergebnisse."),
    ("GREEN", "RED"):   ("SKILL_GAP",       "Hohe Aktivität, schwache Ergebnisse. Qualität verbessern."),
    ("GREEN", "YELLOW"):("SKILL_GAP",       "Aktivität gut, Ergebnisse ausbaufähig. An Conversion arbeiten."),
    ("GREEN", "GREEN"): ("SCALE_GAP",       "Alles on track. Effizienz optimieren, Pipeline ausbauen."),
}


def _traffic_light(actual: float, target: float, green_pct: float = 1.0, yellow_pct: float = 0.8) -> str:
    if target == 0:
        return "GREEN"
    ratio = actual / target
    if ratio >= green_pct:
        return "GREEN"
    elif ratio >= yellow_pct:
        return "YELLOW"
    return "RED"


def _aggregate_signals(signals: list[str]) -> str:
    red = signals.count("RED")
    yellow = signals.count("YELLOW")
    if red >= 2:
        return "RED"
    elif red >= 1 or yellow >= 2:
        return "YELLOW"
    return "GREEN"


def diagnose(metrics: dict, targets: dict = None, phase: str = "phase_4_fully_ramped") -> dict:
    """
    Run the Gap-Detection Matrix on a single rep's daily metrics.

    Args:
        metrics: Dict with calls, calls_connected, connect_rate, emails_sent,
                 meetings_booked, pipeline_value, avg_connected_duration, speed_to_lead
        targets: Optional custom targets dict. If None, uses defaults for the phase.
        phase: Ramping phase key (phase_1_month_1 through phase_4_fully_ramped)

    Returns:
        Dict with main_diagnosis, coaching_focus, activity_status, outcome_status, sub_diagnoses
    """
    # Default targets per phase
    DEFAULT_TARGETS = {
        "phase_1_month_1":     {"calls_per_day": 40, "emails_per_day": 15, "connect_rate": 0.05, "meetings_per_day": 0.4, "pipeline": 30000},
        "phase_2_month_2":     {"calls_per_day": 55, "emails_per_day": 25, "connect_rate": 0.08, "meetings_per_day": 0.8, "pipeline": 60000},
        "phase_3_month_3":     {"calls_per_day": 65, "emails_per_day": 30, "connect_rate": 0.10, "meetings_per_day": 1.2, "pipeline": 100000},
        "phase_4_fully_ramped":{"calls_per_day": 70, "emails_per_day": 40, "connect_rate": 0.12, "meetings_per_day": 1.6, "pipeline": 150000},
    }

    t = targets or DEFAULT_TARGETS.get(phase, DEFAULT_TARGETS["phase_4_fully_ramped"])

    # --- Activity axis ---
    activity_signals = [
        _traffic_light(metrics.get("calls", 0), t["calls_per_day"]),
        _traffic_light(metrics.get("emails_sent", 0), t["emails_per_day"]),
    ]
    activity_status = _aggregate_signals(activity_signals)

    # --- Outcome axis ---
    cr = metrics.get("connect_rate", 0) / 100  # stored as percentage
    outcome_signals = [
        _traffic_light(cr, t["connect_rate"]),
        _traffic_light(metrics.get("meetings_booked", 0), t["meetings_per_day"]),
        _traffic_light(metrics.get("pipeline_value", 0), t["pipeline"]),
    ]
    outcome_status = _aggregate_signals(outcome_signals)

    # --- Matrix lookup ---
    main_diag, coaching_focus = MATRIX.get(
        (activity_status, outcome_status),
        ("PLATEAU", "Moderate Leistung.")
    )

    # --- Sub-diagnoses ---
    sub = []
    if cr >= t["connect_rate"] and metrics.get("meetings_booked", 0) == 0 and metrics.get("calls", 0) > 5:
        sub.append("PITCH: Connects vorhanden, keine Meetings -> Value Prop überarbeiten")
    if cr < 0.08:
        sub.append("OPENER: Connect Rate zu niedrig -> Hook-Rotation testen")
    conn_dur = metrics.get("avg_connected_duration", 0)
    if 0 < conn_dur < 180:
        sub.append(f"TIEFE: Calls zu kurz ({conn_dur}s) -> Offene Fragen, SPIN")
    speed = metrics.get("speed_to_lead", 0)
    if 0 < speed < 900 and speed > 30:
        sub.append(f"SPEED: {round(speed)} min Speed-to-Lead (Target <30)")

    return {
        "main_diagnosis": main_diag,
        "coaching_focus": coaching_focus,
        "activity_status": activity_status,
        "outcome_status": outcome_status,
        "sub_diagnoses": sub,
    }


def diagnose_weakest_dimension(call_scores: list[dict], days: int = 14) -> dict | None:
    """
    Find the weakest scoring dimension across recent calls.

    Args:
        call_scores: List of dicts with keys: date, opener, pitch,
                     objection_handling, closing, depth, rapport
        days: Rolling window in days

    Returns:
        Dict with weakest_dimension, avg_score, training_recommendation, all_dimensions
    """
    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    TRAINING_MAP = {
        "opener": "Hook-Rotation, Pattern-Interrupt, verschiedene Opener testen",
        "pitch": "Value Prop schärfen, Problem-first Pitch, ROI-Argumentation",
        "objection_handling": "LARC-Framework drillen, Reframing, Rückfragen",
        "closing": "1-10 Close, Hypothetical Close, Summary Close, Stille nach Ask",
        "depth": "Offene Fragen, SPIN, Mirroring, 3-Sekunden-Pause",
        "rapport": "Mirroring, Labeling, Active Listening, Tonalität-Training",
    }

    DIMENSIONS = ["opener", "pitch", "objection_handling", "closing", "depth", "rapport"]

    dim_scores = {d: [] for d in DIMENSIONS}
    for cs in call_scores:
        if cs.get("date", "") < cutoff:
            continue
        for d in DIMENSIONS:
            score = cs.get(d)
            if score and float(score) > 0:
                dim_scores[d].append(float(score))

    dim_avgs = {}
    for d, scores in dim_scores.items():
        if scores:
            dim_avgs[d] = round(sum(scores) / len(scores), 1)

    if not dim_avgs:
        return None

    weakest = min(dim_avgs, key=dim_avgs.get)
    return {
        "weakest_dimension": weakest,
        "avg_score": dim_avgs[weakest],
        "training_recommendation": TRAINING_MAP.get(weakest, ""),
        "all_dimensions": dim_avgs,
    }
