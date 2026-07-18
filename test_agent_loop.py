"""
test_agent_loop.py
=====================
Tests the agentic loop's control flow using mocked Claude API
responses. Does NOT test real conversation quality -- see agent.py
and README for that honesty boundary.
"""

from unittest.mock import MagicMock
from agent import MindsetCoachAgent, MAX_TOOL_ITERATIONS

passed = 0
failed = 0


def assert_true(condition, message):
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {message}")


def make_text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    response = MagicMock()
    response.content = [block]
    response.stop_reason = "end_turn"
    return response


def make_tool_use_response(tool_name, tool_input, tool_use_id="toolu_test"):
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = tool_input
    block.id = tool_use_id
    response = MagicMock()
    response.content = [block]
    response.stop_reason = "tool_use"
    return response


def test_checkin_logged_via_bound_tool():
    print("=== log_checkin tool call actually writes to agent's own history ===")
    agent = MindsetCoachAgent(api_key="fake-key")

    tool_call = make_tool_use_response("log_checkin", {"mood": "tired", "effort_today": "debugged all day", "wins": "fixed the bug"})
    final = make_text_response("Sounds like a grind, but you got the bug fixed. What was the actual fix?")
    agent.client.messages.create = MagicMock(side_effect=[tool_call, final])

    agent.send_message("tired today, spent hours debugging but fixed it")

    assert_true(len(agent.checkin_history) == 1, "check-in should be logged to the agent's own history")
    assert_true(agent.checkin_history[0]["mood"] == "tired", "logged mood should match what the model extracted")
    assert_true(agent.checkin_history[0]["wins"] == "fixed the bug", "logged wins should match")
    print("  PASSED\n")


def test_exercise_not_repeated_within_session():
    print("=== get_mindset_exercise avoids repeating within a session ===")
    agent = MindsetCoachAgent(api_key="fake-key")

    call1 = make_tool_use_response("get_mindset_exercise", {})
    resp1 = make_text_response("Here's an exercise for you.")
    agent.client.messages.create = MagicMock(side_effect=[call1, resp1])
    agent.send_message("give me an exercise")

    first_exercise_id = agent.used_exercise_ids[0]

    call2 = make_tool_use_response("get_mindset_exercise", {})
    resp2 = make_text_response("Here's another one.")
    agent.client.messages.create = MagicMock(side_effect=[call2, resp2])
    agent.send_message("give me another one")

    assert_true(len(agent.used_exercise_ids) == 2, "should track two used exercises after two requests")
    assert_true(agent.used_exercise_ids[1] != first_exercise_id, "second exercise should differ from the first")
    print("  PASSED\n")


def test_progress_summary_reflects_real_history():
    print("=== get_progress_summary tool reflects actual logged check-ins ===")
    agent = MindsetCoachAgent(api_key="fake-key")
    agent.checkin_history.append({"mood": "good", "effort_today": "workout", "wins": "ran 5k", "challenges": ""})
    agent.checkin_history.append({"mood": "meh", "effort_today": "work", "wins": "", "challenges": "missed a deadline"})

    call = make_tool_use_response("get_progress_summary", {})
    final = make_text_response("Looking at your recent check-ins...")
    agent.client.messages.create = MagicMock(side_effect=[call, final])

    agent.send_message("how am I doing?")

    # Verify the tool_result sent back to the model contains the REAL data, not a placeholder
    tool_result_messages = [m for m in agent.messages if m["role"] == "user" and isinstance(m["content"], list)]
    content_str = tool_result_messages[-1]["content"][0]["content"]
    assert_true("ran 5k" in content_str, "progress summary sent to model should include real logged win")
    assert_true("missed a deadline" in content_str, "progress summary sent to model should include real logged challenge")
    print("  PASSED\n")


def test_unknown_theme_handled_gracefully():
    print("=== Unknown exercise theme handled without crashing ===")
    agent = MindsetCoachAgent(api_key="fake-key")

    call = make_tool_use_response("get_mindset_exercise", {"theme": "made-up-theme"})
    final = make_text_response("I don't have that exact theme, but here's a related one.")
    agent.client.messages.create = MagicMock(side_effect=[call, final])

    result = agent.send_message("give me a made-up-theme exercise")
    assert_true(result == "I don't have that exact theme, but here's a related one.", "should recover gracefully")
    assert_true(len(agent.used_exercise_ids) == 0, "no exercise should be marked used when the lookup returned None")
    print("  PASSED\n")


def test_safety_cap():
    print("=== Safety cap triggers on runaway tool use ===")
    agent = MindsetCoachAgent(api_key="fake-key")
    always_tool = make_tool_use_response("get_progress_summary", {})
    agent.client.messages.create = MagicMock(return_value=always_tool)

    result = agent.send_message("test")

    assert_true(agent.client.messages.create.call_count == MAX_TOOL_ITERATIONS, "should stop at the iteration cap")
    assert_true("tell me specifically" in result or "one go" in result, "should return a clear message, not hang or crash")
    print("  PASSED\n")


if __name__ == "__main__":
    test_checkin_logged_via_bound_tool()
    test_exercise_not_repeated_within_session()
    test_progress_summary_reflects_real_history()
    test_unknown_theme_handled_gracefully()
    test_safety_cap()

    print(f"\n{passed} passed, {failed} failed")
    if failed > 0:
        exit(1)
    else:
        print("ALL AGENT LOOP CONTROL-FLOW TESTS PASSED")
