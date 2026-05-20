"""
Discrete Academy - main entry point.
Orchestrates all page modules; do NOT add page logic here.
"""

import streamlit as st
from styles.theme import NAV_PAGES, inject_css, render_nav, render_footer
from pages import home, sets, relations, logic, inference, proofs, induction, sequences, combinatorics, graphs, ai_solver
from study.study_mode import render as render_study

st.set_page_config(
    page_title="Discrete Academy — Logic & Mathematics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme from URL param (persists via link sharing)
theme = st.query_params.get("theme", "dark")
if theme not in ("dark", "light"):
    theme = "dark"
st.session_state["theme"] = theme

section = st.query_params.get("page", "home")
valid_keys = {k for k, *_ in NAV_PAGES}
if section not in valid_keys:
    section = "home"

inject_css(theme)
render_nav(section, theme)

PAGES = {
    "home":          home.render,
    "sets":          sets.render,
    "relations":     relations.render,
    "logic":         logic.render,
    "inference":     inference.render,
    "proofs":        proofs.render,
    "induction":     induction.render,
    "sequences":     sequences.render,
    "combinatorics": combinatorics.render,
    "graphs":        graphs.render,
    "ai":            ai_solver.render,
    "study":         render_study,
}

PAGES.get(section, home.render)()

render_footer()
