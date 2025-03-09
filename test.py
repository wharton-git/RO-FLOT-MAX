import networkx as nx

def solve_max_flow():
    G = nx.DiGraph()
    
    # Ajouter les dépôts (sources)
    G.add_edge('S', 'A', capacity=45)
    G.add_edge('S', 'B', capacity=25)
    G.add_edge('S', 'C', capacity=30)
    
    # Ajouter les chemins de transport avec leurs capacités
    G.add_edge('A', 'D', capacity=10)
    G.add_edge('A', 'E', capacity=15)
    G.add_edge('A', 'G', capacity=20)
    G.add_edge('B', 'D', capacity=20)
    G.add_edge('B', 'E', capacity=5)
    G.add_edge('B', 'F', capacity=15)
    G.add_edge('C', 'E', capacity=10)
    G.add_edge('C', 'G', capacity=15)
    
    # Ajouter les demandes (puits)
    G.add_edge('D', 'T', capacity=30)
    G.add_edge('E', 'T', capacity=10)
    G.add_edge('F', 'T', capacity=20)
    G.add_edge('G', 'T', capacity=40)
    
    # Calculer le flot maximal
    flow_value, flow_dict = nx.maximum_flow(G, 'S', 'T')
    
    print(f"Flot maximal : {flow_value} tonnes\n")
    print("Capacités des arcs et flots utilisés :")
    
    for u, neighbors in flow_dict.items():
        for v, flow in neighbors.items():
            if G.has_edge(u, v):
                capacity = G[u][v]['capacity']
                remaining = capacity - flow
                status = "(Saturé)" if remaining == 0 else ""
                print(f"{u} -> {v} : {flow}/{capacity} {status}")

if __name__ == "__main__":
    solve_max_flow()
