import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphe des résidus - Flot Max")
        self.setGeometry(100, 100, 800, 600)

        self.graph_data = [
            ('S', 'A', 5), ('S', 'B', 0), ('A', 'C', 0), ('A', 'S', 5),
            ('C', 'T', 5), ('C', 'A', 5), ('C', 'B', 5), ('B', 'C', 1),
            ('B', 'S', 5), ('T', 'C', 10)
        ]

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.draw_graph()

    def draw_graph(self):
        G = nx.DiGraph()
        for u, v, capacity in self.graph_data:
            G.add_edge(u, v, weight=capacity)

        pos = nx.spring_layout(G)  # Disposition automatique
        plt.clf()

        # Dessiner le graphe
        edges = G.edges(data=True)
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in edges}

        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphVisualizer()
    window.show()
    sys.exit(app.exec_())
