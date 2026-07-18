"""
Mindset Coach — Grounded Motivation & Discipline Training
--------------------------------------------------------------
An agentic coach for daily check-ins and mindset training, built on
named psychological frameworks (growth mindset, stoicism, self-
efficacy theory) rather than generic hype. Designed to encourage
without uncritical validation -- it will name an unrealistic plan
honestly rather than just cheer it on, because that's what actually
helps.

⚠️ Requires your own Anthropic API key. Not a substitute for therapy
or professional mental health support -- see the in-app note and
README.

Run locally with: streamlit run app.py
"""

import streamlit as st
from agent import MindsetCoachAgent

st.set_page_config(page_title="Mindset Coach", page_icon="🧭", layout="centered")


def init_session_state():
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def main():
    st.title("🧭 Mindset Coach")
    st.caption(
        "Daily check-ins and mindset training grounded in real psychological research — "
        "not generic hype. Expect specific feedback, not just encouragement."
    )

    st.warning(
        "⚠️ This is a mindset/discipline training tool, not therapy or mental health "
        "support. If you're going through something serious, please talk to a person "
        "you trust or a professional — this app isn't equipped for that, and it's "
        "designed to say so rather than try to coach you through real distress."
    )

    with st.expander("⚠️ Before you use this — please read"):
        st.markdown(
            "- **Requires your own Anthropic API key** ([console.anthropic.com](https://console.anthropic.com)). "
            "Never stored or logged by this app.\n"
            "- **Deliberately not a hype bot.** Research on motivation (Dweck's growth "
            "mindset work, Bandura's self-efficacy theory) shows generic praise produces "
            "fragility, not resilience. This coach is instructed to give specific, "
            "process-focused feedback and to name unrealistic plans honestly rather than "
            "validate them.\n"
            "- **Check-in history is session-only** — it resets on refresh. This is a "
            "conscious limitation, not an oversight (same as the Neuroplasticity Tracker "
            "and Voice Biomarker projects) — real persistence would need a database.\n"
            "- **Testing boundary:** the tool logic (43 assertions) and agent control flow "
            "(11 assertions, mocked API) were rigorously tested. The live conversation "
            "quality with the real model was NOT tested before shipping — no API key was "
            "available in the build environment. Your early conversations are its real "
            "test. See the GitHub README."
        )

    init_session_state()

    api_key = st.text_input("Anthropic API key", type="password", placeholder="sk-ant-...")

    if not api_key:
        st.info("Enter your Anthropic API key above to start.")
        return

    if st.session_state.agent is None:
        st.session_state.agent = MindsetCoachAgent(api_key=api_key)

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(text)

    user_input = st.chat_input("How's it going? What are you working on?")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response_text = st.session_state.agent.send_message(user_input)
                except Exception as e:
                    response_text = f"Something went wrong talking to the API: {e}"
            st.markdown(response_text)

        st.session_state.chat_history.append(("assistant", response_text))

    if st.session_state.chat_history:
        if st.button("Start over"):
            st.session_state.agent = MindsetCoachAgent(api_key=api_key)
            st.session_state.chat_history = []
            st.rerun()


if __name__ == "__main__":
    main()
