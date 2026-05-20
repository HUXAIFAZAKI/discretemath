"""Relation theory helpers."""

import collections


def relation_properties(n: int, pairs: list) -> dict:
    pair_set = set(pairs)
    reflexive     = all((i, i) in pair_set for i in range(n))
    irreflexive   = all((i, i) not in pair_set for i in range(n))
    symmetric     = all((b, a) in pair_set for (a, b) in pair_set)
    antisymmetric = all(not ((b, a) in pair_set and a != b) for (a, b) in pair_set)
    transitive    = all(
        (a, c) in pair_set
        for (a, b) in pair_set
        for (b2, c) in pair_set
        if b == b2
    )
    return {
        "Reflexive": reflexive, "Irreflexive": irreflexive,
        "Symmetric": symmetric, "Antisymmetric": antisymmetric,
        "Transitive": transitive,
    }


def matrix_to_pairs(matrix: list) -> list:
    n = len(matrix)
    return [(i, j) for i in range(n) for j in range(n) if matrix[i][j]]


def reflexive_closure(n: int, pairs: list) -> list:
    s = set(pairs) | {(i, i) for i in range(n)}
    return sorted(s)


def symmetric_closure(pairs: list) -> list:
    s = set(pairs) | {(b, a) for (a, b) in pairs}
    return sorted(s)


def transitive_closure(n: int, pairs: list) -> list:
    """Warshall's algorithm."""
    reach = [[False] * n for _ in range(n)]
    for (a, b) in pairs:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return [(i, j) for i in range(n) for j in range(n) if reach[i][j]]


def compose_relations(r1: list, r2: list) -> list:
    r2_dict: dict = {}
    for (b, c) in r2:
        r2_dict.setdefault(b, []).append(c)
    result = set()
    for (a, b) in r1:
        for c in r2_dict.get(b, []):
            result.add((a, c))
    return sorted(result)


def is_equivalence(n: int, pairs: list) -> bool:
    p = relation_properties(n, pairs)
    return p["Reflexive"] and p["Symmetric"] and p["Transitive"]


def equivalence_classes(n: int, pairs: list) -> dict:
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    for (a, b) in pairs:
        if a != b:
            union(a, b)
    classes: dict = {}
    for i in range(n):
        classes.setdefault(find(i), []).append(i)
    return classes


def is_partial_order(n: int, pairs: list) -> bool:
    p = relation_properties(n, pairs)
    return p["Reflexive"] and p["Antisymmetric"] and p["Transitive"]


def parse_pairs(s: str, n: int) -> list:
    result = []
    try:
        for token in s.split("|"):
            token = token.strip()
            if not token:
                continue
            parts = token.replace("(", "").replace(")", "").split(",")
            a, b = int(parts[0].strip()), int(parts[1].strip())
            if 0 <= a < n and 0 <= b < n:
                result.append((a, b))
    except Exception:
        pass
    return result
