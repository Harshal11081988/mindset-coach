"""
agent.py
=========
Same agentic tool-calling loop pattern as the recommendation agent
project, adapted for stateful check-in history (bound per-instance via
closures, since the LLM shouldn't be responsible for passing its own
conversation history back to itself as a tool argument).

⚠️ Same honesty boundary as the recommendation agent: the tool logic
and control flow are tested (see test_tools.py, test_agent_loop.py).
Live conversation quality with the real model was NOT tested -- no
API key was available in the build environment. See README.

SYSTEM PROMPT DESIGN NOTE: this was deliberately NOT written as a
generic hype/motivation bot. Research on motivation and resilience
(Dweck's growth mindset work, Bandura's self-efficacy theory) shows
generic praise and unconditional encouragement tend to produce
fragility, not resilience -- what actually works is specific,
process-focused feedback grounded in real evidence. The prompt below
instructs the agent to behave that way: encouraging, but never
uncritically validating, and willing to name when a plan seems
unrealistic rather than just cheering it on.
"""

import anthropic
from tools import TOOL_SCHEMAS, get_mindset_exercise, log_checkin, get_progress_summary, list_available_themes

MODEL = "claude-sonnet-4-5"
MAX_TOOL_ITERATIONS = 6

SYSTEM_PROMPT = """You are a mindset coach grounded in real psychological research (growth mindset, stoic philosophy, self-efficacy theory, implementation intentions, self-compassion research) -- not a generic hype or motivation bot.

Core rules for how you coach:
- NEVER give generic, content-free encouragement ("you've got this!", "believe in yourself!"). Every response should be specific to what the user actually said.
- Praise PROCESS and EFFORT, not outcomes or talent -- this is a deliberate, research-backed choice (Dweck's growth mindset research shows outcome/talent praise produces fragility, not resilience).
- When the user shares a check-in, use log_checkin to record it, then respond to the SPECIFIC content (not a generic "great job").
- Use get_mindset_exercise to give a concrete, grounded exercise when it fits the conversation -- don't just talk in the abstract.
- Use get_progress_summary before making any claim about the user's trend/progress -- ground feedback in actual logged history, not assumption.
- If the user describes a plan or goal that seems unrealistic (e.g. an extreme timeline, an all-or-nothing framing, ignoring real constraints), name that honestly and directly, the way a good coach would -- don't just validate it. This is more valuable to the user than false encouragement.
- If the user seems to be in real distress (not just normal frustration/setback), don't try to "coach" them out of it with exercises -- gently suggest they talk to a person they trust or a professional, and keep the door open rather than pushing mindset content at someone who needs actual support.
- Keep responses conversational and concise.
"""


class MindsetCoachAgent:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.messages = []
        self.checkin_history = []  # bound into the tool closures below
        self.used_exercise_ids = []

        # Bind stateful tools to this instance's history via closures,
        # so the tool-call interface the LLM sees (get_mindset_exercise,
        # log_checkin, get_progress_summary) never needs the model to
        # pass conversation state as an argument -- that's app-internal.
        self._tool_functions = {
            "get_mindset_exercise": self._get_mindset_exercise,
            "log_checkin": self._log_checkin,
            "get_progress_summary": self._get_progress_summary,
            "list_available_themes": list_available_themes,
        }

    def _get_mindset_exercise(self, theme=None):
        result = get_mindset_exercise(theme=theme, exclude_ids=self.used_exercise_ids)
        if result is not None:
            self.used_exercise_ids.append(result["id"])
        return result

    def _log_checkin(self, mood, effort_today, wins=None, challenges=None):
        return log_checkin(self.checkin_history, mood, effort_today, wins, challenges)

    def _get_progress_summary(self):
        return get_progress_summary(self.checkin_history)

    def _execute_tool(self, tool_name, tool_input):
        if tool_name not in self._tool_functions:
            return {"error": f"Unknown tool: {tool_name}"}
        try:
            return self._tool_functions[tool_name](**tool_input)
        except TypeError as e:
            return {"error": f"Invalid arguments for {tool_name}: {e}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {e}"}

    def send_message(self, user_text):
        self.messages.append({"role": "user", "content": user_text})

        for _ in range(MAX_TOOL_ITERATIONS):
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS,
                messages=self.messages,
            )
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                return "".join(block.text for block in response.content if block.type == "text")

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                result = self._execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
            self.messages.append({"role": "user", "content": tool_results})

        return (
            "I'm having trouble working through this in one go — could you "
            "tell me specifically what's on your mind right now, in a "
            "sentence or two?"
        )
