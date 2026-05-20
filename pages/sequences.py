"""Sequences & Summations page."""

import streamlit as st


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_08 · SEQUENCES_AND_SUMMATIONS</div>", unsafe_allow_html=True)
    st.markdown("## Sequences & Summations")

    tab1, tab2 = st.tabs(["📊 Sequence Generator", "∑ Summation Formulas"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            seq_type = st.selectbox("Sequence type", ["arithmetic", "geometric", "fibonacci"])
            n_terms = st.number_input("Number of terms (n)", min_value=1, max_value=25, value=8, key="seq_n")
        with col2:
            a0 = 1
            d = r = 3
            if seq_type == "arithmetic":
                a0 = st.number_input("First term a₁", value=1, key="ar_a")
                d = st.number_input("Common difference d", value=3, key="ar_d")
            elif seq_type == "geometric":
                a0 = st.number_input("First term a₁", value=1, key="ge_a")
                r = st.number_input("Common ratio r", value=2, key="ge_r")

        if st.button("Generate Sequence", key="seq_run"):
            n = int(n_terms)
            if seq_type == "arithmetic":
                terms = [int(a0) + i * int(d) for i in range(n)]
                s = sum(terms)
                formula = f"S_n = n/2·(2a+(n-1)d) = {n}/2·(2·{int(a0)}+{n-1}·{int(d)}) = {s}"
                nth = f"a_n = {int(a0)} + (n-1)·{int(d)}"
            elif seq_type == "geometric":
                terms = [int(a0) * (int(r) ** i) for i in range(n)]
                s = sum(terms)
                if int(r) != 1:
                    formula = f"S_n = a(rⁿ-1)/(r-1) = {int(a0)}·({int(r)}^{n}-1)/({int(r)}-1) = {s}"
                else:
                    formula = f"S_n = n·a = {n}·{int(a0)} = {s}"
                nth = f"a_n = {int(a0)}·{int(r)}^(n-1)"
            else:
                fibs = [1, 1]
                while len(fibs) < n:
                    fibs.append(fibs[-1] + fibs[-2])
                terms = fibs[:n]
                s = sum(terms)
                formula = f"Sum of F_1..F_{n} = {s}"
                nth = "F_n = F_(n-1) + F_(n-2)"

            st.markdown(f"<div class='formula'>{nth}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='result-box'>
              <div style='color:#FF6B35;margin-bottom:0.4rem;'>Terms:</div>
              <div style='margin-bottom:0.8rem;word-break:break-all;'>{', '.join(str(t) for t in terms)}</div>
              <div style='color:#FF6B35;margin-bottom:0.4rem;'>Sum:</div>
              <div style='font-size:1rem;font-weight:700;margin-bottom:0.4rem;'>{s}</div>
              <div style='font-size:0.78rem;opacity:.7;'>{formula}</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        formulas = [
            ("Sum of 1 to n", "Σᵢ₌₁ⁿ i", "n(n+1)/2", "10 → 55"),
            ("Sum of squares", "Σᵢ₌₁ⁿ i²", "n(n+1)(2n+1)/6", "5 → 55"),
            ("Sum of cubes", "Σᵢ₌₁ⁿ i³", "[n(n+1)/2]²", "4 → 100"),
            ("Sum of odd numbers", "Σᵢ₌₁ⁿ (2i-1)", "n²", "5 → 25"),
            ("Geometric series", "Σᵢ₌₀ⁿ rⁱ", "(r^(n+1) - 1)/(r-1)", "r=2,n=4 → 31"),
            ("Infinite geometric", "Σᵢ₌₀^∞ rⁱ  |r|<1", "1/(1-r)", "r=0.5 → 2"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th>Name</th><th>Notation</th><th>Formula</th><th>Example</th></tr></thead><tbody>"
        for name, notation, formula, example in formulas:
            html += f"<tr><td class='T' style='text-align:left'>{name}</td><td>{notation}</td><td style='color:#FF6B35'>{formula}</td><td style='opacity:.7;'>{example}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Compute Σᵢ₌₁ⁿ iᵏ")
        col1, col2 = st.columns(2)
        with col1:
            sum_n = st.number_input("n (upper limit)", 1, 100, 10, key="sumn")
        with col2:
            sum_k = st.number_input("k (power)", 0, 5, 1, key="sumk")
        if st.button("Compute", key="sum_run"):
            result = sum(i ** int(sum_k) for i in range(1, int(sum_n) + 1))
            st.markdown(f"<div class='formula'>Σᵢ₌₁^{int(sum_n)} i^{int(sum_k)} = {result}</div>", unsafe_allow_html=True)
