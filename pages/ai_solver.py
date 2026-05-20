"""AI Solver page."""

import streamlit as st
from utils.ai_api import call_groq_nlp, call_notation_converter


def render() -> None:
    st.markdown("<div class='sec-tag'>// AI_POWERED · NATURAL_LANGUAGE_SOLVER</div>", unsafe_allow_html=True)
    st.markdown("## AI Discrete Math Tools")

    tab_chat, tab_notation = st.tabs(["💬 Problem Solver (Chatbot)", "🔣 English → Notation Converter"])

    with tab_chat:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>DISCRETE_MATH_CHATBOT</div>
          <p style='color:#6EADA0;font-size:0.85rem;margin-top:0.4rem;'>
          Type any discrete mathematics problem <b style='color:#408A71;'>in plain English</b> and the AI will:
          interpret it, formulate it mathematically, solve it step-by-step, and give a clear final answer.
          </p>
        </div>""", unsafe_allow_html=True)

        user_problem = st.text_area(
            "Your problem in plain English",
            placeholder="""Examples:
• "How many ways can we choose 3 students from a class of 10 if order doesn't matter?"
• "If all cats are animals, and Whiskers is a cat, what can we conclude?"
• "Prove that the sum of two even numbers is always even."
• "Find the equivalence classes of R = {(1,1),(2,2),(3,3),(1,2),(2,1)} on {1,2,3}"
""",
            height=180,
            key="nlp_input",
        )

        if st.button("🔍 Solve with AI", key="nlp_run"):
            if not user_problem.strip():
                st.error("Please enter a problem.")
            else:
                with st.spinner("Thinking…"):
                    answer = call_groq_nlp(user_problem)
                st.markdown(f"""
                <div class='result-box' style='line-height:1.8;'>
                {answer.replace(chr(10), '<br>')}
                </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Example Questions to Try")
        examples_nlp = [
            "How many 5-letter passwords can be made from 26 letters if no letter repeats?",
            "Is the relation R = {(1,1),(2,2),(3,3),(1,2),(2,1),(2,3),(3,2),(1,3),(3,1)} an equivalence relation?",
            "Using modus ponens: If it rains, the match is cancelled. It is raining. What follows?",
            "Prove by contradiction that there are infinitely many prime numbers.",
            "Find all ways to arrange the letters in the word MATH.",
            "Use mathematical induction to prove that 1+2+3+...+n = n(n+1)/2",
            "What is the reflexive closure of R = {(1,2),(2,3)} on the set {1,2,3}?",
            "If A = {1,2,3,4} and B = {3,4,5,6}, find A union B, A intersection B, and A minus B.",
        ]
        cols = st.columns(2)
        for i, ex in enumerate(examples_nlp):
            with cols[i % 2]:
                st.markdown(f"""
                <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.2);padding:0.6rem 0.9rem;
                border-radius:4px;margin-bottom:0.5rem;font-size:0.78rem;
                font-family:"JetBrains Mono",monospace;border-left:2px solid #408A71;'>
                {ex}
                </div>""", unsafe_allow_html=True)

    with tab_notation:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>ENGLISH → DISCRETE NOTATION</div>
          <p style='color:#6EADA0;font-size:0.85rem;margin-top:0.4rem;'>
          Enter one or more English statements. The AI will identify the atomic propositions,
          assign variables <b style='color:#408A71;'>(p, q, r, …)</b>, and express the statement
          in formal discrete math notation.
          </p>
          <div class='formula' style='margin-top:0.6rem;'>
          "If you have a current password, then you can log onto the network." → p → q
          </div>
        </div>""", unsafe_allow_html=True)

        notation_input = st.text_area(
            label="English statement",
            placeholder="""Enter one or multiple statements, e.g.:

