"""Relations page."""

import streamlit as st
from utils.relations import (
    relation_properties, matrix_to_pairs, parse_pairs,
    reflexive_closure, symmetric_closure, transitive_closure,
    compose_relations, is_equivalence, equivalence_classes, is_partial_order,
)


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_04-08 · RELATIONS</div>", unsafe_allow_html=True)
    st.markdown("## Relations on Sets")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Property Checker", "🔀 Closures", "🔁 Composition",
        "≡ Equivalence Classes", "≤ Partial Orderings",
    ])

    with tab1:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>ORDERED_PAIRS · MATRIX_REPRESENTATION</div>
          <p style='font-size:0.85rem;'>
          A <b>binary relation</b> R on set A is a subset of A × A.
          Enter a <b>relation matrix</b> (0/1) to check all five properties.
          </p>
        </div>""", unsafe_allow_html=True)

        n_rel = st.slider("Set size n (elements: 0 to n-1)", 2, 6, 3, key="nrel")
        st.markdown(f"<div class='formula'>Relation R ⊆ {{{', '.join(str(i) for i in range(n_rel))}}} × {{{', '.join(str(i) for i in range(n_rel))}}}</div>", unsafe_allow_html=True)
        st.markdown("**Enter relation matrix (row i, col j = 1 means (i,j) ∈ R):**")

        matrix = []
        for i in range(n_rel):
            cols = st.columns(n_rel)
            row = []
            for j in range(n_rel):
                val = cols[j].selectbox(f"({i},{j})", [0, 1], key=f"rel_{i}_{j}")
                row.append(val)
            matrix.append(row)

        if st.button("🔍 Analyze Relation Properties", key="rel_run"):
            pairs = matrix_to_pairs(matrix)
            props = relation_properties(n_rel, pairs)

            st.markdown("**Pairs in R:** " + (str(pairs) if pairs else "∅ (empty relation)"))
            st.markdown("<div class='formula'>Domain: {" + ", ".join(str(a) for a, _ in pairs) + "} | Range: {" + ", ".join(str(b) for _, b in pairs) + "}</div>", unsafe_allow_html=True)

            explanations = {
                "Reflexive": "∀a ∈ A: (a,a) ∈ R — every element relates to itself",
                "Irreflexive": "∀a ∈ A: (a,a) ∉ R — no element relates to itself",
                "Symmetric": "∀a,b: (a,b) ∈ R → (b,a) ∈ R",
                "Antisymmetric": "∀a≠b: (a,b) ∈ R → (b,a) ∉ R",
                "Transitive": "∀a,b,c: (a,b),(b,c) ∈ R → (a,c) ∈ R",
            }
            html = "<table class='tt'><thead><tr><th>Property</th><th>Status</th><th>Explanation</th></tr></thead><tbody>"
            for prop, val in props.items():
                status = "✓ YES" if val else "✗ NO"
                cl = "T" if val else "F"
                html += f"<tr><td style='text-align:left;'>{prop}</td><td class='{cl}'>{status}</td><td style='font-size:0.72rem;text-align:left;opacity:.7;'>{explanations[prop]}</td></tr>"
            html += "</tbody></table>"
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

            is_eq = is_equivalence(n_rel, pairs)
            is_po = is_partial_order(n_rel, pairs)
            summary = []
            if is_eq:
                summary.append("✓ This is an EQUIVALENCE RELATION (reflexive + symmetric + transitive)")
            if is_po:
                summary.append("✓ This is a PARTIAL ORDER (reflexive + antisymmetric + transitive)")
            if not summary:
                summary.append("No special classification")
            for s in summary:
                st.info(s)

    with tab2:
        st.markdown("<div class='sec-tag'>CLOSURES · WARSHALL'S ALGORITHM</div>", unsafe_allow_html=True)
        st.markdown("""<p style='font-size:0.85rem;'>
        The <b>closure</b> of a relation is the smallest relation with a given property
        that contains the original relation.</p>""", unsafe_allow_html=True)

        n_cl = st.slider("Set size", 2, 5, 3, key="ncl")
        pairs_raw = st.text_input("Enter pairs as (i,j) comma-separated", "0,1 | 1,2 | 2,0", key="clpairs")

        if st.button("Compute Closures", key="cl_run"):
            pairs = parse_pairs(pairs_raw, n_cl)
            rc = reflexive_closure(n_cl, pairs)
            sc = symmetric_closure(pairs)
            tc = transitive_closure(n_cl, pairs)

            st.markdown(f"**Original R:** {pairs}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='card'><div class='sec-tag'>REFLEXIVE CLOSURE</div>
                  <div style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{rc}</div>
                  <div style='font-size:0.75rem;margin-top:0.5rem;opacity:.7;'>Added: {set(rc) - set(pairs)}</div></div>""",
                  unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='card'><div class='sec-tag'>SYMMETRIC CLOSURE</div>
                  <div style='color:#FFA060;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{sc}</div>
                  <div style='font-size:0.75rem;margin-top:0.5rem;opacity:.7;'>Added: {set(sc) - set(pairs)}</div></div>""",
                  unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class='card'><div class='sec-tag'>TRANSITIVE CLOSURE (Warshall)</div>
                  <div style='color:#FFA060;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{tc}</div>
                  <div style='font-size:0.75rem;margin-top:0.5rem;opacity:.7;'>Added: {set(tc) - set(pairs)}</div></div>""",
                  unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='sec-tag'>COMPOSITION OF RELATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='formula'>R₁ ∘ R₂ = {(a,c) | ∃b: (a,b) ∈ R₁ ∧ (b,c) ∈ R₂}</div>", unsafe_allow_html=True)

        n_comp = st.slider("Set size", 2, 5, 3, key="ncomp")
        r1_raw = st.text_input("Relation R₁ (pairs: a,b | a,b ...)", "0,1 | 1,2 | 0,2", key="r1raw")
        r2_raw = st.text_input("Relation R₂ (pairs: a,b | a,b ...)", "1,0 | 2,1", key="r2raw")

        if st.button("Compose R₁ ∘ R₂", key="comp_run"):
            r1 = parse_pairs(r1_raw, n_comp)
            r2 = parse_pairs(r2_raw, n_comp)
            composed = compose_relations(r1, r2)
            st.markdown(f"**R₁:** {r1}  |  **R₂:** {r2}")
            st.markdown(f"<div class='result-box'><span style='color:#FF6B35;'>R₁ ∘ R₂ = </span>{composed}</div>", unsafe_allow_html=True)
            steps = [
                f"({a},{b}) ∈ R₁ and ({b},{c}) ∈ R₂  →  ({a},{c}) ∈ R₁∘R₂"
                for (a, b) in r1 for (b2, c) in r2 if b == b2
            ]
            st.markdown("**Steps:**")
            for s in steps:
                st.markdown(f"- {s}")

    with tab4:
        st.markdown("<div class='sec-tag'>EQUIVALENCE CLASSES</div>", unsafe_allow_html=True)
        st.markdown("""<p style='font-size:0.85rem;'>
        An <b>equivalence relation</b> is reflexive, symmetric, and transitive.
        It partitions the set into disjoint <b style='color:#FF6B35;'>equivalence classes</b>.</p>""",
        unsafe_allow_html=True)
        st.markdown("<div class='formula'>A / R = {[a] | a ∈ A} where [a] = {b ∈ A | aRb}</div>", unsafe_allow_html=True)

        n_eq = st.slider("Set size", 2, 8, 4, key="neq")
        eq_raw = st.text_input("Relation R (pairs: a,b | ...)",
                               "0,0 | 1,1 | 2,2 | 3,3 | 0,1 | 1,0 | 2,3 | 3,2", key="eqraw")

        if st.button("Find Equivalence Classes", key="eq_run"):
            pairs = parse_pairs(eq_raw, n_eq)
            if is_equivalence(n_eq, pairs):
                classes = equivalence_classes(n_eq, pairs)
                st.success("✓ This IS an equivalence relation")
                html = f"<div style='color:#FF6B35;margin-bottom:0.6rem;font-size:0.75rem;'>A/R has {len(classes)} equivalence class(es):</div>"
                for root, members in classes.items():
                    rep = members[0]
                    html += f"<div style='margin-bottom:0.4rem;'><span style='color:#FF6B35;'>[{rep}]</span> = {{{', '.join(str(m) for m in members)}}}</div>"
                st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)
            else:
                props = relation_properties(n_eq, pairs)
                missing = [k for k, v in props.items() if not v and k in ("Reflexive", "Symmetric", "Transitive")]
                st.error(f"✗ NOT an equivalence relation. Missing: {', '.join(missing)}")

    with tab5:
        st.markdown("<div class='sec-tag'>PARTIAL ORDERINGS (POSET)</div>", unsafe_allow_html=True)
        st.markdown("""<p style='font-size:0.85rem;'>
        A <b>partial order</b> is reflexive, antisymmetric, and transitive.
        The pair (A, R) is called a <b style='color:#FF6B35;'>partially ordered set (POSET)</b>.</p>""",
        unsafe_allow_html=True)
        st.markdown("<div class='formula'>Poset (A, ≤) satisfies: reflexive + antisymmetric + transitive</div>", unsafe_allow_html=True)

        n_po = st.slider("Set size", 2, 6, 4, key="npo")
        po_raw = st.text_input("Relation R",
                               "0,0 | 1,1 | 2,2 | 3,3 | 0,1 | 0,2 | 0,3 | 1,3 | 2,3", key="poraw")

        if st.button("Check Partial Order", key="po_run"):
            pairs = parse_pairs(po_raw, n_po)
            if is_partial_order(n_po, pairs):
                st.success("✓ This IS a Partial Order (POSET)")
                elements = list(range(n_po))
                has_predecessor = {b for (a, b) in pairs if a != b}
                has_successor   = {a for (a, b) in pairs if a != b}
                minimal = [e for e in elements if e not in has_predecessor]
                maximal = [e for e in elements if e not in has_successor]
                st.markdown(f"""
                <div class='result-box'>
                  <div style='color:#FF6B35;'>Minimal elements: {minimal}</div>
                  <div style='color:#FFA060;margin-top:0.4rem;'>Maximal elements: {maximal}</div>
                  <div style='font-size:0.72rem;margin-top:0.4rem;opacity:.7;'>
                    Comparable pairs: {[(a,b) for (a,b) in pairs if a != b]}
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                props = relation_properties(n_po, pairs)
                missing = [k for k, v in props.items() if not v and k in ("Reflexive", "Antisymmetric", "Transitive")]
                st.error(f"✗ NOT a partial order. Missing: {', '.join(missing)}")
