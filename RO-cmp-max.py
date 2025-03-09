import networkx as nx
import matplotlib.pyplot as plt

# Créer un graphe orienté
G = nx.DiGraph()

# Ajouter les arcs avec leurs capacités
G.add_edge('S', 'A', capacity=45)
G.add_edge('S', 'B', capacity=25)
G.add_edge('S', 'C', capacity=30)

G.add_edge('A', 'D', capacity=10)
G.add_edge('A', 'E', capacity=15)
G.add_edge('A', 'G', capacity=20)

G.add_edge('B', 'D', capacity=20)
G.add_edge('B', 'E', capacity=5)
G.add_edge('B', 'F', capacity=15)

G.add_edge('C', 'F', capacity=10)
G.add_edge('C', 'G', capacity=15)

G.add_edge('D', 'T', capacity=30)
G.add_edge('E', 'T', capacity=10)
G.add_edge('F', 'T', capacity=20)
G.add_edge('G', 'T', capacity=40)

# Calculer le flot maximal
flow_value, flow_dict = nx.maximum_flow(G, 'S', 'T')

# Afficher le flot maximal
print(f"Flot maximal : {flow_value} tonnes")

# Afficher le flot complet (détail des arcs)
print("\nDétail du flot complet :")
for source, targets in flow_dict.items():
    for target, flow in targets.items():
        if flow > 0:
            print(f"{source} -> {target} : {flow} tonnes")

# Préparer les couleurs des arcs
edge_colors = []
for u, v in G.edges():
    capacity = G[u][v]['capacity']
    flow = flow_dict[u].get(v, 0)
    if flow == capacity:  # Arc saturé
        edge_colors.append('red')
    else:  # Arc non saturé
        edge_colors.append('black')

# Dessiner le graphe
pos = {
    'S': (0, 0),  # Source
    'A': (1, 1),  # Dépôt A
    'B': (1, 0),  # Dépôt B
    'C': (1, -1),  # Dépôt C
    'D': (2, 1.5),  # Destination D
    'E': (3, 0.5),  # Destination E
    'F': (3, -0.5),  # Destination F
    'G': (2, -1.5),  # Destination G
    'T': (4, 0)   # Puits T
}
# Positionnement des nœuds
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, width=2, arrows=True)

# Ajouter les labels des flots sur les arcs
edge_labels = {(u, v): f"{flow_dict[u].get(v, 0)}/{G[u][v]['capacity']}" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

# Afficher le graphe
plt.title("Graphe du flot maximal (rouge = arcs saturés)")
plt.show()