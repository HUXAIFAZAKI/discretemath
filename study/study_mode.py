"""Study Hub — coordinator with progress tracking, roadmap, and study sessions."""

import streamlit as st
from study.content import TOPICS, EXPLANATIONS
from study.quizzes import QUIZZES
from study.problem_sets import PROBLEM_SETS

# ---------------------------------------------------------------------------
# Learning roadmap definition
# ---------------------------------------------------------------------------
ROADMAP = [
    {
        "phase": "Foundations",
        "nodes": [
            {"key": "Set Theory",           "icon": "∩", "week": "W2–3"},
            {"key": "Combinatorics",         "icon": "⊕", "week": "+"},
        ],
    },
    {
        "phase": "Relationships",
        "nodes": [
            {"key": "Relations",             "icon": "↔", "week": "W4–8"},
            {"key": "Sequences & Summations","icon": "≋", "week": "W8"},
        ],
    },
    {
        "phase": "Logic & Reasoning",
        "nodes": [
            {"key": "Propositional Logic",   "icon": "∧", "week": "W9–11"},
            {"key": "Rules of Inference",    "icon": "∴", "week": "W12–13"},
        ],
    },
    {
        "phase": "Proof Techniques",
        "nodes": [
            {"key": "Proof Methods",         "icon": "□", "week": "W14–15"},
            {"key": "Mathematical Induction","icon": "∑", "week": "W16"},
        ],
    },
    {
        "phase": "Advanced Topics",
        "nodes": [
            {"key": "Graph Theory",          "icon": "◇", "week": "+"},
        ],
    },
]

ACHIEVEMENTS = [
    ("First Step",      "Complete any explain",        lambda e, q, p: len(e) >= 1),
    ("Quiz Taker",      "Take your first quiz",        lambda e, q, p: len(q) >= 1),
    ("Half Way",        "Complete 5 topics",           lambda e, q, p: len(e) >= 5),
    ("Quiz Master",     "Score 100% on any quiz",      lambda e, q, p: any(v == 100 for v in q.values())),
    ("Practice Pro",    "Complete 3 practice sets",    lambda e, q, p: len(p) >= 3),
    ("Graduate",        "Cover all 9 topics",          lambda e, q, p: len(e) >= 9),
]

# ---------------------------------------------------------------------------
# Progress helpers
# ---------------------------------------------------------------------------
def _init_progress() -> None:
    if "prog_explained" not in st.session_state:
        st.session_state["prog_explained"] = set()
    if "prog_quiz" not in st.session_state:
        st.session_state["prog_quiz"] = {}
    if "prog_practice" not in st.session_state:
        st.session_state["prog_practice"] = set()


def _mark_explained(topic: str) -> None:
    st.session_state["prog_explained"].add(topic)


def _update_quiz_score(topic: str, pct: int) -> None:
    current = st.session_state["prog_quiz"].get(topic, 0)
    st.session_state["prog_quiz"][topic] = max(current, pct)


def _mark_practiced(topic: str) -> None:
    st.session_state["prog_practice"].add(topic)


def _topic_completion(topic: str) -> float:
    """Return fraction 0–1 for a single topic (out of 3 activities)."""
    done = 0
    if topic in st.session_state.get("prog_explained", set()):
        done += 1
    if st.session_state.get("prog_quiz", {}).get(topic, 0) > 0:
        done += 1
    if topic in st.session_state.get("prog_practice", set()):
        done += 1
    return done / 3


