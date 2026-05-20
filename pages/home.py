"""Home page."""

import streamlit as st


def render() -> None:
    st.markdown("""
    <div class='hero-wrapper'>
      <div class='hero-glow'></div>
      <div class='hero-glow-2'></div>
      <div class='hero-inner'>
        <div class='hero-eyebrow'>DISCRETE MATHEMATICS · MADE APPROACHABLE</div>
        <div class='hero-title'>
          Learn to Think<br><em>Like a Computer Scientist</em>
        </div>
        <p class='hero-sub'>
          From sets and logic to proofs and graphs —
          master the mathematical foundations that power every algorithm,
          database, and AI system ever built.
          Interactive tools · AI solver · Progress tracking.
        </p>
        <div class='hero-stats'>
          <div class='hero-stat'>
            <span class='hero-stat-num'>11</span>
            <span class='hero-stat-label'>Topics</span>
          </div>
          <div class='hero-stat-sep'>&middot;</div>
          <div class='hero-stat'>
            <span class='hero-stat-num'>9</span>
            <span class='hero-stat-label'>Quizzes</span>
          </div>
          <div class='hero-stat-sep'>&middot;</div>
          <div class='hero-stat'>
            <span class='hero-stat-num'>∞</span>
            <span class='hero-stat-label'>Practice</span>
          </div>
          <div class='hero-stat-sep'>&middot;</div>
          <div class='hero-stat'>
            <span class='hero-stat-num'>AI</span>
            <span class='hero-stat-label'>Solver</span>
          </div>
          <div class='hero-stat-sep'>&middot;</div>
          <div class='hero-stat'>
            <span class='hero-stat-num'>📊</span>
            <span class='hero-stat-label'>Progress</span>
          </div>
        </div>
        <div class='hero-symbols'>∧ &middot; ∨ &middot; ∀ &middot; ∃ &middot; ∩ &middot; ∪ &middot; ⊆ &middot; ∴ &middot; ∑ &middot; ⟹</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Study Mode CTA
    st.markdown("""
    <div class='cta-banner'>
      <div style='font-size:2.2rem;'>&#128218;</div>
      <div>
        <div style='font-family:"Syne",sans-serif;font-size:1.05rem;font-weight:800;color:#FF6B35;margin-bottom:.3rem;'>
          Your Personal Study Hub
        </div>
        <div style='font-size:.86rem;color:#9E9890;'>
          Track your progress, follow the structured learning roadmap, take quizzes,
          and work through practice problems — all in one place.
          <a href='?page=study' target='_self' style='color:#FF6B35;text-decoration:none;margin-left:.4rem;font-weight:600;'>
            Open Study Hub →
          </a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sec-tag'>// COURSE OUTLINE — WHAT YOU'LL EXPLORE</div>
    <h3 style='margin-bottom:1.2rem;'>From Zero to Proof</h3>
    """, unsafe_allow_html=True)

    topics = [
        ("Sets & Venn Diagrams",    "W2–3",  "∩",
         "Understand collections, membership, union, intersection, and the powerful De Morgan laws through visual Venn diagrams."),
        ("Relations on Sets",       "W4–5",  "↔",
         "Explore ordered pairs, Cartesian products, and how to represent relations as matrices, arrow diagrams, and directed graphs."),
        ("Types of Relations",      "W6–7",  "⇄",
         "Identify reflexive, symmetric, antisymmetric, and transitive relations — building blocks of equivalence and order."),
        ("Closures & Orders",       "W8",         "≤",
         "Compute transitive closures with Warshall’s algorithm, understand equivalence classes, and explore partial orderings."),
        ("Propositional Logic",     "W9–10", "∧",
         "Build truth tables, identify tautologies, and master logical connectives — the language of computation."),
        ("Predicates & Quantifiers","W10–11","∀",
         "Move beyond propositions to statements with variables using ∀ and ∃ — the heart of mathematical reasoning."),
        ("Rules of Inference",      "W12–13","∴",
         "Apply Modus Ponens, Modus Tollens, and other inference rules to construct valid logical arguments."),
        ("Proof Methods",           "W14–15","□",
         "Master direct proofs, proof by contradiction, contrapositive, and exhaustive case analysis."),
        ("Mathematical Induction",  "W16",        "∑",
         "Prove statements for all natural numbers using the powerful two-step induction principle."),
        ("Combinatorics",           "+",          "⊕",
         "Count arrangements and selections with permutations, combinations, and the Pigeonhole Principle."),
        ("Graph Theory",            "+",          "◇",
         "Model networks with vertices and edges. Find Euler paths, spanning trees, and solve real-world graph problems."),
    ]

    theme = st.session_state.get('theme', 'dark')
    title_color = '#1C1714' if theme == 'light' else '#F2EDE6'
    cols = st.columns(3)
    for idx, (title, week, icon, desc) in enumerate(topics):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='topic-card' style='animation-delay:{idx*0.05:.2f}s;'>
              <div style='display:flex;align-items:center;gap:.7rem;margin-bottom:.5rem;'>
                <span style='font-size:1.1rem;'>{icon}</span>
                <div>
                  <div style='font-family:"Space Grotesk",sans-serif;font-size:.9rem;font-weight:700;color:{title_color};'>{title}</div>
                  <div style='font-family:"JetBrains Mono",monospace;font-size:.6rem;color:#FF6B35;letter-spacing:.08em;'>{week}</div>
                </div>
              </div>
              <p style='color:#9E9890;font-size:.8rem;line-height:1.6;margin:0;'>{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div class='sec-tag'>// WHAT MAKES THIS DIFFERENT</div>
    <h3 style='margin-bottom:1.2rem;'>Built for Deep Understanding</h3>
    """, unsafe_allow_html=True)

    features = [
        ("⚡", "AI Problem Solver",    "Type any discrete math problem in plain English and get a step-by-step solution powered by AI."),
        ("🧠", "Interactive Tools",   "Compute truth tables, visualize graphs, check relation properties — all live in your browser."),
        ("📊", "Progress Tracking",   "Your personal learning dashboard tracks every topic, quiz score, and practice session."),
        ("🗺️", "Learning Roadmap", "Follow a structured path from foundations to advanced topics with clear milestones."),
    ]
    cols2 = st.columns(4)
    for i, (ic, title, desc) in enumerate(features):
        with cols2[i]:
            st.markdown(f"""
            <div class='card' style='text-align:center;animation-delay:{i*0.08:.2f}s;'>
              <div style='font-size:1.8rem;margin-bottom:.6rem;'>{ic}</div>
              <div style='font-family:"Syne",sans-serif;font-size:.92rem;font-weight:700;color:{title_color};margin-bottom:.4rem;'>{title}</div>
              <p style='color:#9E9890;font-size:.78rem;line-height:1.58;margin:0;'>{desc}</p>
            </div>""", unsafe_allow_html=True)
