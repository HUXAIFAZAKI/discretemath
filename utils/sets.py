"""Set theory helpers."""


def parse_set(s: str) -> list:
    return list(dict.fromkeys([x.strip() for x in s.split(",") if x.strip()]))


def fmt_set(lst: list) -> str:
    return "{" + ", ".join(str(x) for x in lst) + "}" if lst else "∅"


def compute_set_ops(A: list, B: list, U: list) -> dict:
    As, Bs = set(A), set(B)
    union = list(dict.fromkeys(A + [x for x in B if x not in As]))
    inter = [x for x in A if x in Bs]
    diff_ab = [x for x in A if x not in Bs]
    diff_ba = [x for x in B if x not in As]
    sym_diff = diff_ab + diff_ba
    comp_a = [x for x in U if x not in As]
    comp_b = [x for x in U if x not in Bs]
    cart = [(a, b) for a in A for b in B]
    return {
        "union": union,
        "intersection": inter,
        "diff_ab": diff_ab,
        "diff_ba": diff_ba,
        "sym_diff": sym_diff,
        "comp_a": comp_a,
        "comp_b": comp_b,
        "cartesian": cart,
    }