def _topic_status(topic: str) -> str:
    frac = _topic_completion(topic)
    if frac >= 1.0:
        return "mastered"
    if frac > 0:
        return "in-progress"
    return "new"


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def _render_progress_dashboard() -> None:
    theme = st.session_state.get("theme", "dark")
    title_c = "#1C1714" if theme == "light" else "#F2EDE6"
    explained = st.session_state.get("prog_explained", set())
    quiz_scores = st.session_state.get("prog_quiz", {})
    practiced = st.session_state.get("prog_practice", set())

    total = len(TOPICS)
    total_acts = total * 3
    done_acts = len(explained) + len([s for s in quiz_scores.values() if s > 0]) + len(practiced)
    overall_pct = int(done_acts / total_acts * 100) if total_acts else 0

    best_quiz = max(quiz_scores.values(), default=0)
    avg_quiz  = int(sum(quiz_scores.values()) / len(quiz_scores)) if quiz_scores else 0

    # Top stats
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{overall_pct}%", "Overall Progress"),
        (str(len(explained)), f"Topics Explored / {total}"),
        (str(len(quiz_scores)), "Quizzes Taken"),
        (f"{best_quiz}%", "Best Quiz Score"),
    ]
    for col, (num, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class='stat-box'>
              <div class='stat-box-num'>{num}</div>
              <div class='stat-box-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    # Overall progress bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='margin-bottom:.4rem;display:flex;justify-content:space-between;align-items:center;'>
      <span style='font-family:"Space Grotesk",sans-serif;font-size:.85rem;font-weight:600;color:{title_c};'>
        Overall Mastery
      </span>
      <span style='font-family:"JetBrains Mono",monospace;font-size:.72rem;color:#FF6B35;'>{overall_pct}%</span>
    </div>
    <div class='progress-bar-bg'>
      <div class='progress-bar-fill' style='width:{overall_pct}%'></div>
    </div>
    """, unsafe_allow_html=True)

    # Achievements
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='sec-tag'>// ACHIEVEMENTS</div>", unsafe_allow_html=True)
    badges_html = ""
    for name, desc, check in ACHIEVEMENTS:
        earned = check(explained, quiz_scores, practiced)
        cls = "achievement earned" if earned else "achievement"
        icon = "🏆" if earned else "🔒"
        badges_html += f"<span class='{cls}'>{icon} {name}</span>"
    st.markdown(f"<div style='margin-top:.4rem;'>{badges_html}</div>", unsafe_allow_html=True)

    # Per-topic breakdown
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='sec-tag'>// TOPIC BREAKDOWN</div>", unsafe_allow_html=True)
    for topic in TOPICS:
        frac = _topic_completion(topic)
        pct_t = int(frac * 100)
        status = _topic_status(topic)
        explained_done = topic in explained
        quiz_score     = quiz_scores.get(topic, 0)
        practice_done  = topic in practiced

        status_label = {
            "mastered":    "<span class='status-badge done'>MASTERED</span>",
            "in-progress": "<span class='status-badge partial'>IN PROGRESS</span>",
            "new":         "<span class='status-badge new'>NOT STARTED</span>",
        }[status]

        e_icon = "✅" if explained_done else "○"
        q_icon = f"📊 {quiz_score}%" if quiz_score > 0 else "○ Quiz"
        p_icon = "✅" if practice_done else "○"

        st.markdown(f"""
        <div class='card' style='padding:1rem 1.3rem;margin-bottom:.5rem;'>
          <div style='display:flex;align-items:center;gap:1rem;flex-wrap:wrap;'>
            <div style='flex:1;min-width:140px;'>
              <div style='font-family:"Space Grotesk",sans-serif;font-size:.9rem;
              font-weight:600;color:{title_c};margin-bottom:.15rem;'>{topic}</div>
              <div style='font-family:"JetBrains Mono",monospace;font-size:.65rem;color:#706860;'>
                {e_icon} Read &nbsp;·&nbsp; {q_icon} &nbsp;·&nbsp; {p_icon} Practice
              </div>
            </div>
            <div style='width:200px;'>
              <div class='progress-bar-bg' style='height:5px;'>
                <div class='progress-bar-fill' style='width:{pct_t}%'></div>
              </div>
            </div>
            {status_label}
          </div>
        </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Roadmap
# ---------------------------------------------------------------------------
def _render_roadmap() -> None:
    st.markdown("""
    <p style='font-family:"Space Grotesk",sans-serif;font-size:.9rem;color:#9E9890;margin-bottom:1.5rem;line-height:1.6;text-align:center;'>
    Follow this structured path from foundations to advanced topics.<br>
    Each node shows your completion progress.
    </p>
    """, unsafe_allow_html=True)

    inner = ""
    for phase_idx, phase in enumerate(ROADMAP):
        nodes_html = ""
        for i, node in enumerate(phase["nodes"]):
            key    = node["key"]
            icon   = node["icon"]
            week   = node["week"]
            frac   = _topic_completion(key)
            pct_n  = int(frac * 100)
            status = _topic_status(key)

            nodes_html += f"""
            <div class='roadmap-node {status}'>
              <span class='roadmap-node-icon'>{icon}</span>
              <div class='roadmap-node-title'>{key}</div>
              <div class='roadmap-node-week'>{week}</div>
              <div class='roadmap-node-bar'>
                <div class='roadmap-node-bar-fill' style='width:{pct_n}%'></div>
              </div>
            </div>"""
            if i < len(phase["nodes"]) - 1:
                nodes_html += "<div class='roadmap-arrow'>→</div>"

        inner += f"""
        <div class='roadmap-phase-label'>{phase['phase']}</div>
        <div class='roadmap-row'>{nodes_html}</div>"""

        if phase_idx < len(ROADMAP) - 1:
            inner += "<div class='roadmap-phase-connector'>↓</div>"

    st.markdown(f"<div class='roadmap-container'>{inner}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;font-family:"JetBrains Mono",monospace;font-size:.62rem;color:#706860;'>
      <span>■ <span style='color:#FF6B35;'>Orange border</span> = Mastered</span>
      <span>■ <span style='color:#FFA06066;'>Faded border</span> = In Progress</span>
      <span>■ Dim = Not started</span>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Study session (explain / quiz / practice)
# ---------------------------------------------------------------------------
def _render_explain(topic: str) -> None:
    _mark_explained(topic)
    content = EXPLANATIONS.get(topic, {})
    if not content:
        st.info("Content coming soon.")
        return

    st.markdown(f"""
    <div class='card'>
      <div class='sec-tag'>OVERVIEW</div>
      <p style='color:#b8c4d4;font-size:.9rem;line-height:1.7;'>{content['summary']}</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### Key Concepts")
    cols = st.columns(2)
    for idx, (name, desc) in enumerate(content.get("key_concepts", [])):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='card' style='margin-bottom:.6rem;'>
              <div style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:.72rem;
              letter-spacing:.08em;margin-bottom:.3rem;'>{name}</div>
              <p style='color:#8892a4;font-size:.82rem;margin:0;'>{desc}</p>
            </div>""", unsafe_allow_html=True)

    if content.get("formulas"):
        st.markdown("#### Key Formulas")
        fhtml = "".join(
            f"<div class='formula' style='margin-bottom:.4rem;'>{f}</div>"
            for f in content["formulas"]
        )
        st.markdown(fhtml, unsafe_allow_html=True)

    if content.get("tip"):
        st.markdown(f"""
        <div style='background:rgba(255,107,53,.07);border:1px solid rgba(255,107,53,.3);
        border-left:3px solid #FF6B35;padding:.8rem 1.1rem;border-radius:8px;margin-top:.8rem;'>
          <span style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:.7rem;
          letter-spacing:.08em;'>💡 STUDY TIP</span>
          <p style='color:#b8c4d4;margin:.4rem 0 0;font-size:.85rem;'>{content['tip']}</p>
        </div>""", unsafe_allow_html=True)


def _render_quiz(topic: str) -> None:
    theme = st.session_state.get("theme", "dark")
    title_c = "#1C1714" if theme == "light" else "#F2EDE6"
    questions = QUIZZES.get(topic, [])
    if not questions:
        st.info("Quiz coming soon for this topic.")
        return

    q_key    = f"quiz_{topic}_q"
    ans_key  = f"quiz_{topic}_ans"
    score_key= f"quiz_{topic}_score"
    done_key = f"quiz_{topic}_done"

    if q_key not in st.session_state:
        st.session_state[q_key]    = 0
        st.session_state[ans_key]  = None
        st.session_state[score_key]= 0
        st.session_state[done_key] = False

    total   = len(questions)
    current = st.session_state[q_key]

    if st.session_state[done_key]:
        score = st.session_state[score_key]
        pct   = int(score / total * 100)
        _update_quiz_score(topic, pct)
        color = "#4ADE80" if pct >= 70 else "#FFA060" if pct >= 40 else "#FF5252"
        st.markdown(f"""
        <div style='text-align:center;padding:2.5rem 1rem;'>
          <div style='font-family:"JetBrains Mono",monospace;font-size:.75rem;color:#9E9890;
          letter-spacing:.1em;margin-bottom:.5rem;'>QUIZ COMPLETE</div>
          <div style='font-size:3.2rem;font-weight:800;font-family:"Syne",sans-serif;color:{color};'>{pct}%</div>
          <div style='color:#b8c4d4;font-size:1rem;margin-top:.3rem;'>{score} / {total} correct</div>
          <div style='color:#9E9890;font-size:.84rem;margin-top:.6rem;'>
            {"&#x1F389; Excellent work!" if pct >= 80 else "&#x1F4D6; Keep reviewing!" if pct < 50 else "&#x1F44D; Good effort!"}
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Try Again", key=f"restart_{topic}"):
            for k in [q_key, ans_key, score_key, done_key]:
                del st.session_state[k]
            st.rerun()
        return

    q        = questions[current]
    progress = current / total

    st.markdown(f"""
    <div class='progress-bar-bg' style='margin-bottom:.35rem;'>
      <div class='progress-bar-fill' style='width:{progress*100:.0f}%'></div>
    </div>
    <div style='color:#9E9890;font-size:.75rem;text-align:right;margin-bottom:1rem;'>
      Question {current+1} of {total} · Score: {st.session_state[score_key]}
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card'>
      <div style='color:{title_c};font-size:.95rem;font-weight:600;margin-bottom:1rem;'>{q['q']}</div>
    </div>""", unsafe_allow_html=True)

    selected = st.session_state[ans_key]
    if selected is None:
        for i, opt in enumerate(q["options"]):
            if st.button(opt, key=f"opt_{topic}_{current}_{i}"):
                st.session_state[ans_key] = i
                if i == q["answer"]:
                    st.session_state[score_key] += 1
                st.rerun()
    else:
        for i, opt in enumerate(q["options"]):
            cls  = "quiz-correct" if i == q["answer"] else ("quiz-wrong" if i == selected else "quiz-option")
            icon = "✓" if i == q["answer"] else ("✗" if i == selected else "")
            st.markdown(f"<div class='{cls}'>{icon} {opt}</div>", unsafe_allow_html=True)

        if selected == q["answer"]:
            st.success("✓ Correct!")
        else:
            st.error(f"✗ Incorrect. Correct: **{q['options'][q['answer']]}**")

        st.markdown(f"""
        <div style='background:rgba(255,107,53,.05);border:1px solid rgba(255,107,53,.2);
        border-left:3px solid #FF6B35;padding:.7rem 1rem;margin-top:.5rem;border-radius:6px;'>
          <span style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:.68rem;'>EXPLANATION</span>
          <p style='color:#b8c4d4;margin:.3rem 0 0;font-size:.83rem;'>{q['explanation']}</p>
        </div>""", unsafe_allow_html=True)

        next_label = "Finish Quiz →" if current + 1 == total else "Next Question →"
        if st.button(next_label, key=f"next_{topic}_{current}"):
            st.session_state[ans_key] = None
            if current + 1 == total:
                st.session_state[done_key] = True
            else:
                st.session_state[q_key] = current + 1
            st.rerun()


def _render_practice(topic: str) -> None:
    theme = st.session_state.get("theme", "dark")
    title_c = "#1C1714" if theme == "light" else "#F2EDE6"
    problems = PROBLEM_SETS.get(topic, [])
    if not problems:
        st.info("Practice problems coming soon for this topic.")
        return

    _mark_practiced(topic)

    for idx, prob in enumerate(problems):
        with st.expander(f"Problem {idx+1}: {prob['title']}", expanded=(idx == 0)):
            st.markdown(f"""
            <div class='card'>
              <div class='sec-tag'>PROBLEM STATEMENT</div>
              <p style='color:#b8c4d4;font-size:.9rem;line-height:1.7;'>{prob['problem']}</p>
            </div>""", unsafe_allow_html=True)

            show_key = f"show_sol_{topic}_{idx}"
            if show_key not in st.session_state:
                st.session_state[show_key] = False

            if st.button(
                "Show Solution" if not st.session_state[show_key] else "Hide Solution",
                key=f"sol_btn_{topic}_{idx}",
            ):
                st.session_state[show_key] = not st.session_state[show_key]
                st.rerun()

            if st.session_state[show_key]:
                steps_html = "".join(
                    f"<div class='problem-step'><span class='step-num'>STEP {i+1}</span>"
                    f"<span style='color:#b8c4d4;'>{s}</span></div>"
                    for i, s in enumerate(prob["steps"])
                )
                st.markdown(f"""
                <div style='margin-top:.8rem;'>
                  <div class='sec-tag'>STEP-BY-STEP SOLUTION</div>
                  <div style='margin-top:.5rem;'>{steps_html}</div>
                  <div style='background:rgba(255,107,53,.07);border:1px solid rgba(255,107,53,.25);
                  padding:.7rem 1rem;margin-top:.8rem;border-radius:6px;'>
                    <div style='color:#FF6B35;font-family:"JetBrains Mono",monospace;font-size:.68rem;
                    margin-bottom:.3rem;'>FINAL ANSWER</div>
                    <div style='color:{title_c};font-size:.88rem;'>{prob['answer']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render() -> None:
    _init_progress()

    st.markdown("""
    <div class='page-header'>
      <div class='sec-tag'>// STUDY HUB — YOUR PERSONAL LEARNING SPACE</div>
      <h2>Your Learning Journey</h2>
      <p class='page-desc'>
        Track your progress across all topics, follow the structured learning roadmap,
        and dive into explanations, quizzes, and practice problems — all in one place.
      </p>
    </div>
    """, unsafe_allow_html=True)

    tab_dash, tab_road, tab_study = st.tabs([
        "📊  Progress Dashboard",
        "🗺️  Learning Roadmap",
        "📖  Study Session",
    ])

    with tab_dash:
        _render_progress_dashboard()

    with tab_road:
        _render_roadmap()

    with tab_study:
        st.markdown("""
        <p style='color:#9E9890;font-size:.88rem;line-height:1.65;margin-bottom:1.2rem;'>
        Choose a topic and a study mode. Your progress is automatically saved as you complete each activity.
        </p>""", unsafe_allow_html=True)

        topic = st.selectbox("Choose a Topic", TOPICS, key="study_topic")

        # Show current topic status
        frac   = _topic_completion(topic)
        status = _topic_status(topic)
        pct_t  = int(frac * 100)
        status_colors = {
            "mastered":    "#FF6B35",
            "in-progress": "#FFA060",
            "new":         "#706860",
        }
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:.8rem;margin:.4rem 0 1rem;'>
          <div class='progress-bar-bg' style='flex:1;height:5px;'>
            <div class='progress-bar-fill' style='width:{pct_t}%'></div>
          </div>
          <span style='font-family:"JetBrains Mono",monospace;font-size:.65rem;
          color:{status_colors[status]};'>{pct_t}% complete</span>
        </div>
        """, unsafe_allow_html=True)

        mode = st.radio(
            "Study Mode",
            ["📖 Read & Learn", "🧪 Take a Quiz", "💪 Practice Problems"],
            horizontal=True,
            key="study_mode",
        )

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        if mode == "📖 Read & Learn":
            _render_explain(topic)
        elif mode == "🧪 Take a Quiz":
            _render_quiz(topic)
        else:
            _render_practice(topic)
