import networkx as nx

def dfs(residual_graph, source, sink, parent, visited):
    visited.add(source)
    if source == sink:
        return True
    
    for v in residual_graph[source]:
        if v not in visited and residual_graph[source][v] > 0:
            parent[v] = source
            if dfs(residual_graph, v, sink, parent, visited):
                return True
    return False

def ford_fulkerson(graph, source, sink):
    residual_graph = {u: {v: graph[u][v] for v in graph[u]} for u in graph}
    
    # Ajouter toutes les clés pour les arcs inverses
    for u in graph:
        for v in graph[u]:
            if v not in residual_graph:
                residual_graph[v] = {}
            if u not in residual_graph[v]:
                residual_graph[v][u] = 0
    
    parent = {}
    max_flow = 0
    
    while True:
        visited = set()
        if not dfs(residual_graph, source, sink, parent, visited):
            break
        
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]
        
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]
        
        max_flow += path_flow
    
    return max_flow, residual_graph

def solve_max_flow():
    graph = {
        'S': {'A': 45, 'B': 25, 'C': 30},
        'A': {'D': 10, 'E': 15, 'G': 20},
        'B': {'D': 20, 'E': 5, 'F': 15},
        'C': {'E': 10, 'G': 15},
        'D': {'T': 30},
        'E': {'T': 10},
        'F': {'T': 20},
        'G': {'T': 40},
        'T': {}
    }
    
    max_flow, residual_graph = ford_fulkerson(graph, 'S', 'T')
    
    print(f"Flot maximal : {max_flow} tonnes\n")
    print("Capacités des arcs et flots restants :")
    for u in graph:
        for v in graph[u]:
            used_flow = graph[u][v] - residual_graph[u].get(v, 0)
            remaining = residual_graph[u].get(v, 0)
            status = "(Saturé)" if remaining == 0 else ""
            print(f"{u} -> {v} : {used_flow}/{graph[u][v]} {status}")

if __name__ == "__main__":
    solve_max_flow()
