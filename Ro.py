import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonction pour créer le graphe et calculer le flot maximal
def calculer_flot():
    G = nx.DiGraph()

    # Récupérer les noms des dépôts et destinations
    depots = entry_depots.get().split()
    destinations = entry_destinations.get().split()

    try:
        # Ajouter les arcs avec leurs capacités
        for depot in depots:
            capacite = int(entries_capacites[depot].get())
            G.add_edge('S', depot, capacity=capacite)

        for destination in destinations:
            demande = int(entries_demandes[destination].get())
            G.add_edge(destination, 'T', capacity=demande)

        # Ajouter les arêtes entre les dépôts et les destinations
        for i, depot in enumerate(depots):
            for j, destination in enumerate(destinations):
                capacite = int(entries_aretes[i][j].get())
                if capacite > 0:  # Ignorer les arêtes avec une capacité de 0
                    G.add_edge(depot, destination, capacity=capacite)

        # Calculer le flot maximal
        flow_value, flow_dict = nx.maximum_flow(G, 'S', 'T')

        # Afficher le résultat
        resultat = f"Flot maximal: {flow_value}\n\nRépartition des flots:\n"
        for u, in_flow in flow_dict.items():
            for v, flow in in_flow.items():
                if flow > 0:
                    resultat += f"{u} -> {v}: {flow}\n"
        messagebox.showinfo("Résultat", resultat)

        # Dessiner le graphe
        pos = nx.spring_layout(G)  # Positionnement automatique
        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'capacity')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        # Afficher le graphe dans l'interface
        for widget in frame_graph.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")

# Fonction pour créer les champs de saisie dynamiques
def creer_champs_saisie():
    # Supprimer les anciens champs
    for widget in frame_entrees.winfo_children():
        widget.destroy()

    # Récupérer les noms des dépôts et destinations
    depots = entry_depots.get().split()
    destinations = entry_destinations.get().split()

    # Créer les champs pour les capacités des dépôts
    Label(frame_entrees, text="Capacité des dépôts:").grid(row=0, column=0, columnspan=2)
    for i, depot in enumerate(depots):
        Label(frame_entrees, text=f"{depot}:").grid(row=i + 1, column=0)
        entries_capacites[depot] = Entry(frame_entrees)
        entries_capacites[depot].grid(row=i + 1, column=1)

    # Créer les champs pour les demandes des destinations
    Label(frame_entrees, text="\nDemandes des destinations:").grid(row=len(depots) + 2, column=0, columnspan=2)
    for i, destination in enumerate(destinations):
        Label(frame_entrees, text=f"{destination}:").grid(row=len(depots) + 3 + i, column=0)
        entries_demandes[destination] = Entry(frame_entrees)
        entries_demandes[destination].grid(row=len(depots) + 3 + i, column=1)

    # Créer le tableau des capacités des arêtes
    Label(frame_entrees, text="\nCapacités des arêtes (dépôts -> destinations):").grid(row=len(depots) + len(destinations) + 4, column=0, columnspan=len(destinations) + 1)
    entries_aretes.clear()
    for i, depot in enumerate(depots):
        entries_aretes.append([])
        Label(frame_entrees, text=depot).grid(row=len(depots) + len(destinations) + 5 + i, column=0)
        for j, destination in enumerate(destinations):
            entry = Entry(frame_entrees)
            entry.grid(row=len(depots) + len(destinations) + 5 + i, column=j + 1)
            entries_aretes[i].append(entry)

# Créer l'interface graphique
root = Tk()
root.title("Problème de flot maximal")

# Variables pour stocker les entrées
entries_capacites = {}
entries_demandes = {}
entries_aretes = []

# Frame pour les noms des dépôts et destinations
frame_noms = Frame(root)
frame_noms.pack(pady=10)

Label(frame_noms, text="Dépôts (séparés par des espaces):").grid(row=0, column=0)
entry_depots = Entry(frame_noms)
entry_depots.grid(row=0, column=1)

Label(frame_noms, text="Destinations (séparés par des espaces):").grid(row=1, column=0)
entry_destinations = Entry(frame_noms)
entry_destinations.grid(row=1, column=1)

Button(frame_noms, text="Créer les champs de saisie", command=creer_champs_saisie).grid(row=2, column=0, columnspan=2)

# Frame pour les entrées
frame_entrees = Frame(root)
frame_entrees.pack(pady=10, side="right")

# Frame pour afficher le graphe
frame_graph = Frame(root)
frame_graph.pack(pady=10, side="left", fill="both", expand=True)

# Bouton pour calculer le flot
Button(root, text="Calculer le flot maximal", command=calculer_flot).pack(pady=10)

# Lancer l'interface
root.mainloop()