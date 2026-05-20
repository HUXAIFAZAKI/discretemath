"""Groq AI API wrappers."""

import json
import os
import re
from pathlib import Path

# Load .env.local if present (so GROQ_API_KEY is available without system env)
_env_file = Path(__file__).resolve().parent.parent / ".env.local"
if _env_file.exists():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())


def call_groq_nlp(user_statement: str) -> str:
    try:
        from groq import Groq  # type: ignore
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        system_prompt = """You are an expert in Discrete Mathematics.
The user will give you a problem in plain English.
Parse it and solve it step-by-step. Topics covered:
- Set Theory, Relations, Propositional Logic, Rules of Inference,
  Proof Methods, Mathematical Induction, Sequences, Combinatorics, Graph Theory.

Respond with:
1. Problem interpretation
2. Mathematical formulation
3. Step-by-step solution
4. Final answer

Keep it clear and educational."""
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_statement},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            temperature=0.3,
        )
        return chat.choices[0].message.content
    except ImportError:
        return "❌ groq package not installed. Run: pip install groq"
    except KeyError:
        return "❌ GROQ_API_KEY environment variable not set."
    except Exception as e:
        return f"❌ Groq API error: {str(e)}"


def call_notation_converter(statement: str) -> dict:
    system_prompt = """You are an expert in Discrete Mathematics and Propositional Logic.
Convert the given English statement(s) into formal discrete mathematical notation.

Instructions:
1. Identify each atomic proposition and assign short variable names (p, q, r, s, ...).
2. Identify the logical connective(s): → (if-then), ∧ (and), ∨ (or), ¬ (not), ↔ (iff).
3. Write the complete formal notation.
4. If the input contains multiple statements forming an argument, also write the argument form.
5. Name the argument form if applicable (e.g., Modus Ponens, Modus Tollens).

Respond in this EXACT JSON format — pure JSON only, no markdown fences:
{
  "variables": [{"symbol": "p", "meaning": "..."}],
  "notation": "p → q",
  "argument_form": "p → q\\np\\n∴ q",
  "form_name": "Modus Ponens",
  "explanation": "Short explanation",
  "truth_condition": "This is true when ..."
}
If there is no multi-statement argument, set "argument_form" and "form_name" to empty strings."""

    raw = ""
    try:
        from groq import Groq  # type: ignore
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert to discrete math notation:\n{statement}"},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=700,
            temperature=0.1,
        )
        raw = resp.choices[0].message.content.strip()
        cleaned = re.sub(r'```(?:json)?\s*|\s*```', '', raw).strip()
        data = json.loads(cleaned)
        return {"success": True, "data": data}
    except KeyError:
        return {"success": False, "error": "GROQ_API_KEY environment variable not set."}
    except ImportError as e:
        return {"success": False, "error": f"Package not installed: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e), "raw": raw}
