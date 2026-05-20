"""Propositional Logic page."""

import re
import streamlit as st
from utils.logic import eval_proposition, gen_truth_table, check_tautology


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_09-11 · PROPOSITIONAL_LOGIC</div>", unsafe_allow_html=True)
    st.markdown("## Propositional Logic & Truth Tables")

    tab1, tab2, tab3 = st.tabs(["📊 Truth Table Generator", "≡ Equivalence Checker", "∀ Predicates & Quantifiers"])

    with tab1:
        st.markdown("""
        <div class='card'>
          <p style='font-size:0.85rem;'>
          Enter a logical expression using single lowercase letters as variables.<br>
          Operators: <code>&amp;&amp;</code> (AND) &nbsp; <code>||</code> (OR) &nbsp; <code>!</code> (NOT)
          &nbsp; <code>-&gt;</code> (implication) &nbsp; <code>&lt;-&gt;</code> (biconditional) &nbsp; <code>XOR</code>
          </p>
        </div>""", unsafe_allow_html=True)

        expr = st.text_input("Logical expression", "(p && q) -> r", key="tt_expr")
        if st.button("Generate Truth Table", key="tt_run"):
            html, rows = gen_truth_table(expr)
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)
            if rows:
                classification = check_tautology(rows)
                cl_color = "#408A71" if "TAUTOLOGY" in classification else ("#ff6b6b" if "CONTRADICTION" in classification else "#ff9f4a")
                st.markdown(f"<div class='formula' style='color:{cl_color};border-color:{cl_color};'>Classification: {classification}</div>", unsafe_allow_html=True)

        st.markdown("<div class='sec-tag' style='margin-top:1.5rem;'>COMMON EXPRESSIONS TO TRY</div>", unsafe_allow_html=True)
        for ex in ["p -> p", "p || !p", "p && !p",
                   "(p -> q) && (q -> r) -> (p -> r)",
                   "(p && q) -> p", "!(p && q) <-> (!p || !q)"]:
            st.code(ex, language=None)

    with tab2:
        st.markdown("<div class='sec-tag'>PROPOSITIONAL_EQUIVALENCES</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            expr1 = st.text_input("Expression 1", "!(p && q)", key="eq1")
        with col2:
            expr2 = st.text_input("Expression 2", "!p || !q", key="eq2")

        if st.button("Check Logical Equivalence", key="eqchk"):
            all_vars = sorted(set(re.findall(r'\b([a-z])\b', expr1)) | set(re.findall(r'\b([a-z])\b', expr2)))
            if len(all_vars) > 5:
                st.error("Too many variables (max 5)")
            else:
                n = len(all_vars)
                equivalent = True
                diffs = []
                for i in range(1 << n):
                    vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(all_vars)}
                    r1 = eval_proposition(expr1, vals)
                    r2 = eval_proposition(expr2, vals)
                    if r1 != r2:
                        equivalent = False
                        diffs.append({v: vals[v] for v in all_vars})
                if equivalent:
                    st.success(f"✓ **LOGICALLY EQUIVALENT** — {expr1} ≡ {expr2}")
                    st.markdown("<div class='formula'>Identical truth values for all variable assignments</div>", unsafe_allow_html=True)
                else:
                    st.error("✗ **NOT EQUIVALENT** — Counterexample found")
                    st.json(diffs[0])

        st.markdown("<div class='sec-tag' style='margin-top:1.5rem;'>IMPORTANT LOGICAL EQUIVALENCES</div>", unsafe_allow_html=True)
        equiv_laws = [
            ("De Morgan's 1", "¬(p ∧ q) ≡ ¬p ∨ ¬q"),
            ("De Morgan's 2", "¬(p ∨ q) ≡ ¬p ∧ ¬q"),
            ("Double Negation", "¬¬p ≡ p"),
            ("Implication", "p → q ≡ ¬p ∨ q"),
            ("Contrapositive", "p → q ≡ ¬q → ¬p"),
            ("Biconditional", "p ↔ q ≡ (p → q) ∧ (q → p)"),
            ("Absorption", "p ∨ (p ∧ q) ≡ p"),
            ("Distributive", "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)"),
            ("Tautology", "p ∨ ¬p ≡ T"),
            ("Contradiction", "p ∧ ¬p ≡ F"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Law</th><th style='text-align:left'>Equivalence</th></tr></thead><tbody>"
        for law, eq in equiv_laws:
            html += f"<tr><td class='T' style='text-align:left'>{law}</td><td>{eq}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='sec-tag'>PREDICATES & QUANTIFIERS</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='card'>
          <div class='formula'>∀x P(x) — For all x, P(x) is true</div>
          <div class='formula'>∃x P(x) — There exists an x such that P(x) is true</div>
          <p style='font-size:0.85rem;margin-top:0.8rem;'>
          A <b>predicate</b> P(x) becomes a proposition when x is assigned a domain value.
          </p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            domain_raw = st.text_input("Domain (comma-separated integers)", "1, 2, 3, 4, 5", key="dom")
            predicate_type = st.selectbox("Predicate P(x)", [
                "x > 2 (greater than 2)", "x is even", "x is odd",
                "x is prime", "x² < 20", "x > 0 (positive)",
            ])

        if st.button("Evaluate Quantifiers", key="quant_run"):
            domain = [int(x.strip()) for x in domain_raw.split(",") if x.strip().lstrip("-").isdigit()]
            pred_map = {
                "x > 2 (greater than 2)": lambda x: x > 2,
                "x is even": lambda x: x % 2 == 0,
                "x is odd": lambda x: x % 2 != 0,
                "x is prime": lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5)+1)),
                "x² < 20": lambda x: x*x < 20,
                "x > 0 (positive)": lambda x: x > 0,
            }
            pred = pred_map[predicate_type]
            results = {x: pred(x) for x in domain}
            for_all = all(results.values())
            exists = any(results.values())
            true_elems  = [x for x, v in results.items() if v]
            false_elems = [x for x, v in results.items() if not v]

            st.markdown(f"""
            <div class='result-box'>
              <div style='margin-bottom:0.5rem;'><span style='color:#408A71;'>Domain:</span> {{{', '.join(str(x) for x in domain)}}}</div>
              <div style='margin-bottom:0.5rem;'><span style='color:#408A71;'>P(x) true for:</span> {{{', '.join(str(x) for x in true_elems)}}}</div>
              <div style='margin-bottom:0.5rem;'><span style='color:#B0E4CC;'>P(x) false for:</span> {{{', '.join(str(x) for x in false_elems)}}}</div>
              <hr style='border-color:rgba(64,138,113,.2);margin:0.8rem 0;'/>
              <div style='margin-bottom:0.4rem;'>
                <span class='{"T" if for_all else "F"}'>∀x P(x): {"TRUE ✓" if for_all else "FALSE ✗"}</span>
                {f"<span style='color:#6EADA0;font-size:0.72rem;'> — counterexample: x={false_elems[0]}</span>" if not for_all and false_elems else ""}
              </div>
              <div>
                <span class='{"T" if exists else "F"}'>∃x P(x): {"TRUE ✓" if exists else "FALSE ✗"}</span>
                {f"<span style='color:#6EADA0;font-size:0.72rem;'> — witness: x={true_elems[0]}</span>" if exists and true_elems else ""}
              </div>
            </div>""", unsafe_allow_html=True)
