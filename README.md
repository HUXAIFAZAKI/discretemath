# Discrete Academy — Logic & Mathematics

An interactive web app for learning **Discrete Mathematics** — the branch of math that powers computer science, algorithms, databases, and AI. Built with Python and Streamlit, it combines lessons, practice problems, quizzes, visual tools, and an AI solver all in one place.

---

## What Is This App?

Discrete Academy is a study platform aimed at students learning discrete math for the first time. Instead of just reading a textbook, you can interact with concepts directly — build sets, draw graphs, test logic formulas, and ask an AI to solve problems step by step.

---

## Features at a Glance

| Feature                | What It Does                                                               |
| ---------------------- | -------------------------------------------------------------------------- |
| **11 Topic Pages**     | One dedicated page per topic, each with explanations and interactive tools |
| **AI Solver**          | Type a problem in plain English and get a full step-by-step solution       |
| **Notation Converter** | Translate English sentences into proper math symbols                       |
| **Study Mode**         | Structured learning roadmap with quizzes and problem sets                  |
| **Progress Tracking**  | Keeps track of which topics and quizzes you have completed                 |
| **Dark / Light Theme** | Switch themes via a URL parameter (`?theme=dark` or `?theme=light`)        |

---

## Topics Covered

1. **Sets** — unions, intersections, subsets, power sets, Venn diagrams
2. **Relations** — reflexive, symmetric, transitive properties; equivalence classes
3. **Propositional Logic** — AND, OR, NOT, truth tables, logical equivalences
4. **Rules of Inference** — modus ponens, syllogisms, valid arguments
5. **Proof Methods** — direct proof, proof by contradiction, contrapositive
6. **Mathematical Induction** — base case, inductive step, strong induction
7. **Sequences & Summations** — arithmetic, geometric, recursive sequences; sigma notation
8. **Combinatorics** — permutations, combinations, counting principles
9. **Graphs** — nodes, edges, paths, directed and undirected graphs, visualizer
10. **Study Mode** — roadmap across all topics with quizzes and practice problems
11. **AI Solver** — powered by Groq's LLaMA 3 model

---

## Project Structure

```
app.py                  ← Main entry point; runs the app and routes pages
requirements.txt        ← Python packages needed to run the app

pages/                  ← One file per topic page
    home.py             ← Landing / welcome page
    sets.py             ← Set Theory page
    relations.py        ← Relations page
    logic.py            ← Propositional Logic page
    inference.py        ← Rules of Inference page
    proofs.py           ← Proof Methods page
    induction.py        ← Mathematical Induction page
    sequences.py        ← Sequences & Summations page
    combinatorics.py    ← Combinatorics page
    graphs.py           ← Graph Theory page
    ai_solver.py        ← AI Solver & Notation Converter page

study/                  ← Study Mode components
    study_mode.py       ← Roadmap, progress tracker, session coordinator
    content.py          ← Topic explanations and learning material
    quizzes.py          ← Quiz questions and answer checking
    problem_sets.py     ← Practice problems per topic

utils/                  ← Shared helper functions
    ai_api.py           ← Connects to Groq AI API (LLaMA 3 model)
    graph.py            ← Graph drawing and analysis helpers
    logic.py            ← Logic formula evaluation helpers
    relations.py        ← Relation property checkers
    sets.py             ← Set operation helpers

styles/
    theme.py            ← CSS styling, navigation bar, dark/light themes
```

---

## How to Run

### 1. Install Python

Make sure you have Python 3.9 or newer installed. Download it from [python.org](https://python.org).

### 2. Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install streamlit groq matplotlib
```

### 3. Set Up the AI API Key

The AI Solver uses [Groq](https://groq.com) to run the LLaMA 3 model. You need a free API key.

1. Sign up at [console.groq.com](https://console.groq.com) to get your key.
2. Create a file named `.env.local` in the project root folder.
3. Add this line to it (replace the placeholder with your actual key):

```
GROQ_API_KEY=your_api_key_here
```

> If you skip this step, everything except the AI Solver will still work fine.

### 4. Start the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How Navigation Works

The app uses URL query parameters to track the current page and theme:

- `?page=sets` → opens the Sets page
- `?page=graphs` → opens the Graph Theory page
- `?theme=light` → switches to light mode
- `?theme=dark` → switches to dark mode (default)

You can bookmark or share any page directly using these URLs.

---

## AI Solver Details

The AI Solver has two tools:

1. **Problem Solver (Chatbot)** — Type any discrete math problem in plain English. The AI will:
   - Interpret what you are asking
   - Write it out in proper math notation
   - Solve it step by step
   - Give a clear final answer

2. **English → Notation Converter** — Type a sentence like _"For all x, if x is even then x squared is even"_ and the app converts it to proper mathematical symbols like `∀x (Even(x) → Even(x²))`.

Both tools are powered by Groq's `llama-3.3-70b-versatile` model.

---

## Study Mode

Study Mode gives you a structured path through all topics:

- A **visual roadmap** showing topics grouped by phase (Foundations → Relationships → Logic → Proofs → Advanced)
- **Quizzes** at the end of each topic with instant feedback
- **Problem sets** for extra practice
- A **progress dashboard** showing how many topics and quizzes you have finished

Progress is saved in your browser session.

---

## Requirements

| Package      | Purpose                                |
| ------------ | -------------------------------------- |
| `streamlit`  | Web framework that runs the entire app |
| `groq`       | Python client for the Groq AI API      |
| `matplotlib` | Drawing graphs and charts              |

Install all at once:

```bash
pip install streamlit groq matplotlib
```

---

## Quick Start Summary

```bash
# 1. Clone or download the project
# 2. Install packages
pip install streamlit groq matplotlib

# 3. Add your Groq API key to .env.local (optional, for AI features)
echo GROQ_API_KEY=your_key_here > .env.local

# 4. Run
streamlit run app.py
```

---

## Who Is This For?

- Students taking a Discrete Mathematics course
- Anyone who wants to understand the math behind computer science
- Learners who prefer hands-on, interactive tools over passive reading
