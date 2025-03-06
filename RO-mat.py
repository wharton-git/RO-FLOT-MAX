import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FlotMaxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.graph = nx.DiGraph()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.label_depots = QLabel("Dépôts (séparés par des espaces):")
        layout.addWidget(self.label_depots)
        self.entry_depots = QLineEdit()
        layout.addWidget(self.entry_depots)
        
        self.label_destinations = QLabel("Destinations (séparées par des espaces):")
        layout.addWidget(self.label_destinations)
        self.entry_destinations = QLineEdit()
        layout.addWidget(self.entry_destinations)
        
        self.label_arcs = QLabel("Arcs (départ arrivée capacité) séparés par des virgules:")
        layout.addWidget(self.label_arcs)
        self.entry_arcs = QLineEdit()
        layout.addWidget(self.entry_arcs)
        
        self.btn_calculer = QPushButton("Calculer le flot maximal")
        self.btn_calculer.clicked.connect(self.calculer_flot)
        layout.addWidget(self.btn_calculer)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.setWindowTitle("Problème de flot maximal")

    def flot_max(self, graph, src, dst):
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

    def calculer_flot(self):
        self.graph.clear()
        depots = self.entry_depots.text().split()
        destinations = self.entry_destinations.text().split()
        arcs = self.entry_arcs.text().split(',')
        
        for depot in depots:
            self.graph.add_edge("S", depot, capacity=10)
        for dest in destinations:
            self.graph.add_edge(dest, "T", capacity=10)
        for arc in arcs:
            try:
                u, v, c = arc.split()
                self.graph.add_edge(u, v, capacity=int(c))
            except ValueError:
                continue

        max_flot, resid_graph = self.flot_max(self.graph, "S", "T")
        QMessageBox.information(self, "Résultat", f"Flot maximal: {max_flot}")
        
        self.dessiner_graphe(resid_graph)

    def dessiner_graphe(self, graph):
        self.ax.clear()
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', ax=self.ax)
        edge_labels = nx.get_edge_attributes(graph, 'capacity')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlotMaxApp()
    window.show()
    sys.exit(app.exec_())