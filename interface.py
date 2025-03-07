import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QTableView, QVBoxLayout, 
                            QWidget, QPushButton, QDialog, QLineEdit, QFormLayout, QTextEdit)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as netx

class MyTableModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex, list)

    def __init__(self, data, row_labels, col_labels):
        super().__init__()
        self._data = data
        self.row_labels = row_labels
        self.col_labels = col_labels

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]
        return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                # Convertir la valeur en entier
                self._data[index.row()][index.column()] = int(value)
                self.dataChanged.emit(index, index, [Qt.DisplayRole])
                return True
            except ValueError:
                return False
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.col_labels[section]
            elif orientation == Qt.Vertical:
                return self.row_labels[section]
        return None

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créer un nouveau tableau")

        layout = QFormLayout()
        self.row_input = QLineEdit(self)
        self.col_input = QLineEdit(self)

        layout.addRow("Entrer les lignes du tableau (séparer par des virgules) :", self.row_input)
        layout.addRow("Entrer les colonnes du tableau (séparer par des virgules) :", self.col_input)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_inputs(self):
        rows = [x.strip() for x in self.row_input.text().split(",") if x.strip()]
        cols = [x.strip() for x in self.col_input.text().split(",") if x.strip()]
        return rows, cols

class FictiveValuesDialog(QDialog):
    def __init__(self, row_labels, col_labels, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Définir les valeurs fictives")

        self.layout = QFormLayout()
        self.inputs = {}
        
        # Champs pour S -> A, S -> B, S -> C
        for row in row_labels:
            label = f"Valeur de S → {row} :"
            self.inputs[("S", row)] = QLineEdit(self)
            self.layout.addRow(label, self.inputs[("S", row)])

        # Champs pour X -> T, Y -> T
        for col in col_labels:
            label = f"Valeur de {col} → T :"
            self.inputs[(col, "T")] = QLineEdit(self)
            self.layout.addRow(label, self.inputs[(col, "T")])

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_fictive_values(self):
        return {key: int(value.text()) if value.text().isdigit() else 0 for key, value in self.inputs.items()}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tableau Dynamique avec Graphique")

        self.fictive_values = {}  # Ajouter cet attribut pour stocker les valeurs fictives

        # Initialisation du splitter
        splitter = QSplitter(Qt.Horizontal)

        # Création du canvas Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        splitter.addWidget(self.canvas)

        # Création du conteneur principal
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)

        # Création d'un bouton pour configurer le tableau
        self.config_button = QPushButton("Configurer le tableau", self)
        self.config_button.clicked.connect(self.open_config_dialog)

        # Création du widget pour afficher les informations de la table
        self.table_info_display = QTextEdit(self)
        self.table_info_display.setReadOnly(True)  # Rendre le QTextEdit non éditable

        # Initialisation du tableau avec des valeurs par défaut
        self.setup_table(["A", "B", "C"], ["X", "Y"])

        # Ajout des widgets
        self.layout.addWidget(splitter)
        self.layout.addWidget(self.config_button)

        # Affichage des informations de la table à côté
        self.layout.addWidget(self.table_info_display)

        self.setCentralWidget(central_widget)

        # Maximiser la fenêtre
        self.showMaximized()
        
    def display_table_info(self, table_info):
        """Affiche les informations de la table dans la console."""
        print("Informations de la table :")
        for row, col, value in table_info:
            print(f"({row}, {col}, {value})")
    
    def calcule_flot_max(self, table_info):
        G = netx.DiGraph()
        edge = []
        for row, col, value in table_info:
            edge.append((row, col, value))
        for d, f, cap in edge:
            G.add_edge(d, f, capacity=cap)

        source = "S"
        destination = "T"

        max_flot, resid_graph = self.flot_max(G, source, destination)
        # Affichage des flux sur chaque arc
        for u, v in G.edges():
            print(f"Flux de {u} → {v} : {resid_graph [u][v]} / {G[u][v]['capacity']}")
            
        print(f"Flot maximal: {max_flot}")
        print("Graphe des résidus:", [(d, f, resid_graph[d][f]['capacity']) for d, f in resid_graph.edges])

    # Ajoutez cette méthode pour mettre à jour les valeurs fictives
    def update_fictive_values(self, fictive_values):
        """Met à jour les valeurs fictives en gardant la plus récente."""
        for (r, c), value in fictive_values.items():
            # Mettre à jour ou ajouter la nouvelle valeur (la plus récente)
            self.fictive_values[(r, c)] = value

        self.update_table_info_display()
        
    def setup_table(self, row_labels, col_labels):
        """Initialise ou met à jour le tableau et le graphique."""
        self.row_labels = row_labels
        self.col_labels = col_labels

        # Initialisation du tableau avec des valeurs à 0
        data = np.zeros((len(row_labels), len(col_labels)), dtype=int).tolist()
        self.model = MyTableModel(data, row_labels, col_labels)

        # Création du QTableView
        if hasattr(self, "table_view"):  # Vérifie si le tableau existe déjà
            self.layout.removeWidget(self.table_view)
            self.table_view.deleteLater()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.layout.insertWidget(0, self.table_view)  # Ajoute avant le splitter

        # Connexion pour mettre à jour le graphique
        self.model.dataChanged.connect(self.update_graph)

        # Mise à jour du graphique
        self.plot_graph()

        # Créer la variable avec les tuples comme demandé
        self.table_info = self.get_table_info()

        # Afficher les informations dans le QTextEdit
        self.update_table_info_display()

    def get_table_info(self):
        """Retourne les informations sous la forme d'une liste de tuples, y compris les valeurs fictives S et T."""
        table_info = []
        
        # Connexions de "S" aux lignes et des lignes aux colonnes
        for i, row in enumerate(self.model._data):
            table_info.append(("S", self.model.row_labels[i], 0))  # Connexion fictive "S" -> ligne
            
            for j, value in enumerate(row):
                table_info.append((self.model.row_labels[i], self.model.col_labels[j], value))  # Ligne -> Colonne
        
        # Connexions des colonnes vers "T" (une seule fois)
        for col in self.model.col_labels:
            table_info.append((col, "T", 0))  # Connexion unique pour chaque colonne

        return table_info

    def update_table_info_display(self):
        """Met à jour l'affichage des informations de la table avec les valeurs fictives."""
        table_info_text = "\n".join([f"({r}, {c}, {v})" for r, c, v in self.table_info])
        self.table_info_display.setPlainText(table_info_text)

    def plot_graph(self):
        """Trace le graphique initial avec légende."""
        self.ax.clear()
        self.ax.set_title("Graphique des données")
        self.ax.set_xlabel("Catégories")
        self.ax.set_ylabel("Valeurs")
        self.ax.grid(True)

        x = np.arange(len(self.model.col_labels))
        for i, row in enumerate(self.model._data):
            self.ax.plot(x, row, marker="o", linestyle="-", label=self.model.row_labels[i])

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.model.col_labels)
        self.ax.legend()
        self.canvas.draw()

    def update_graph(self):
        """Met à jour le graphique et les informations de la table."""
        self.plot_graph()

        # Mise à jour de table_info
        self.table_info = self.get_table_info()

        # Ajout des valeurs fictives en prenant la plus récente
        for (r, c), v in self.fictive_values.items():
            # Si la combinaison existe déjà dans table_info, on la met à jour avec la plus récente
            for i, entry in enumerate(self.table_info):
                if entry[0] == r and entry[1] == c:
                    # Mise à jour directement dans table_info sans chercher par index
                    self.table_info[i] = (r, c, v)  # Remplace l'entrée existante
                    break
            else:
                # Si l'entrée n'existe pas, on l'ajoute
                self.table_info.append((r, c, v))

        # Mise à jour de l'affichage de table_info
        self.update_table_info_display()
        self.display_table_info(self.table_info)
        self.calcule_flot_max(self.table_info)


    def open_config_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec_():
            rows, cols = dialog.get_inputs()
            if rows and cols:
                self.setup_table(rows, cols)
                self.open_fictive_values_dialog(rows, cols)

    def open_fictive_values_dialog(self, row_labels, col_labels):
        dialog = FictiveValuesDialog(row_labels, col_labels, self)
        if dialog.exec_():
            fictive_values = dialog.get_fictive_values()
            
            # Mettre à jour les valeurs fictives
            self.update_fictive_values(fictive_values)
        
            # Mettre à jour les valeurs existantes dans table_info
            for (r, c), value in fictive_values.items():
                for i, (row, col, v) in enumerate(self.table_info):
                    if row == r and col == c:
                        self.table_info[i] = (row, col, value)  # Mettre à jour la valeur existante
            
            # Mettre à jour l'affichage
            self.update_table_info_display()
            
            
    #Algo de Ford-Fulkerson pour resoudre Flot-max        
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
