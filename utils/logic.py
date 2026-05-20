"""Propositional logic helpers — safe recursive-descent parser (no eval)."""

import re


# ─── Tokenizer ────────────────────────────────────────────────────────────────

def _pl_tokenize(expr: str) -> list:
    tokens, i, s = [], 0, expr.strip()
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i:i+3] == '<->':
            tokens.append('<->'); i += 3
        elif s[i:i+2] == '->':
            tokens.append('->'); i += 2
        elif s[i:i+3].upper() == 'XOR' and (i + 3 >= len(s) or not s[i+3].isalpha()):
            tokens.append('XOR'); i += 3
        elif s[i:i+2] == '&&':
            tokens.append('&&'); i += 2
        elif s[i:i+2] == '||':
            tokens.append('||'); i += 2
        elif s[i] == '!':
            tokens.append('!'); i += 1
        elif s[i] == '(':
            tokens.append('('); i += 1
        elif s[i] == ')':
            tokens.append(')'); i += 1
        elif s[i].isalpha():
            j = i + 1
            while j < len(s) and s[j].isalpha():
                j += 1
            tokens.append(s[i:j]); i = j
        else:
            i += 1
    return tokens


# ─── Recursive descent parsers ────────────────────────────────────────────────

def _pl_bic(tokens, vals, pos):
    lv, pos = _pl_imp(tokens, vals, pos)
    while pos < len(tokens) and tokens[pos] == '<->':
        pos += 1
        rv, pos = _pl_imp(tokens, vals, pos)
        lv = (lv == rv)
    return lv, pos


def _pl_imp(tokens, vals, pos):
    lv, pos = _pl_or(tokens, vals, pos)
    if pos < len(tokens) and tokens[pos] == '->':
        pos += 1
        rv, pos = _pl_imp(tokens, vals, pos)
        lv = (not lv) or rv
    return lv, pos


def _pl_or(tokens, vals, pos):
    lv, pos = _pl_and(tokens, vals, pos)
    while pos < len(tokens) and tokens[pos] == '||':
        pos += 1
        rv, pos = _pl_and(tokens, vals, pos)
        lv = lv or rv
    return lv, pos


def _pl_and(tokens, vals, pos):
    lv, pos = _pl_xor(tokens, vals, pos)
    while pos < len(tokens) and tokens[pos] == '&&':
        pos += 1
        rv, pos = _pl_xor(tokens, vals, pos)
        lv = lv and rv
    return lv, pos


def _pl_xor(tokens, vals, pos):
    lv, pos = _pl_not(tokens, vals, pos)
    while pos < len(tokens) and tokens[pos] == 'XOR':
        pos += 1
        rv, pos = _pl_not(tokens, vals, pos)
        lv = (lv != rv)
    return lv, pos


def _pl_not(tokens, vals, pos):
    if pos < len(tokens) and tokens[pos] == '!':
        pos += 1
        v, pos = _pl_not(tokens, vals, pos)
        return (not v), pos
    return _pl_atom(tokens, vals, pos)


def _pl_atom(tokens, vals, pos):
    if pos >= len(tokens):
        raise ValueError("Unexpected end of expression")
    tok = tokens[pos]
    if tok == '(':
        pos += 1
        v, pos = _pl_bic(tokens, vals, pos)
        if pos < len(tokens) and tokens[pos] == ')':
            pos += 1
        return v, pos
    elif tok.lower() == 'true':
        return True, pos + 1
    elif tok.lower() == 'false':
        return False, pos + 1
    elif tok in vals:
        return vals[tok], pos + 1
    else:
        raise ValueError(f"Unknown token: {tok!r}")


# ─── Public API ───────────────────────────────────────────────────────────────

def eval_proposition(expr: str, vals: dict) -> bool | None:
    try:
        tokens = _pl_tokenize(expr)
        result, _ = _pl_bic(tokens, vals, 0)
        return bool(result)
    except Exception:
        return None


def gen_truth_table(expr: str):
    """Return (html_string, rows_data) for a truth table."""
    vars_found = sorted(set(re.findall(r'\b([a-z])\b', expr)))
    if not vars_found:
        return "<span class='err'>// ERROR: no single-letter variables found</span>", []
    if len(vars_found) > 5:
        return "<span class='err'>// ERROR: max 5 variables</span>", []

    rows_data = []
    html = "<table class='tt'><thead><tr>"
    for v in vars_found:
        html += f"<th>{v}</th>"
    html += "<th>Result</th></tr></thead><tbody>"
    n = len(vars_found)
    for i in range(1 << n):
        vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(vars_found)}
        res = eval_proposition(expr, vals)
        html += "<tr>"
        for v in vars_found:
            cl = "T" if vals[v] else "F"
            html += f"<td class='{cl}'>{'T' if vals[v] else 'F'}</td>"
        if res is None:
            html += "<td class='err'>ERR</td>"
        else:
            cl = "T" if res else "F"
            html += f"<td class='{cl}'>{'T' if res else 'F'}</td>"
        html += "</tr>"
        rows_data.append((vals, res))
    html += "</tbody></table>"
    return html, rows_data


def check_tautology(rows_data) -> str:
    if not rows_data:
        return ""
    results = [r for _, r in rows_data]
    if all(r is True for r in results):
        return "TAUTOLOGY — true for all assignments"
    if all(r is False for r in results):
        return "CONTRADICTION — false for all assignments"
    return "CONTINGENCY — neither tautology nor contradiction"


def induction_checker(formula_type: str, n_val: int) -> str:
    if formula_type == "sum_natural":
        lhs = sum(range(1, n_val + 1))
        rhs = n_val * (n_val + 1) // 2
        return (f"Base case (n=1): 1 = 1·2/2 = 1 ✓\n"
                f"Inductive hypothesis: Assume true for k.\n"
                f"Inductive step: sum(1..{n_val}) = {lhs}, formula = {n_val}·{n_val+1}/2 = {rhs}\n"
                f"{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}")
    elif formula_type == "sum_squares":
        lhs = sum(i * i for i in range(1, n_val + 1))
        rhs = n_val * (n_val + 1) * (2 * n_val + 1) // 6
        return (f"Base case (n=1): 1² = 1·2·3/6 = 1 ✓\n"
                f"Inductive step: Σi²(1..{n_val}) = {lhs}, formula = {n_val}·{n_val+1}·{2*n_val+1}/6 = {rhs}\n"
                f"{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}")
    elif formula_type == "geometric":
        r = 2
        lhs = sum(r**i for i in range(n_val + 1))
        rhs = r**(n_val + 1) - 1
        return (f"Geometric sum Σ 2^i (i=0..{n_val}):\n"
                f"Base (n=0): 1 = 2^1-1 = 1 ✓\n"
                f"Step: sum = {lhs}, 2^({n_val}+1)-1 = {rhs}\n"
                f"{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}")
    elif formula_type == "power_of_2":
        return (f"Claim: 2^n divisible by 2 for n≥1\n"
                f"2^{n_val} = {2**n_val}\n"
                f"Base (n=1): 2^1=2, divisible by 2 ✓\n"
                f"Inductive step: if 2^k is divisible by 2, then 2^(k+1)=2·2^k also divisible by 2 ✓")
    return "Formula not recognized."
