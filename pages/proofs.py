"""Proof Methods page."""

import streamlit as st


PROOF_METHODS = {
    "Direct Proof": {
        "description": "Assume the hypothesis p is true, and use logical steps to show q must be true.",
        "structure": "Assume p.\nStep 1: ...\nStep 2: ...\n∴ q  □",
        "example_claim": "If n is even, then n² is even.",
        "example_proof": """Assume n is even.
→ n = 2k for some integer k  [definition of even]
→ n² = (2k)² = 4k² = 2(2k²)  [algebra]
→ n² = 2m where m = 2k²  [m is an integer]
→ n² is even  [definition of even]  □""",
    },
    "Proof by Contradiction": {
        "description": "Assume p ∧ ¬q is true. Derive a contradiction, proving p → q.",
        "structure": "Assume p and ¬q.\nDerive a contradiction C.\n∴ Our assumption was wrong, so p → q  □",
        "example_claim": "√2 is irrational.",
        "example_proof": """Assume √2 is rational (negation).
→ √2 = a/b where gcd(a,b)=1 (fully reduced)
→ 2 = a²/b²  →  a² = 2b²
→ a² is even  →  a is even
→ a = 2k for some integer k
→ a² = 4k² = 2b²  →  b² = 2k²
→ b² is even  →  b is even
→ Both a and b are even → gcd(a,b) ≥ 2
→ CONTRADICTION with gcd(a,b) = 1  □
∴ √2 is irrational""",
    },
    "Proof by Contrapositive": {
        "description": "To prove p → q, instead prove its contrapositive ¬q → ¬p.",
        "structure": "Assume ¬q.\nStep 1...\n∴ ¬p  □",
        "example_claim": "If n² is odd, then n is odd.",
        "example_proof": """We prove the contrapositive: if n is even, then n² is even.

Assume n is even.
→ n = 2k for some integer k
→ n² = 4k² = 2(2k²)
→ n² is even  □

Since ¬q → ¬p is proven, p → q holds by contrapositive.""",
    },
    "Proof by Cases": {
        "description": "Divide the domain into cases and prove the claim for each case.",
        "structure": "Case 1: ...\nCase 2: ...\nEach case leads to conclusion.\n∴ Holds for all cases  □",
        "example_claim": "For any integer n, n² + n is even.",
        "example_proof": """Case 1: n is even.
  n = 2k  →  n² + n = 4k² + 2k = 2(2k² + k)  →  even ✓

Case 2: n is odd.
  n = 2k+1
  n² + n = (2k+1)² + (2k+1) = 4k²+6k+2 = 2(2k²+3k+1)  →  even ✓

In both cases n² + n is even.  □""",
    },
}


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_14-15 · PROOF_METHODS</div>", unsafe_allow_html=True)
    st.markdown("## Methods of Proving")

    for method, content in PROOF_METHODS.items():
        with st.expander(f"📘 {method}", expanded=(method == "Direct Proof")):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>STRATEGY</div>
                  <p style='font-size:0.85rem;'>{content['description']}</p>
                  <div class='sec-tag' style='margin-top:0.8rem;'>STRUCTURE</div>
                  <pre style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:0.78rem;
                  background:rgba(255,107,53,0.05);padding:0.7rem;border:1px solid rgba(255,107,53,.2);border-radius:4px;'>{content['structure']}</pre>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>WORKED EXAMPLE</div>
                  <div style='font-weight:600;margin-bottom:0.5rem;font-size:0.9rem;'>Claim: {content['example_claim']}</div>
                  <pre style='font-family:"JetBrains Mono",monospace;font-size:0.75rem;
                  background:rgba(0,0,0,.04);padding:0.7rem;border:1px solid rgba(255,107,53,.2);border-radius:4px;
                  white-space:pre-wrap;'>{content['example_proof']}</pre>
                </div>""", unsafe_allow_html=True)
