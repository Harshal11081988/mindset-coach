"""
test_tools.py
===============
Unit tests for deterministic tool logic -- no LLM/API access needed.
"""

from tools import get_mindset_exercise, log_checkin, get_checkin_history, get_progress_summary, list_available_themes
from content import EXERCISES, THEMES

passed = 0
failed = 0


def assert_true(condition, message):
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {message}")


def test_get_exercise_no_filter():
    print("=== get_mindset_exercise: no filter ===")
    ex = get_mindset_exercise()
    assert_true(ex is not None, "should return an exercise with no filters")
    assert_true("framework" in ex, "exercise should cite a real framework")
    print("  PASSED\n")


def test_get_exercise_by_theme():
    print("=== get_mindset_exercise: theme filter ===")
    ex = get_mindset_exercise(theme="growth-mindset")
    assert_true(ex is not None, "should find a growth-mindset exercise")
    assert_true(ex["theme"] == "growth-mindset", "returned exercise should match requested theme")

    ex_case = get_mindset_exercise(theme="GROWTH-MINDSET")
    assert_true(ex_case is not None, "theme filter should be case-insensitive")
    print("  PASSED\n")


def test_get_exercise_unknown_theme():
    print("=== get_mindset_exercise: unknown theme (graceful failure) ===")
    ex = get_mindset_exercise(theme="totally-made-up-theme")
    assert_true(ex is None, "should return None for an unknown theme, not raise or return wrong theme")
    print("  PASSED\n")


def test_get_exercise_exclude_ids():
    print("=== get_mindset_exercise: exclude_ids avoids repeats ===")
    seen = []
    ex1 = get_mindset_exercise(exclude_ids=seen)
    seen.append(ex1["id"])
    ex2 = get_mindset_exercise(exclude_ids=seen)
    assert_true(ex2["id"] != ex1["id"], "should not repeat an already-seen exercise")
    print("  PASSED\n")


def test_get_exercise_all_excluded():
    print("=== get_mindset_exercise: all exercises excluded ===")
    all_ids = [e["id"] for e in EXERCISES]
    ex = get_mindset_exercise(exclude_ids=all_ids)
    assert_true(ex is None, "should return None gracefully when everything is excluded, not raise")
    print("  PASSED\n")


def test_log_checkin_and_history():
    print("=== log_checkin + get_checkin_history ===")
    history = []
    entry = log_checkin(history, mood="tired but okay", effort_today="finished the report", wins="hit the deadline")
    assert_true(len(history) == 1, "history should have one entry after logging")
    assert_true(entry["mood"] == "tired but okay", "logged entry should preserve mood text")
    assert_true(entry["wins"] == "hit the deadline", "logged entry should preserve wins text")
    assert_true(entry["challenges"] == "", "unspecified challenges should default to empty string, not error")

    log_checkin(history, mood="good", effort_today="workout")
    recent = get_checkin_history(history, limit=1)
    assert_true(len(recent) == 1, "should respect the limit parameter")
    assert_true(recent[0]["mood"] == "good", "should return most recent entry when limited")
    print("  PASSED\n")


def test_progress_summary_empty():
    print("=== get_progress_summary: empty history ===")
    summary = get_progress_summary([])
    assert_true(summary["total_checkins"] == 0, "empty history should report 0 checkins, not error")
    assert_true(summary["recent_wins"] == [], "empty history should have empty wins list")
    print("  PASSED\n")


def test_progress_summary_with_data():
    print("=== get_progress_summary: with data ===")
    history = []
    log_checkin(history, mood="good", effort_today="coded", wins="fixed a bug", challenges="")
    log_checkin(history, mood="stressed", effort_today="meetings", wins="", challenges="ran out of time")

    summary = get_progress_summary(history)
    assert_true(summary["total_checkins"] == 2, "should count all checkins")
    assert_true("fixed a bug" in summary["recent_wins"], "should surface actual logged wins")
    assert_true("ran out of time" in summary["recent_challenges"], "should surface actual logged challenges")

    # Verify this is purely factual, not an editorialized "you're doing great!" judgment
    assert_true("total_checkins" in summary and len(summary) == 3,
                "summary should only contain factual fields, no injected sentiment/judgment field")
    print("  PASSED\n")


def test_list_available_themes():
    print("=== list_available_themes ===")
    themes = list_available_themes()
    assert_true(len(themes) > 0, "should list at least one theme")
    assert_true(set(themes) == set(THEMES), "should match the actual themes present in content.py")
    print("  PASSED\n")


def test_content_integrity():
    print("=== content.py data integrity ===")
    ids = [e["id"] for e in EXERCISES]
    assert_true(len(ids) == len(set(ids)), "all exercise IDs should be unique")
    for e in EXERCISES:
        assert_true(len(e["framework"]) > 0, f"{e['title']} should cite a framework")
        assert_true("(" in e["framework"], f"{e['title']}'s framework should cite a real source/author, not just a category name")
    print("  PASSED\n")


if __name__ == "__main__":
    test_get_exercise_no_filter()
    test_get_exercise_by_theme()
    test_get_exercise_unknown_theme()
    test_get_exercise_exclude_ids()
    test_get_exercise_all_excluded()
    test_log_checkin_and_history()
    test_progress_summary_empty()
    test_progress_summary_with_data()
    test_list_available_themes()
    test_content_integrity()

    print(f"\n{passed} passed, {failed} failed")
    if failed > 0:
        exit(1)
    else:
        print("ALL TOOL LOGIC TESTS PASSED")
