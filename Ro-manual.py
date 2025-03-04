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
    while True:
        chemin = chemin_up(resid_graph, src, dst, [], set())
        if not chemin:
            break

        limite_min = min(resid_graph[u][v]['capacity'] for u, v in chemin)
        
        for u, v in chemin:
            resid_graph[u][v]['capacity'] -= limite_min
            if resid_graph.has_edge(v, u):
                resid_graph[v][u]['capacity'] += limite_min
            else:
                resid_graph.add_edge(v, u, capacity=limite_min)
        
        max_flot += limite_min
    return max_flot, resid_graph

G = netx.DiGraph()
# edge = [
#     ('S', 'A', 10), ('S', 'B', 5), ('S', 'C', 15),
#     ('A', 'B', 4), ('A', 'D', 9), ('A', 'E', 15),
#     ('B', 'C', 4), ('B', 'E', 8),
#     ('C', 'F', 16),
#     ('D', 'E', 15), ('D', 'T', 10),
#     ('E', 'F', 15), ('E', 'T', 10),
#     ('F', 'T', 10)
# ]

# for d, f, cap in edge: #d = depart, f = fin, cap = capacite
#     G.add_edge(d, f, capacity=cap)

depots = {} 
depots_input = input("Entrer les dépôts (ex: A B C) : ").split()
for nom in depots_input:
    capacite = int(input(f"Capacité du dépôt {nom} : "))
    depots[nom] = capacite
    G.add_edge("S", nom, capacity=capacite)

destinations = {}  
destinations_input = input("Entrer les destinations (ex: X Y Z) : ").split()
for nom in destinations_input:
    capacite = int(input(f"Capacité de la destination {nom} : "))
    destinations[nom] = capacite
    G.add_edge(nom, "T", capacity=capacite)

print("Entrer les arcs (départ arrivée capacité), laisser vide pour terminer :")
while True:
    arc_input = input("Noeud de départ, arrivée et capacité (ex: A B 10) : ")
    if not arc_input:
        break
    d, f, cap = arc_input.split()
    cap = int(cap)
    if cap > 0:
        G.add_edge(d, f, capacity=cap)

source, destination = "S", "T"
max_flot, resid_graph = flot_max(G, source, destination)
print(f"Flot maximal: {max_flot}")
print("Graphe des résidus:", [(d, f, resid_graph[d][f]['capacity']) for d, f in resid_graph.edges])
