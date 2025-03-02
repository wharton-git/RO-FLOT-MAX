import networkx as nx
import matplotlib.pyplot as plt

# Fonction pour saisir les données manuellement
def saisir_donnees():
    G = nx.DiGraph()

    # Saisir les nœuds (dépôts et destinations)
    print("Saisie des nœuds :")
    depots = input("Entrez les nœuds de dépôts (séparés par des espaces, ex: A B C) : ").split()
    destinations = input("Entrez les nœuds de destinations (séparés par des espaces, ex: D E F G) : ").split()

    # Saisir les capacités des dépôts
    print("\nSaisie des capacités des dépôts :")
    for depot in depots:
        capacite = int(input(f"Capacité du dépôt {depot} : "))
        G.add_edge('S', depot, capacity=capacite)  # Relier la source aux dépôts

    # Saisir les demandes des destinations
    print("\nSaisie des demandes des destinations :")
    for destination in destinations:
        demande = int(input(f"Demande de la destination {destination} : "))
        G.add_edge(destination, 'T', capacity=demande)  # Relier les destinations au puits

    # Saisir les arêtes entre les dépôts et les destinations
    print("\nSaisie des arêtes entre les dépôts et les destinations :")
    while True:
        u = input("Entrez le nœud de départ (ou appuyez sur Entrée pour terminer) : ")
        if u == "":
            break
        v = input("Entrez le nœud d'arrivée : ")
        capacite = int(input(f"Capacité de l'arête {u} -> {v} : "))
        G.add_edge(u, v, capacity=capacite)

    return G

# Fonction principale
def main():
    # Saisir les données manuellement
    G = saisir_donnees()

    # Afficher les nœuds et les arêtes
    print("\nNœuds du graphe:")
    print(G.nodes())

    print("\nArêtes du graphe avec leurs capacités:")
    for u, v, data in G.edges(data=True):
        print(f"{u} -> {v} : capacité = {data['capacity']}")

    # Calculer le flot maximal
    flow_value, flow_dict = nx.maximum_flow(G, 'S', 'T')

    print(f"\nFlot maximal: {flow_value}")
    print("Répartition des flots:")
    for u, in_flow in flow_dict.items():
        for v, flow in in_flow.items():
            if flow > 0:
                print(f"{u} -> {v}: {flow}")

    # Définir des positions fixes pour les nœuds
    pos = {
        'S': (0, 1),  # Source en haut à gauche
        'A': (1, 2),  # Dépôt A
        'B': (1, 1),  # Dépôt B
        'C': (1, 0),  # Dépôt C
        'D': (2, 2),  # Destination D
        'E': (2, 1),  # Destination E
        'F': (2, 0),  # Destination F
        'G': (2, -1),  # Destination G
        'T': (4, 1),  # Puits en haut à droite
    }

    # Dessiner le graphe avec les positions fixes
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')

    # Ajouter les labels des capacités sur les arêtes
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.savefig("graph.png")  # Sauvegarder la figure si l'affichage échoue
    print("Le graphe a été sauvegardé sous 'graph.png'")

# Exécuter le programme
if __name__ == "__main__":
    main()