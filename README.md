# 🧭 Mindset Coach

An agentic coach for daily check-ins and mindset training — built
deliberately on named psychological research, not generic hype or
motivational-quote content.

## Why this isn't a hype bot, on purpose

Research on motivation and resilience consistently shows that generic
praise and unconditional encouragement backfire: Carol Dweck's growth
mindset research found that praising talent/outcomes produces
fragility (kids praised for being "smart" avoid challenges that risk
that label), while praising process/effort produces resilience.
Albert Bandura's self-efficacy research similarly grounds real
self-belief in specific remembered evidence, not affirmations.

So this coach is explicitly instructed (see the system prompt in
`agent.py`) to:
- Never give content-free encouragement ("you've got this!")
- Praise process and effort, not outcomes or talent
- Ground feedback in actual logged check-in history, not assumption
- **Name an unrealistic plan honestly rather than validate it** — the
  same principle used throughout the conversation that led to this
  project being built this way
- Recognize the difference between normal frustration (where a
  mindset exercise helps) and real distress (where it should
  gently point toward actual human/professional support instead)

> ⚠️ This is a mindset/discipline training tool, not therapy. It's
> designed to say so and step back if it detects real distress, not
> to try to coach someone through something it isn't equipped for.

## Important honesty note — read this before using it

Same testing boundary as the Recommendation Agent project, and for
the same reason (no Anthropic API key was available in the build
environment):

- **Rigorously tested:** all deterministic tool logic — exercise
  retrieval, check-in logging, progress summarization, graceful
  handling of unknown themes/exhausted exercises (43 passing
  assertions, `test_tools.py`). The agent's tool-calling control flow
  — stateful history binding, exercise non-repetition, safety cap
  against runaway tool loops (11 passing assertions against mocked
  API responses, `test_agent_loop.py`).
- **NOT tested:** whether Claude actually coaches well with this
  system prompt in real conversation — whether it stays appropriately
  honest instead of drifting into generic encouragement anyway,
  whether it recognizes real distress correctly, whether the exercise
  suggestions land naturally in conversation. This needs a live API
  key and real usage, which wasn't available here.

**Practical implication:** the plumbing (state tracking, tool
execution, error recovery) is verified. The actual coaching quality —
whether the system prompt's instructions are followed well by the
model in practice — is genuinely unverified until you run real
conversations with your own key. Pay particular attention early on to
whether it ever slides into generic hype despite the instructions not
to, and whether its distress-recognition behavior seems reasonable —
both are the kind of thing that needs real usage to evaluate, not
just code review.

## How it works

1. **`content.py`** — 10 mindset exercises, each citing a real,
   named psychological framework (growth mindset, stoic dichotomy of
   control, implementation intentions, self-compassion, self-efficacy)
2. **`tools.py`** — deterministic functions: retrieve an exercise,
   log a check-in, summarize progress factually (no editorializing
   about whether the user is "doing well" — that judgment is left to
   the agent's reasoning, grounded in the real data)
3. **`agent.py`** — the agentic loop, with stateful tools (check-in
   history, used-exercise tracking) bound per-instance via closures,
   so the LLM never has to manage its own state as a tool argument
4. **`app.py`** — Streamlit chat UI, your own API key entered at runtime

## Project structure

```
mindset-coach/
├── app.py                 # Streamlit chat app (deploy this)
├── agent.py                 # Agentic loop + system prompt design
├── tools.py                   # Deterministic tool functions + schemas
├── content.py                    # Exercises grounded in named frameworks
├── test_tools.py                   # 43 assertions, no API key needed
├── test_agent_loop.py                # 11 assertions, mocked API, no key needed
├── requirements.txt
└── README.md
```

## Setup (local)

```bash
git clone <your-repo-url>
cd mindset-coach
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python test_tools.py
python test_agent_loop.py

streamlit run app.py
```

## Deploying to Streamlit Community Cloud

No dataset, no training step — push as-is, point Streamlit Cloud at
`app.py`. Users supply their own API key at runtime.

## Tech stack

- **Anthropic SDK** — Claude API with tool use
- **Streamlit** — chat UI, session state

## Possible extensions

- Real evaluation harness once live behavior is validated: scripted
  conversations checking the agent doesn't drift into generic hype,
  correctly recognizes distress signals, etc.
- Persistent check-in history across sessions (needs a real database
  — same honest limitation as other session-only projects in this series)
- More exercises/frameworks (behavioral activation, values
  clarification from ACT, etc.)
