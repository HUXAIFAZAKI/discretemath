"""Graph Theory page."""

import streamlit as st
from utils.graph import graph_analyze


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_10-11 · GRAPH_THEORY</div>", unsafe_allow_html=True)
    st.markdown("## Graph Theory")

    tab1, tab2 = st.tabs(["🔍 Graph Analyzer", "📚 Graph Concepts"])

    with tab1:
        st.markdown("""
        <p style='font-size:0.85rem;'>
        Enter an adjacency matrix (space-separated rows). Each cell is 0 (no edge) or 1 (edge).
        The graph is treated as <b>undirected</b>.
        </p>""", unsafe_allow_html=True)

        default = "0 1 1 0\n1 0 1 1\n1 1 0 1\n0 1 1 0"
        matrix_input = st.text_area("Adjacency Matrix", default, height=120, key="graph_mat")

        if st.button("Analyze Graph", key="graph_analyze_btn"):
            try:
                rows = [list(map(int, r.split())) for r in matrix_input.strip().split("\n") if r.strip()]
                n = len(rows)
                for row in rows:
                    if len(row) != n:
                        raise ValueError("Matrix must be square")
                    for v in row:
                        if v not in (0, 1):
                            raise ValueError("Values must be 0 or 1")
                adj = rows
                result = graph_analyze(adj)

                badges = " ".join(
                    f"<span style='background:#FF6B35;color:#FFF5EE;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>{p}</span>"
                    for p in result.get("properties", [])
                ) if result.get("properties") else "<span style='opacity:.6;'>None detected</span>"

                deg_table = "".join(
                    f"<tr><td style='color:#FFA060;padding:3px 12px;'>v{i}</td><td style='color:#FF6B35;padding:3px 12px;'>{d}</td></tr>"
                    for i, d in enumerate(result["degrees"])
                )

                st.markdown(f"""
                <div class='result-box'>
                  <div style='display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:1rem;'>
                    <div><div style='font-size:0.75rem;opacity:.7;'>VERTICES</div><div style='font-size:1.8rem;font-weight:700;'>{result['vertices']}</div></div>
                    <div><div style='font-size:0.75rem;opacity:.7;'>EDGES</div><div style='font-size:1.8rem;font-weight:700;'>{result['edges']}</div></div>
                    <div><div style='font-size:0.75rem;opacity:.7;'>CONNECTED</div><div style='font-size:1.8rem;font-weight:700;'>{"Yes" if result["connected"] else "No"}</div></div>
                    <div><div style='font-size:0.75rem;opacity:.7;'>SUM OF DEGREES</div><div style='font-size:1.8rem;font-weight:700;'>{result["total_degree"]}</div></div>
                  </div>
                  <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.75rem;opacity:.7;margin-bottom:0.3rem;'>PROPERTIES</div>
                    {badges}
                  </div>
                  <div style='font-size:0.75rem;opacity:.7;margin-bottom:0.3rem;'>DEGREE SEQUENCE</div>
                  <table><tbody>{deg_table}</tbody></table>
                </div>""", unsafe_allow_html=True)

                # Handshaking lemma verification
                st.markdown(f"""
                <div class='formula'>
                Handshaking Lemma: Σdeg(v) = 2|E| → {result['total_degree']} = 2×{result['edges']} = {2*result['edges']}
                {"✓" if result['total_degree'] == 2 * result['edges'] else "✗"}
                </div>""", unsafe_allow_html=True)

                # Eulerian info
                st.markdown(f"<div class='result-box' style='margin-top:0.5rem;'>{result['eulerian']}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        concepts = [
            {
                "name": "Simple Graph",
                "def": "Undirected graph with no self-loops and no multiple edges.",
                "formula": "Max edges = n(n-1)/2 for n vertices",
            },
            {
                "name": "Complete Graph Kₙ",
                "def": "Every pair of vertices is connected by exactly one edge.",
                "formula": "Edges = n(n-1)/2, each vertex has degree n-1",
            },
            {
                "name": "Bipartite Graph",
                "def": "Vertices split into two sets V₁ and V₂; edges only between sets.",
                "formula": "A graph is bipartite iff it has no odd-length cycle",
            },
            {
                "name": "Euler Path & Circuit",
                "def": "Euler path: visits every edge once. Euler circuit: starts and ends at same vertex.",
                "formula": "Circuit: all vertices even degree. Path: exactly 2 vertices odd degree",
            },
            {
                "name": "Hamiltonian Path & Circuit",
                "def": "Visits every vertex exactly once.",
                "formula": "No simple necessary and sufficient condition (NP-complete)",
            },
            {
                "name": "Isomorphism",
                "def": "Two graphs G₁ and G₂ are isomorphic if there's a bijection f: V₁→V₂ preserving adjacency.",
                "formula": "Necessary: same |V|, |E|, and degree sequence",
            },
        ]
        cols = st.columns(2)
        for idx, c in enumerate(concepts):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>{c['name'].upper()}</div>
                  <p style='font-size:0.82rem;margin-bottom:0.4rem;'>{c['def']}</p>
                  <div class='formula' style='font-size:0.78rem;'>{c['formula']}</div>
                </div>""", unsafe_allow_html=True)
