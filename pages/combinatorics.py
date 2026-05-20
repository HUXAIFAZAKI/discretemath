"""Combinatorics page."""

import math
import streamlit as st


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_09-10 · COMBINATORICS</div>", unsafe_allow_html=True)
    st.markdown("## Counting & Combinatorics")

    tab1, tab2, tab3 = st.tabs(["🔢 P(n,r) & C(n,r)", "🐦 Pigeonhole Principle", "📐 Counting Principles"])

    with tab1:
        st.markdown("""
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;'>
          <div class='card'>
            <div class='sec-tag'>PERMUTATIONS</div>
            <div class='formula'>P(n,r) = n! / (n-r)!</div>
            <p style='font-size:0.82rem;'>Ordered arrangements — order matters.</p>
          </div>
          <div class='card'>
            <div class='sec-tag'>COMBINATIONS</div>
            <div class='formula'>C(n,r) = n! / (r!(n-r)!)</div>
            <p style='font-size:0.82rem;'>Unordered selections — order does NOT matter.</p>
          </div>
        </div>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            n_val = st.number_input("n (total items)", min_value=0, max_value=30, value=10, key="comb_n")
        with col2:
            r_val = st.number_input("r (chosen)", min_value=0, max_value=30, value=3, key="comb_r")
        with col3:
            st.write("")
            st.write("")
            calc_btn = st.button("Calculate", key="comb_btn")

        if calc_btn:
            n, r = int(n_val), int(r_val)
            if r > n:
                st.error("r cannot exceed n")
            else:
                p = math.perm(n, r)
                c = math.comb(n, r)
                st.markdown(f"""
                <div class='result-box' style='display:flex;gap:2rem;'>
                  <div>
                    <div style='color:#FF6B35;font-size:0.75rem;margin-bottom:0.3rem;'>P({n},{r})</div>
                    <div style='font-size:2rem;font-weight:700;'>{p:,}</div>
                    <div style='font-size:0.75rem;opacity:.7;'>{n}! / {n-r}!</div>
                  </div>
                  <div style='border-left:1px solid rgba(255,107,53,.2);padding-left:2rem;'>
                    <div style='color:#FFA060;font-size:0.75rem;margin-bottom:0.3rem;'>C({n},{r})</div>
                    <div style='font-size:2rem;font-weight:700;'>{c:,}</div>
                    <div style='font-size:0.75rem;opacity:.7;'>{n}! / ({r}! · {n-r}!)</div>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Pascal's triangle context row
                if n <= 15:
                    row = [math.comb(n, k) for k in range(n + 1)]
                    highlighted = "".join(
                        f"<span style='color:#FF6B35;font-weight:700;'>{v}</span>" if k == r else f"<span style='opacity:.6;'>{v}</span>"
                        for k, v in enumerate(row)
                    )
                    sep = "<span style='opacity:.3;'> · </span>"
                    st.markdown(f"<div class='formula'>Row n={n}: {sep.join(highlighted.split(' '))}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>THE PRINCIPLE</div>
          <div class='formula'>If n+1 objects are placed into n boxes, at least one box contains ≥ 2 objects</div>
          <p style='font-size:0.85rem;margin-top:0.5rem;'>
          Generalized: If N objects → k boxes, at least one box has ⌈N/k⌉ objects.
          </p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ph_n = st.number_input("Number of objects (N)", min_value=1, max_value=1000, value=13, key="ph_n")
        with col2:
            ph_k = st.number_input("Number of boxes (k)", min_value=1, max_value=100, value=12, key="ph_k")

        if st.button("Apply Pigeonhole", key="ph_btn"):
            n, k = int(ph_n), int(ph_k)
            guaranteed = math.ceil(n / k)
            st.markdown(f"""
            <div class='result-box'>
              <div style='color:#FF6B35;font-size:0.9rem;margin-bottom:0.5rem;'>
                Distributing <b>{n} objects</b> into <b>{k} boxes</b>:
              </div>
              <div class='formula'>⌈{n}/{k}⌉ = {guaranteed}</div>
              <p style='margin-top:0.5rem;'>
                At least one box must contain <b style='color:#FF6B35;'>{guaranteed}</b> or more objects.
              </p>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Classic Examples")
        examples = [
            ("Socks in drawer", "In a drawer with 12 red and 12 blue socks, how many to guarantee a matching pair?", "3 socks (2 colors → 3rd must match one)"),
            ("Birthday problem", "How many people to guarantee 2 share a birthday?", "367 (366 days → 367th must repeat)"),
            ("Cards in deck", "How many cards to guarantee 2 from the same suit?", "5 (4 suits → 5th repeats)"),
        ]
        for title, problem, answer in examples:
            with st.expander(f"🎯 {title}"):
                st.markdown(f"**Problem:** {problem}")
                st.markdown(f"**Answer:** {answer}")

    with tab3:
        principles = [
            ("Product Rule", "If task 1 can be done m ways and task 2 in n ways, both together: m × n ways", "Choosing outfit: 4 shirts × 3 pants = 12 combinations"),
            ("Sum Rule", "If task 1 can be done m ways OR task 2 in n ways (mutually exclusive): m + n ways", "Choose a fruit or vegetable: 5+7=12 choices"),
            ("Inclusion-Exclusion", "|A ∪ B| = |A| + |B| - |A ∩ B|", "Students in CS or Math: 30+25-10=45"),
        ]
        for name, rule, example in principles:
            st.markdown(f"""
            <div class='card'>
              <div class='sec-tag'>{name.upper()}</div>
              <div class='formula'>{rule}</div>
              <p style='font-size:0.82rem;'>Example: {example}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Inclusion-Exclusion Calculator")
        col1, col2, col3 = st.columns(3)
        with col1:
            ie_a = st.number_input("|A|", min_value=0, value=30, key="ie_a")
        with col2:
            ie_b = st.number_input("|B|", min_value=0, value=25, key="ie_b")
        with col3:
            ie_ab = st.number_input("|A ∩ B|", min_value=0, value=10, key="ie_ab")
        if st.button("Calculate |A ∪ B|", key="ie_btn"):
            result = int(ie_a) + int(ie_b) - int(ie_ab)
            st.markdown(f"<div class='formula'>|A ∪ B| = {int(ie_a)} + {int(ie_b)} − {int(ie_ab)} = {result}</div>", unsafe_allow_html=True)
