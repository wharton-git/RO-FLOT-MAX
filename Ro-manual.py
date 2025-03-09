import networkx as netx

def flot_max(graph, src, dst):
    resid_graph = graph.copy()
    max_flot = 0

    def chemin_up(resid_graph, src, dst, chemin, visited):
        if src == dst:
            return chemin
        visited.add(src)

        for voisin in resid_graph.neighbors(src):
            capacity = resid_graph[src][voisin]['capacity']
            if voisin not in visited and capacity > 0:
                nouvelle_chemin = chemin_up(resid_graph, voisin, dst, chemin + [(src, voisin)], visited)
                if nouvelle_chemin:
                    return nouvelle_chemin
        return None
    
    iteration = 1
    while True:
        print(f"Iteration {iteration}:")
        chemin = chemin_up(resid_graph, src, dst, [], set())
        if not chemin:
            print("Aucun chemin trouvé, arrêt de l'algorithme.")
            break
        
        print(f"Chemin trouvé: {chemin}")
        limite_min = min(resid_graph[u][v]['capacity'] for u, v in chemin)
        print(f"Flot ajouté: {limite_min}")
        
        for u, v in chemin:
            resid_graph[u][v]['capacity'] -= limite_min
            if resid_graph.has_edge(v, u):
                resid_graph[v][u]['capacity'] += limite_min
            else:
                resid_graph.add_edge(v, u, capacity=limite_min)
        
        max_flot += limite_min
        iteration += 1
    
    return max_flot, resid_graph

def afficher_arcs_saturation(graph, resid_graph):
    print("\nÉtat des arcs après exécution de l'algorithme:")
    for u, v in graph.edges():
        capacite_initiale = graph[u][v]['capacity']
        capacite_residuelle = resid_graph[u][v]['capacity']
        capacite_utilisée = capacite_initiale - capacite_residuelle
        etat = "Saturé" if capacite_residuelle == 0 else "Non saturé"
        print(f"{u} -> {v} (capacité utilisée: {capacite_utilisée}/{capacite_initiale}) - {etat}")

G = netx.DiGraph()
edge = [
    ('S', 'A', 45), ('S', 'B', 25), ('S', 'C', 30),
    ('A', 'D', 10), ('A', 'E', 15), ('A', 'G', 20),
    ('B', 'D', 20), ('B', 'E', 5), ('B', 'F', 15),
    ('C', 'E', 10), ('C', 'G', 15),
    ('D', 'T', 30),
    ('E', 'T', 10),
    ('F', 'T', 20),
    ('G', 'T', 40)
]

for d, f, cap in edge:
    G.add_edge(d, f, capacity=cap)

source, destination = "S", "T"
max_flot, resid_graph = flot_max(G, source, destination)
print(f"\nFlot maximal: {max_flot}\n")
afficher_arcs_saturation(G, resid_graph)
