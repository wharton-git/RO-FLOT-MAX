import networkx as nx
import matplotlib.pyplot as plt

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

def draw_graph(graph, residual_graph):
    G = nx.DiGraph()
    
    # Ajouter les arcs au graphe
    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v, capacity=graph[u][v], flow=graph[u][v] - residual_graph[u].get(v, 0))
    
    # Définir les positions manuellement
    pos = {
        'S': (0, -0.5),
        'A': (1, 0.5),
        'B': (1, -0.5),
        'C': (1, -1.5),
        'D': (2, 1),
        'E': (2.5, 0),
        'F': (2.5, -1),
        'G': (2, -2),
        'T': (4, -0.5)
    }
    
    edges = G.edges()
    
    # Couleurs des arcs (rouge pour saturé, bleu pour non saturé)
    edge_colors = ['red' if G[u][v]['flow'] == G[u][v]['capacity'] else 'blue' for u, v in edges]
    
    # Dessiner le graphe
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', arrowsize=20)
    
    # Dessiner les arcs avec la couleur
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=2)
    
    # Ajouter les labels de capacité et de flux
    edge_labels = {(u, v): f"{G[u][v]['flow']}/{G[u][v]['capacity']}" for u, v in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Graphe de Flot Maximal")
    plt.show()

def solve_max_flow():
    graph = {
        'S': {'A': 45, 'B': 25, 'C': 30},
        'A': {'D': 10, 'E': 15, 'G': 20},
        'B': {'D': 20, 'E': 5, 'F': 15},
        'C': {'F': 10, 'G': 15},
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
    
    # Dessiner le graphe
    draw_graph(graph, residual_graph)

if __name__ == "__main__":
    solve_max_flow()
