"""Mathematical Induction page."""

import streamlit as st
from utils.logic import induction_checker


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_16 · MATHEMATICAL_INDUCTION</div>", unsafe_allow_html=True)
    st.markdown("## Mathematical Induction")
    st.markdown("""
    <div class='card'>
      <div class='formula'>Base Case: P(1) is true</div>
      <div class='formula'>Inductive Step: P(k) true → P(k+1) true</div>
      <div class='formula'>Conclusion: P(n) is true for all n ≥ 1</div>
      <p style='font-size:0.85rem;margin-top:0.8rem;'>
      Like a chain of dominoes: prove the first falls, and prove each one knocks the next. Then all fall.
      </p>
    </div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🧮 Formula Verifier", "📋 Classic Proofs"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            formula_type = st.selectbox("Choose formula to verify", [
                "sum_natural — Σi = n(n+1)/2",
                "sum_squares — Σi² = n(n+1)(2n+1)/6",
                "geometric — Σ2^i = 2^(n+1)-1",
                "power_of_2 — 2^n divisible by 2",
            ])
            n_val = st.number_input("Check for n =", min_value=1, max_value=30, value=5, key="ind_n")

        if st.button("Verify by Induction", key="ind_run"):
            ft = formula_type.split(" — ")[0]
            result = induction_checker(ft, int(n_val))
            st.markdown(f"""
            <div class='result-box'>
            <pre style='white-space:pre-wrap;margin:0;font-family:"JetBrains Mono",monospace;font-size:0.82rem;'>{result}</pre>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Step-by-step: Prove Σi = n(n+1)/2")
        n_demo = st.slider("n", 1, 15, 4, key="ind_demo")
        actual = sum(range(1, n_demo + 1))
        formula_val = n_demo * (n_demo + 1) // 2
        steps_html = ""
        running = 0
        for i in range(1, n_demo + 1):
            running += i
            steps_html += f"<div style='opacity:.7;'> + {i} = {running}</div>"
        st.markdown(f"""
        <div class='result-box'>
          <div style='color:#FF6B35;margin-bottom:0.5rem;'>Base case (n=1): 1 = 1·2/2 = 1 ✓</div>
          <div style='margin-bottom:0.4rem;'>Running sum 1 to {n_demo}:</div>
          {steps_html}
          <hr style='border-color:rgba(255,107,53,.2);margin:0.6rem 0;'/>
          <div style='color:#FF6B35;font-weight:600;'>Σ(1..{n_demo}) = {actual}</div>
          <div style='margin-bottom:0;'>Formula: {n_demo}·{n_demo+1}/2 = {formula_val}</div>
          <div style='color:{"#FF6B35" if actual == formula_val else "#FF5252"};margin-top:0.3rem;'>
            {"✓ Match! Induction holds." if actual == formula_val else "✗ Mismatch!"}
          </div>
        </div>""", unsafe_allow_html=True)

    with tab2:
        proofs = [
            {
                "title": "Sum of First n Natural Numbers",
                "claim": "For all n ≥ 1: 1 + 2 + ... + n = n(n+1)/2",
                "base": "P(1): LHS = 1, RHS = 1·2/2 = 1. ✓",
                "hyp": "P(k): Assume 1 + 2 + ... + k = k(k+1)/2",
                "step": "P(k+1): k(k+1)/2 + (k+1) = (k+1)[k/2+1] = (k+1)(k+2)/2 ✓",
            },
            {
                "title": "Sum of First n Odd Numbers",
                "claim": "For all n ≥ 1: 1 + 3 + 5 + ... + (2n-1) = n²",
                "base": "P(1): LHS = 1, RHS = 1² = 1. ✓",
                "hyp": "P(k): Assume 1 + 3 + ... + (2k-1) = k²",
                "step": "P(k+1): k² + (2k+1) = k² + 2k + 1 = (k+1)² ✓",
            },
            {
                "title": "Power of 2 Inequality",
                "claim": "For all n ≥ 1: 2ⁿ > n",
                "base": "P(1): 2¹ = 2 > 1. ✓",
                "hyp": "P(k): Assume 2ᵏ > k",
                "step": "P(k+1): 2^(k+1) = 2·2ᵏ > 2k ≥ k+1 for k≥1 ✓",
            },
        ]
        for proof in proofs:
            with st.expander(f"📗 {proof['title']}"):
                st.markdown(f"""
                <div class='card'>
                  <div style='font-weight:600;margin-bottom:0.8rem;'>{proof['claim']}</div>
                  <div style='margin-bottom:0.6rem;'>
                    <span style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>BASE CASE:</span><br>
                    <span style='font-size:0.85rem;'>{proof['base']}</span>
                  </div>
                  <div style='margin-bottom:0.6rem;'>
                    <span style='color:#FFA060;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>INDUCTIVE HYPOTHESIS:</span><br>
                    <span style='font-size:0.85rem;'>{proof['hyp']}</span>
                  </div>
                  <div>
                    <span style='color:#FFA060;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>INDUCTIVE STEP:</span><br>
                    <pre style='font-size:0.83rem;background:rgba(0,0,0,.04);padding:0.6rem;border:1px solid rgba(255,107,53,.2);
                    border-radius:4px;white-space:pre-wrap;margin-top:0.3rem;'>{proof['step']}</pre>
                  </div>
                </div>""", unsafe_allow_html=True)
