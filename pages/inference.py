"""Rules of Inference page."""

import re
import streamlit as st
from utils.logic import eval_proposition


RULES = [
    {
        "name": "Modus Ponens",
        "form": "p → q\np\n∴ q",
        "formula": "(p ∧ (p → q)) → q",
        "example": "If it rains, the ground gets wet. It is raining. ∴ The ground is wet.",
    },
    {
        "name": "Modus Tollens",
        "form": "p → q\n¬q\n∴ ¬p",
        "formula": "(¬q ∧ (p → q)) → ¬p",
        "example": "If it rains, the ground gets wet. The ground is NOT wet. ∴ It did NOT rain.",
    },
    {
        "name": "Hypothetical Syllogism",
        "form": "p → q\nq → r\n∴ p → r",
        "formula": "((p → q) ∧ (q → r)) → (p → r)",
        "example": "If it rains, streets flood. If streets flood, traffic stops. ∴ If it rains, traffic stops.",
    },
    {
        "name": "Disjunctive Syllogism",
        "form": "p ∨ q\n¬p\n∴ q",
        "formula": "((p ∨ q) ∧ ¬p) → q",
        "example": "Either Ali or Sara wrote the code. Ali did not write it. ∴ Sara wrote it.",
    },
    {
        "name": "Addition",
        "form": "p\n∴ p ∨ q",
        "formula": "p → (p ∨ q)",
        "example": "It is raining. ∴ It is raining OR snowing.",
    },
    {
        "name": "Simplification",
        "form": "p ∧ q\n∴ p",
        "formula": "(p ∧ q) → p",
        "example": "It is cold AND raining. ∴ It is cold.",
    },
    {
        "name": "Conjunction",
        "form": "p\nq\n∴ p ∧ q",
        "formula": "(p ∧ q) → (p ∧ q)",
        "example": "It is cold. It is raining. ∴ It is cold AND raining.",
    },
    {
        "name": "Resolution",
        "form": "p ∨ q\n¬p ∨ r\n∴ q ∨ r",
        "formula": "((p ∨ q) ∧ (¬p ∨ r)) → (q ∨ r)",
        "example": "Ali passed OR Sara passed. Ali did not pass OR Huzaifa cheered. ∴ Sara passed OR Huzaifa cheered.",
    },
]


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_12-13 · RULES_OF_INFERENCE</div>", unsafe_allow_html=True)
    st.markdown("## Rules of Inference")
    st.markdown("""
    <p style='font-size:0.85rem;'>
    A <b>rule of inference</b> is a valid argument form that allows us to derive
    new propositions from existing ones — the building blocks of logical proofs.
    </p>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 All Rules", "🧪 Argument Validator"])

    with tab1:
        cols = st.columns(2)
        for idx, rule in enumerate(RULES):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>{rule['name'].upper()}</div>
                  <div class='formula'>{rule['formula']}</div>
                  <pre style='color:#408A71;font-family:"JetBrains Mono",monospace;font-size:0.8rem;
                  background:rgba(64,138,113,0.08);padding:0.6rem;border:1px solid rgba(64,138,113,.2);
                  border-radius:4px;margin:0.6rem 0;'>{rule['form']}</pre>
                  <p style='font-size:0.8rem;'><b style='color:#408A71;'>Example:</b> {rule['example']}</p>
                </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='sec-tag'>ARGUMENT_VALIDATOR</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='font-size:0.85rem;'>
        Enter premises and a conclusion. The validator checks if the argument is valid
        (conclusion is a tautological consequence of the premises).
        </p>""", unsafe_allow_html=True)

        premises_raw = st.text_area(
            "Premises (one per line, use p,q,r as variables)",
            "p -> q\np", key="premises_input",
        )
        conclusion_raw = st.text_input("Conclusion", "q", key="conc_input")

        if st.button("Validate Argument", key="arg_val"):
            premises_list = [p.strip() for p in premises_raw.strip().split("\n") if p.strip()]
            all_vars = sorted(set(re.findall(r'\b([a-z])\b', premises_raw + " " + conclusion_raw)))
            if len(all_vars) > 5:
                st.error("Too many variables (max 5)")
            elif not all_vars:
                st.error("No variables found")
            else:
                n = len(all_vars)
                valid = True
                counterexample = None
                for i in range(1 << n):
                    vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(all_vars)}
                    if all(eval_proposition(p, vals) for p in premises_list):
                        if not eval_proposition(conclusion_raw, vals):
                            valid = False
                            counterexample = vals
                            break
                if valid:
                    st.success("✓ VALID ARGUMENT — The conclusion follows logically from the premises")
                    combined = " ∧ ".join(f"({p})" for p in premises_list)
                    st.markdown(f"<div class='formula'>({combined}) → ({conclusion_raw}) is a tautology</div>", unsafe_allow_html=True)
                else:
                    st.error("✗ INVALID ARGUMENT — Counterexample found")
                    st.json(counterexample)
