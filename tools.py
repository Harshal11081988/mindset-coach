"""
tools.py
=========
Deterministic tool functions the mindset coach agent can call.
Check-in history is held in a plain list passed in by the caller
(not global state) so this stays fully unit-testable in isolation --
same pattern as the recommendation agent project.
"""

from content import EXERCISES, THEMES


def get_mindset_exercise(theme=None, exclude_ids=None):
    """
    Return one mindset training exercise, optionally filtered by theme
    and excluding already-used exercise IDs. Returns None if nothing
    matches.
    """
    exclude_ids = set(exclude_ids or [])
    candidates = [e for e in EXERCISES if e["id"] not in exclude_ids]

    if theme:
        theme_matches = [e for e in candidates if e["theme"].lower() == theme.lower()]
        if theme_matches:
            candidates = theme_matches
        else:
            return None  # explicit no-match, so the agent can recover honestly

    if not candidates:
        return None

    return candidates[0]


def log_checkin(history, mood, effort_today, wins=None, challenges=None):
    """
    Append a check-in entry to the history list (mutates and returns
    it, so the caller keeps a single source of truth). mood and
    effort_today are user-provided free text or simple ratings --
    this function doesn't validate/judge their content, only records it.
    """
    entry = {
        "mood": mood,
        "effort_today": effort_today,
        "wins": wins or "",
        "challenges": challenges or "",
    }
    history.append(entry)
    return entry


def get_checkin_history(history, limit=10):
    """Return the most recent `limit` check-ins, most recent last."""
    return history[-limit:]


def get_progress_summary(history):
    """
    Summarize check-in history factually -- counts and recent patterns
    only, no editorializing about whether the user is "doing well."
    That judgment belongs to the agent's reasoning (and the user),
    not baked into this deterministic function.
    """
    if not history:
        return {"total_checkins": 0, "recent_challenges": [], "recent_wins": []}

    recent = history[-5:]
    return {
        "total_checkins": len(history),
        "recent_wins": [h["wins"] for h in recent if h.get("wins")],
        "recent_challenges": [h["challenges"] for h in recent if h.get("challenges")],
    }


def list_available_themes():
    """List all mindset exercise themes available, for graceful recovery on an unknown theme request."""
    return THEMES


# ---- Tool schemas for the Anthropic API ----
TOOL_SCHEMAS = [
    {
        "name": "get_mindset_exercise",
        "description": (
            "Retrieve one mindset training exercise grounded in a real psychological "
            "framework (growth mindset, stoic dichotomy of control, implementation "
            "intentions, self-compassion, resilience). Use this to give the user a "
            "concrete exercise rather than generic encouragement."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "theme": {"type": "string",
                          "description": f"Optional theme filter. Available: {', '.join(THEMES)}"},
                "exclude_ids": {"type": "array", "items": {"type": "string"},
                                 "description": "Exercise IDs already given this conversation, to avoid repeats"},
            },
        },
    },
    {
        "name": "log_checkin",
        "description": (
            "Record the user's check-in: mood, effort/work done today, wins, and "
            "challenges. Use this when the user shares how their day/work went."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mood": {"type": "string", "description": "How the user describes their mood/state"},
                "effort_today": {"type": "string", "description": "What the user actually did/worked on"},
                "wins": {"type": "string", "description": "Specific things that went well, if mentioned"},
                "challenges": {"type": "string", "description": "Specific difficulties, if mentioned"},
            },
            "required": ["mood", "effort_today"],
        },
    },
    {
        "name": "get_progress_summary",
        "description": "Get a factual summary of check-in history (counts, recent wins/challenges) to ground feedback in actual logged data rather than assumptions.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_available_themes",
        "description": "List available mindset exercise themes, for recovering gracefully if a requested theme doesn't exist.",
        "input_schema": {"type": "object", "properties": {}},
    },
]
