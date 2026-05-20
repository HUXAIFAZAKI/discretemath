"""Graph theory helpers."""

import collections


def graph_analyze(adj: list) -> dict:
    n = len(adj)
    degrees = [sum(row) for row in adj]
    total_deg = sum(degrees)
    edges = total_deg // 2
    odd = sum(1 for d in degrees if d % 2 != 0)

    visited = [False] * n
    queue = collections.deque([0])
    visited[0] = True
    cnt = 1
    while queue:
        u = queue.popleft()
        for v in range(n):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                cnt += 1
                queue.append(v)

    if odd == 0:
        eulerian = "Eulerian Circuit exists (all even degrees)"
    elif odd == 2:
        eulerian = "Eulerian Path exists (exactly 2 odd-degree vertices)"
    else:
        eulerian = f"No Eulerian path/circuit ({odd} odd-degree vertices)"

    return {
        "vertices": n, "edges": edges, "degrees": degrees,
        "total_degree": total_deg, "connected": cnt == n,
        "odd_degree_count": odd, "eulerian": eulerian,
    }
