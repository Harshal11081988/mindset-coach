"""
content.py
===========
Mindset training exercises grounded in specific, named psychological
frameworks -- deliberately NOT generic motivational quotes. Research
on motivation (e.g. Carol Dweck's growth mindset work) consistently
shows that generic praise/hype produces fragility, not resilience;
specific, process-focused techniques are what actually build
durable mindset change. Each exercise here traces to a real,
citable framework.
"""

EXERCISES = [
    {
        "id": "e001", "theme": "growth-mindset",
        "framework": "Growth Mindset (Carol Dweck)",
        "title": "Reframe a recent setback",
        "prompt": (
            "Think of something that didn't go well recently. Write it as a "
            "\"not yet\" statement instead of a failure statement. E.g. not "
            "\"I failed the interview\" but \"I haven't yet developed this "
            "specific skill the interview tested.\" What's the concrete skill?"
        ),
    },
    {
        "id": "e002", "theme": "growth-mindset",
        "framework": "Growth Mindset (Carol Dweck)",
        "title": "Praise the process, not the outcome",
        "prompt": (
            "Look back at your last check-in. Instead of judging whether the "
            "outcome was good or bad, describe the specific effort or strategy "
            "you used. What's one thing about your PROCESS (not result) you'd "
            "keep doing?"
        ),
    },
    {
        "id": "e003", "theme": "stoic-control",
        "framework": "Dichotomy of Control (Epictetus / Stoicism)",
        "title": "Sort what's actually yours to control",
        "prompt": (
            "Write down what's stressing you right now. Split it into two "
            "lists: things fully within your control (your effort, your "
            "actions, your preparation) and things NOT in your control "
            "(others' decisions, timing, luck). Where should your energy "
            "actually go?"
        ),
    },
    {
        "id": "e004", "theme": "implementation-intentions",
        "framework": "Implementation Intentions (Peter Gollwitzer)",
        "title": "Turn a vague goal into an if-then plan",
        "prompt": (
            "Vague intentions ('I'll study more') rarely work. Pick one goal "
            "and write it as: 'If [specific situation/time], then I will "
            "[specific action].' E.g. 'If it's 7am on a weekday, then I will "
            "study for 30 minutes before checking my phone.'"
        ),
    },
    {
        "id": "e005", "theme": "self-compassion",
        "framework": "Self-Compassion (Kristin Neff)",
        "title": "Talk to yourself like you'd talk to a friend",
        "prompt": (
            "Write down the harshest thing you've said to yourself this week "
            "about a mistake. Now write what you'd actually say to a close "
            "friend who made the same mistake. Notice the gap."
        ),
    },
    {
        "id": "e006", "theme": "resilience",
        "framework": "Cognitive Reframing (CBT-based resilience research)",
        "title": "Separate the event from the story",
        "prompt": (
            "Describe one fact from today (just what objectively happened). "
            "Then separately describe the STORY you're telling yourself about "
            "what it means. Are those actually the same thing?"
        ),
    },
    {
        "id": "e007", "theme": "growth-mindset",
        "framework": "Growth Mindset (Carol Dweck)",
        "title": "Identify the specific skill gap",
        "prompt": (
            "Instead of a vague goal like 'get better,' name ONE specific, "
            "narrow skill you're weakest at right now. What's the smallest "
            "possible practice rep for that specific skill this week?"
        ),
    },
    {
        "id": "e008", "theme": "implementation-intentions",
        "framework": "Implementation Intentions (Peter Gollwitzer)",
        "title": "Plan for your own obstacle",
        "prompt": (
            "What's the most likely reason you'll skip your plan this week? "
            "Be specific (not 'laziness' — what situation actually derails "
            "you?). Write an if-then plan for THAT specific obstacle."
        ),
    },
    {
        "id": "e009", "theme": "stoic-control",
        "framework": "Dichotomy of Control (Epictetus / Stoicism)",
        "title": "Premeditatio malorum (rehearse the setback)",
        "prompt": (
            "Pick something you're working toward. Honestly imagine it NOT "
            "going as planned. What would you actually do next if that "
            "happened? Having the answer ready reduces the fear of it."
        ),
    },
    {
        "id": "e010", "theme": "resilience",
        "framework": "Self-Efficacy Theory (Albert Bandura)",
        "title": "Find your evidence",
        "prompt": (
            "Self-belief isn't built by hype — it's built by remembering real "
            "evidence. Name one specific past instance where you did something "
            "hard and it worked out, even partially. What did you actually do "
            "that made it work?"
        ),
    },
]

THEMES = sorted({e["theme"] for e in EXERCISES})
FRAMEWORKS = sorted({e["framework"] for e in EXERCISES})
