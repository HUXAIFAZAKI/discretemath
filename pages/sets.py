"""Set Theory page."""

import math
import streamlit as st
from utils.sets import parse_set, fmt_set, compute_set_ops


def render() -> None:
    st.markdown("<div class='sec-tag'>// WEEK_02-03 · SET_THEORY</div>", unsafe_allow_html=True)
    st.markdown("## Set Theory & Venn Diagrams")
    st.markdown("""
    <p style='font-size:0.85rem;'>
    A <b>set</b> is an unordered collection of distinct objects.
    Set operations are the foundation of logic, databases, and AI.
    </p>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚙️ Set Calculator", "🔵 Venn Visualizer", "📖 Set Identities"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            set_a_raw = st.text_input("Set A (comma-separated)", "1, 2, 3, 4, 5", key="sa")
            set_b_raw = st.text_input("Set B (comma-separated)", "3, 4, 5, 6, 7", key="sb")
            set_c_raw = st.text_input("Set C (optional, for 3-set ops)", "", key="sc")
        with col2:
            universe_raw = st.text_input("Universal Set U (optional)", "1,2,3,4,5,6,7,8,9,10", key="su")

        if st.button("🔢 Compute All Set Operations", key="set_run"):
            A = parse_set(set_a_raw)
            B = parse_set(set_b_raw)
            U = parse_set(universe_raw) if universe_raw.strip() else list(set(A + B))
            ops = compute_set_ops(A, B, U)
            cart = ops["cartesian"]

            ie = len(ops["intersection"])
            st.markdown(
                f"<div class='formula'>|A ∪ B| = |A| + |B| − |A ∩ B| = {len(A)} + {len(B)} − {ie} = {len(ops['union'])}</div>",
                unsafe_allow_html=True
            )

            results = [
                ("A", fmt_set(A), f"|A| = {len(A)}"),
                ("B", fmt_set(B), f"|B| = {len(B)}"),
                ("A ∪ B", fmt_set(ops["union"]), f"|A ∪ B| = {len(ops['union'])}"),
                ("A ∩ B", fmt_set(ops["intersection"]), f"|A ∩ B| = {len(ops['intersection'])}"),
                ("A − B", fmt_set(ops["diff_ab"]), f"|A − B| = {len(ops['diff_ab'])}"),
                ("B − A", fmt_set(ops["diff_ba"]), f"|B − A| = {len(ops['diff_ba'])}"),
                ("A △ B", fmt_set(ops["sym_diff"]), "Symmetric difference"),
                ("Ā (comp. A)", fmt_set(ops["comp_a"]), "Elements in U but not A"),
                ("B̄ (comp. B)", fmt_set(ops["comp_b"]), "Elements in U but not B"),
                ("A × B", str(cart[:10]) + ("..." if len(cart) > 10 else ""), f"|A × B| = {len(cart)}"),
            ]
            html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Operation</th><th style='text-align:left'>Result</th><th style='text-align:left'>Note</th></tr></thead><tbody>"
            for op, res, note in results:
                html += f"<tr><td class='T' style='text-align:left;padding-right:1rem'>{op}</td><td>{res}</td><td style='font-size:0.72rem;opacity:.7;'>{note}</td></tr>"
            html += "</tbody></table>"
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

            if set_c_raw.strip():
                C = parse_set(set_c_raw)
                Cs = set(C)
                inter3 = [x for x in ops["intersection"] if x in Cs]
                union3 = list(set(A + B + C))
                st.info(f"**3-Set:** A ∩ B ∩ C = {fmt_set(inter3)} | A ∪ B ∪ C = {fmt_set(union3)}")

    with tab2:
        st.markdown("""
        <div class='sec-tag'>VENN_VISUALIZER · MULTI-SET</div>
        <p style='font-size:0.85rem;margin-bottom:1.2rem;'>
        Build Venn diagrams for 2, 3, or 4 sets. Every region is labelled with its elements.
        </p>""", unsafe_allow_html=True)

        n_sets = st.radio("Number of sets:", [2, 3, 4], horizontal=True, key="venn_n")
        _set_defaults = {
            "A": "Ali, Sara, Mustafa, Farhan, Zain",
            "B": "Sara, Ahmed, Bilal, Mustafa, Huzaifa",
            "C": "Farhan, Ahmed, Kasim, Mustafa, Bilal",
            "D": "Zain, Tariq, Kasim, Ahmed, Laiba",
        }
        _set_names = ["A", "B", "C", "D"][:n_sets]
        _vcols = st.columns(n_sets)
        _raw_v = {}
        for _i, _sn in enumerate(_set_names):
            with _vcols[_i]:
                _raw_v[_sn] = st.text_input(f"Set {_sn}", _set_defaults[_sn], key=f"venn_s{_sn}")

        if st.button("Generate Venn Diagram", key="venn_run"):
            try:
                import matplotlib.pyplot as plt
                import numpy as np

                _parsed_v = {n: parse_set(_raw_v[n]) for n in _set_names}
                _as_sets  = {n: set(e) for n, e in _parsed_v.items()}

                def _region_elems(mask):
                    in_i  = [i for i in range(n_sets) if mask & (1 << i)]
                    out_i = [i for i in range(n_sets) if not (mask & (1 << i))]
                    els = _as_sets[_set_names[in_i[0]]].copy()
                    for i in in_i[1:]:
                        els &= _as_sets[_set_names[i]]
                    for i in out_i:
                        els -= _as_sets[_set_names[i]]
                    return sorted(els, key=str)

                _regions = {}
                for _mask in range(1, 2**n_sets):
                    _in = [_set_names[i] for i in range(n_sets) if _mask & (1 << i)]
                    _label = " ∩ ".join(_in) + (" only" if len(_in) < n_sets else "")
                    _regions[_mask] = (_label, _region_elems(_mask))

                _c_palette = ['#FF6B35', '#FFA060', '#38BDF8', '#F472B6']
                _html_rows = ""
                for _mask in sorted(_regions.keys()):
                    _lbl, _els = _regions[_mask]
                    _in_i = [i for i in range(n_sets) if _mask & (1 << i)]
                    _col  = _c_palette[_in_i[0]] if len(_in_i) == 1 else '#FFA060'
                    _html_rows += (
                        f"<tr><td style='color:{_col};text-align:left;padding-right:1rem'>{_lbl}</td>"
                        f"<td>{fmt_set(_els)}</td>"
                        f"<td style='font-size:0.7rem;opacity:.7;'>{len(_els)}</td></tr>"
                    )
                st.markdown(
                    f"<div class='result-box'><table class='tt' style='width:100%;'>"
                    f"<thead><tr><th style='text-align:left'>Region</th>"
                    f"<th style='text-align:left'>Elements</th>"
                    f"<th style='text-align:left'>|n|</th></tr></thead>"
                    f"<tbody>{_html_rows}</tbody></table></div>",
                    unsafe_allow_html=True
                )

                def _in_ellipse(XX, YY, cx, cy, a, b, theta=0.0):
                    ct, st_ = np.cos(theta), np.sin(theta)
                    Xr = (XX - cx) * ct + (YY - cy) * st_
                    Yr = -(XX - cx) * st_ + (YY - cy) * ct
                    return (Xr / a)**2 + (Yr / b)**2 <= 1.0

                def _fit_text(elements, max_items=7, line_width=13):
                    if not elements:
                        return '∅'
                    shown = [str(e)[:9] for e in elements[:max_items]]
                    extra = len(elements) - max_items
                    lines, buf = [], []
                    for e in shown:
                        buf.append(e)
                        if len(', '.join(buf)) >= line_width:
                            lines.append(', '.join(buf[:-1]))
                            buf = [buf[-1]]
                    if buf:
                        lines.append(', '.join(buf))
                    result = '\n'.join(l for l in lines if l)
                    if extra > 0:
                        result += f'\n(+{extra})'
                    return result

                W, H = 900, 580
                x_min, x_max, y_min, y_max = 0.0, 10.0, 0.0, 7.5
                xs_arr = np.linspace(x_min, x_max, W)
                ys_arr = np.linspace(y_min, y_max, H)
                XX, YY = np.meshgrid(xs_arr, ys_arr)

                if n_sets == 2:
                    _geom = [(3.5, 3.75, 2.3, 2.3, 0.0), (6.5, 3.75, 2.3, 2.3, 0.0)]
                    _lbl_off = [(-0.2, 0.3), (0.2, 0.3)]
                elif n_sets == 3:
                    _geom = [(3.2, 2.8, 2.45, 2.45, 0.0), (6.8, 2.8, 2.45, 2.45, 0.0), (5.0, 5.6, 2.45, 2.45, 0.0)]
                    _lbl_off = [(-0.3, -0.1), (0.3, -0.1), (0.0, 0.4)]
                else:
                    _geom = [
                        (3.5, 4.2, 2.8, 1.5,  math.pi * 0.25),
                        (6.5, 4.2, 2.8, 1.5, -math.pi * 0.25),
                        (3.5, 3.2, 2.8, 1.5, -math.pi * 0.25),
                        (6.5, 3.2, 2.8, 1.5,  math.pi * 0.25),
                    ]
                    _lbl_off = [(-0.4, 0.6), (0.4, 0.6), (-0.4, -0.6), (0.4, -0.6)]

                _cmasks = [_in_ellipse(XX, YY, *g) for g in _geom]
                _img = np.zeros((H, W, 4), dtype=float)
                _rgb_sets = [
                    (255/255, 107/255,  53/255),  # #FF6B35 orange
                    (255/255, 160/255,  96/255),  # #FFA060 lt-orange
                    ( 56/255, 189/255, 248/255),  # #38BDF8 sky-blue
                    (244/255, 114/255, 182/255),  # #F472B6 pink
                ]
                for _mask in range(1, 2**n_sets):
                    _in_i = [i for i in range(n_sets) if _mask & (1 << i)]
                    _rm = _cmasks[_in_i[0]].copy()
                    for i in _in_i[1:]:
                        _rm &= _cmasks[i]
                    for i in range(n_sets):
                        if not (_mask & (1 << i)):
                            _rm &= ~_cmasks[i]
                    if not _rm.any():
                        continue
                    rr = sum(_rgb_sets[i][0] for i in _in_i) / len(_in_i)
                    gg = sum(_rgb_sets[i][1] for i in _in_i) / len(_in_i)
                    bb = sum(_rgb_sets[i][2] for i in _in_i) / len(_in_i)
                    aa = min(0.38 + 0.1 * (len(_in_i) - 1), 0.78)
                    _img[_rm] = [rr, gg, bb, aa]

                _bg = '#060504' if st.session_state.get('theme', 'dark') == 'dark' else '#F5F1EC'
                fig, ax = plt.subplots(figsize=(10, 6.5))
                fig.patch.set_facecolor(_bg)
                ax.set_facecolor(_bg)
                ax.imshow(_img, extent=[x_min, x_max, y_min, y_max],
                          origin='lower', aspect='auto', interpolation='bilinear')

                _theta = np.linspace(0, 2 * math.pi, 500)
                _ec = ['#FF6B35', '#FFA060', '#38BDF8', '#F472B6']
                for i, (cx, cy, a, b, ang) in enumerate(_geom):
                    ct, st_ = np.cos(ang), np.sin(ang)
                    ex = cx + a * np.cos(_theta) * ct - b * np.sin(_theta) * st_
                    ey = cy + a * np.cos(_theta) * st_ + b * np.sin(_theta) * ct
                    ax.plot(ex, ey, color=_ec[i], linewidth=2.0, alpha=0.9)
                    ox, oy = _lbl_off[i]
                    lx = cx + ox
                    ly = cy + b + 0.35 + oy if ang == 0 else cy + max(a, b) * 0.7 + oy
                    ax.text(lx, ly, _set_names[i], color=_ec[i],
                            fontsize=18, fontweight='bold', ha='center', va='bottom',
                            fontfamily='monospace')

                for _mask in range(1, 2**n_sets):
                    _in_i = [i for i in range(n_sets) if _mask & (1 << i)]
                    _rm = _cmasks[_in_i[0]].copy()
                    for i in _in_i[1:]:
                        _rm &= _cmasks[i]
                    for i in range(n_sets):
                        if not (_mask & (1 << i)):
                            _rm &= ~_cmasks[i]
                    if not _rm.any():
                        continue
                    ys_px, xs_px = np.where(_rm)
                    cx_t = xs_arr[int(np.clip(np.mean(xs_px), 0, W - 1))]
                    cy_t = ys_arr[int(np.clip(np.mean(ys_px), 0, H - 1))]
                    _, _els = _regions[_mask]
                    _txt = _fit_text(_els)
                    _venn_text = '#F2EDE6' if st.session_state.get('theme','dark')=='dark' else '#1C1714'
                    _tcol = _ec[_in_i[0]] if len(_in_i) == 1 else _venn_text
                    _fs   = 7.5 if n_sets <= 3 else 6.5
                    ax.text(cx_t, cy_t, _txt, color=_tcol, fontsize=_fs,
                            ha='center', va='center', fontfamily='monospace', linespacing=1.5,
                            bbox=dict(facecolor='none', edgecolor='none'))

                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min - 0.2, y_max + 0.2)
                ax.axis('off')
                ax.set_title(
                    f'{n_sets}-Set Venn Diagram  ·  '
                    + ' · '.join(f'{n}={len(_parsed_v[n])}' for n in _set_names),
                    color='#9E9890', fontsize=10, pad=10, fontfamily='monospace'
                )
                plt.tight_layout(pad=0.4)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            except ImportError:
                st.info("Install matplotlib (`pip install matplotlib`) for the visual Venn diagram.")

    with tab3:
        st.markdown("""
        <div class='sec-tag'>SET_IDENTITIES</div>
        <h4 style='margin-bottom:1rem;'>Fundamental Set Laws</h4>
        """, unsafe_allow_html=True)
        identities = [
            ("Commutative", "A ∪ B = B ∪ A", "A ∩ B = B ∩ A"),
            ("Associative", "A ∪ (B ∪ C) = (A ∪ B) ∪ C", "A ∩ (B ∩ C) = (A ∩ B) ∩ C"),
            ("Distributive", "A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)", "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)"),
            ("Identity", "A ∪ ∅ = A", "A ∩ U = A"),
            ("Complement", "A ∪ Ā = U", "A ∩ Ā = ∅"),
            ("De Morgan's", "(A ∪ B)' = A' ∩ B'", "(A ∩ B)' = A' ∪ B'"),
            ("Idempotent", "A ∪ A = A", "A ∩ A = A"),
            ("Double Complement", "Ā̄ = A", "—"),
            ("Domination", "A ∪ U = U", "A ∩ ∅ = ∅"),
            ("Absorption", "A ∪ (A ∩ B) = A", "A ∩ (A ∪ B) = A"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th>Law</th><th>Union Form</th><th>Intersection Form</th></tr></thead><tbody>"
        for law, f1, f2 in identities:
            html += f"<tr><td class='T' style='text-align:left'>{law}</td><td style='color:#FF6B35'>{f1}</td><td style='color:#FFA060'>{f2}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)
