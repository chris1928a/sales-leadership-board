"""
Objection Handling Library with LARC Framework.
44 pre-written scripts mapped to common B2B sales objections.
Fuzzy-matching for automatic assignment of lost reasons to scripts.
"""

from difflib import SequenceMatcher


# Core objection scripts (LARC: Listen-Acknowledge-Respond-Confirm)
OBJECTION_SCRIPTS = {
    "arbeiten mit anderem recruiter": (
        "Verstehe ich. Darf ich fragen: Wenn der aktuelle Partner morgen aufhört, "
        "was würde Ihnen am meisten fehlen? -- Genau das können wir auch, plus [USP]. "
        "Lassen Sie uns 15 Min sprechen, damit Sie einen Vergleich haben."
    ),
    "fees zu hoch": (
        "Die Fee spiegelt die Qualität wider. Rechnen wir kurz: Was kostet eine "
        "Fehlbesetzung? Wir garantieren [Garantie], d.h. Ihr Risiko ist minimiert. "
        "Welche Positionen sind am dringendsten?"
    ),
    "internes recruiting team": (
        "Super, dass Sie intern aufgestellt sind. Viele unserer Kunden nutzen uns "
        "als Erweiterung für Spezial-Profile, die intern schwer zu finden sind. "
        "Haben Sie gerade solche Engpässe?"
    ),
    "stellen nicht ein": (
        "Verstehe, aktuell kein Bedarf. Darf ich fragen: Wenn Sie in Q3/Q4 wieder "
        "wachsen, was wäre die erste Rolle? Ich schicke Ihnen einen Markt-Report "
        "zu dem Profil, damit Sie vorbereitet sind."
    ),
    "schlechte erfahrungen": (
        "Das tut mir leid. Was genau ist schiefgelaufen? -- Danke fürs Teilen. "
        "Genau deshalb arbeiten wir mit [Differenzierung: Shortlist in 5 Tagen, "
        "Qualitätsgarantie]. Wollen wir einen kleinen Test machen mit einer Rolle?"
    ),
    "muss nachdenken": (
        "Absolut. Damit Sie eine gute Entscheidung treffen können: Was genau "
        "müssten Sie noch wissen? -- Ich schicke Ihnen [Case Study / Referenz]. "
        "Passt Donnerstag für einen kurzen Follow-up?"
    ),
    "kein interesse": (
        "Verstehe. Nur eine kurze Frage: Wenn Sie an Ihre größte Recruiting-"
        "Herausforderung der letzten 6 Monate denken, was war das? -- Genau da "
        "setzen wir an. 10 Minuten, und ich zeige Ihnen wie."
    ),
    "kein budget": (
        "Budget ist immer ein Thema. Unsere Kunden sehen uns als Investment: "
        "Pro Einstellung [ROI-Argument]. Gibt es eine Rolle, die so dringend ist, "
        "dass sie Budget rechtfertigen würde?"
    ),
    "zu viele bewerbungen": (
        "Genau das hören wir oft. 300 Bewerbungen, davon 5 relevant. "
        "Wir schicken Ihnen keine 300. Wir schicken 3, alle vorqualifiziert "
        "per Topgrading. Wenn keiner passt, kostet Sie das nichts."
    ),
    "kein zeitdruck": (
        "Verstehe. Genau deshalb wäre jetzt der beste Zeitpunkt: Wenn kein Druck da ist, "
        "können wir in Ruhe die besten Profile am Markt identifizieren. Frühzeitig "
        "anfangen heißt bessere Auswahl. Wann wäre ein guter Zeitpunkt für 15 Min?"
    ),
}


def match_objection(lost_reason: str) -> tuple[str | None, str | None]:
    """
    Fuzzy-match a lost reason to the best objection script.
    Returns (matched_key, script_text) or (None, None).
    """
    if not lost_reason:
        return None, None

    reason_lower = lost_reason.lower().strip()
    best_key, best_score = None, 0.0

    for key in OBJECTION_SCRIPTS:
        score = SequenceMatcher(None, reason_lower, key).ratio()
        # Boost if key appears as substring
        if key in reason_lower or reason_lower in key:
            score = max(score, 0.85)
        if score > best_score:
            best_score = score
            best_key = key

    if best_score >= 0.45 and best_key:
        return best_key, OBJECTION_SCRIPTS[best_key]

    return None, None


def get_all_scripts() -> dict:
    """Return the full objection library."""
    return dict(OBJECTION_SCRIPTS)