"If you have a current password, then you can log onto the network."
"You have a current password."
"Therefore, you can log onto the network."
""",
            height=160,
            key="notation_input",
        )

        notation_examples = [
            ("Simple implication", "If it is raining, then the ground is wet."),
            ("Conjunction", "It is raining and it is cold."),
            ("Disjunction", "Either the alarm is faulty or there is a fire."),
            ("Negation", "It is not the case that the door is locked."),
            ("Biconditional", "You pass the exam if and only if you score above 60."),
            ("Modus Ponens", "If all cats are animals, and Whiskers is a cat, then Whiskers is an animal."),
            ("Contrapositive", "If the network is down, then you cannot send emails."),
            ("Compound", "If it is raining or snowing, then the road is slippery."),
        ]
        st.markdown("<div style='font-family:\"JetBrains Mono\",monospace;font-size:0.68rem;color:#408A71;letter-spacing:0.1em;margin-bottom:0.4rem;'>QUICK EXAMPLES</div>", unsafe_allow_html=True)
        ecols = st.columns(2)
        for idx, (label, example_text) in enumerate(notation_examples):
            with ecols[idx % 2]:
                st.markdown(f"""
                <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.2);padding:0.5rem 0.8rem;
                border-radius:4px;margin-bottom:0.4rem;border-left:2px solid rgba(64,138,113,.5);'>
                  <div style='font-family:"JetBrains Mono",monospace;font-size:0.62rem;
                  color:#408A71;letter-spacing:0.08em;margin-bottom:0.2rem;'>{label}</div>
                  <div style='font-size:0.78rem;font-style:italic;'>"{example_text}"</div>
                </div>""", unsafe_allow_html=True)

        if st.button("🔣 Convert to Notation", key="notation_run"):
            if not notation_input.strip():
                st.error("Please enter an English statement.")
            else:
                with st.spinner("Converting…"):
                    result = call_notation_converter(notation_input.strip())

                if not result["success"]:
                    st.error(f"Conversion error: {result.get('error', 'Unknown error')}")
                    if result.get("raw"):
                        st.code(result["raw"], language="text")
                else:
                    data = result["data"]
                    vars_data = data.get("variables", [])
                    notation = data.get("notation", "")
                    arg_form = data.get("argument_form", "")
                    form_name = data.get("form_name", "")
                    explanation = data.get("explanation", "")
                    truth_cond = data.get("truth_condition", "")

                    if vars_data:
                        vars_html = "".join(
                            f"<div style='display:flex;align-items:center;gap:0.8rem;padding:0.35rem 0;"
                            f"border-bottom:1px solid rgba(64,138,113,.15);'>"
                            f"<span style='font-family:\"JetBrains Mono\",monospace;font-size:1rem;"
                            f"color:#408A71;font-weight:700;min-width:24px;'>{v['symbol']}</span>"
                            f"<span style='opacity:.5;'>≔</span>"
                            f"<span style='font-size:0.83rem;'>{v['meaning']}</span>"
                            f"</div>"
                            for v in vars_data
                        )
                        st.markdown(f"""
                        <div style='margin-bottom:1rem;'>
                          <div class='sec-tag'>VARIABLE ASSIGNMENTS</div>
                          <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.2);padding:0.7rem 1rem;
                          border-radius:4px;border-left:3px solid #408A71;'>
                          {vars_html}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style='margin-bottom:1rem;'>
                      <div class='sec-tag'>FORMAL NOTATION</div>
                      <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.25);padding:1.1rem 1.4rem;
                      border-radius:4px;text-align:center;'>
                        <span style='font-family:"JetBrains Mono",monospace;font-size:1.6rem;
                        font-weight:700;color:#408A71;letter-spacing:0.06em;'>{notation}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    if arg_form and arg_form.strip():
                        arg_html = arg_form.replace("\\n", "<br>").replace("\n", "<br>")
                        form_label = f" — {form_name}" if form_name else ""
                        st.markdown(f"""
                        <div style='margin-bottom:1rem;'>
                          <div class='sec-tag'>ARGUMENT FORM{form_label.upper()}</div>
                          <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.25);padding:0.9rem 1.2rem;
                          border-radius:4px;font-family:"JetBrains Mono",monospace;
                          font-size:1rem;color:#B0E4CC;line-height:2;'>
                          {arg_html}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    details_html = ""
                    if explanation:
                        details_html += f"<div style='margin-bottom:0.5rem;'><span style='color:#408A71;font-size:0.68rem;letter-spacing:0.08em;font-family:\"JetBrains Mono\",monospace;'>EXPLANATION</span><br><span>{explanation}</span></div>"
                    if truth_cond:
                        details_html += f"<div><span style='color:#408A71;font-size:0.68rem;letter-spacing:0.08em;font-family:\"JetBrains Mono\",monospace;'>TRUTH CONDITION</span><br><span style='opacity:.7;'>{truth_cond}</span></div>"
                    if details_html:
                        st.markdown(f"""
                        <div style='background:rgba(0,0,0,.08);border:1px solid rgba(64,138,113,.2);padding:0.9rem 1.1rem;
                        border-radius:4px;font-size:0.83rem;line-height:1.8;'>
                        {details_html}
                        </div>""", unsafe_allow_html=True)
