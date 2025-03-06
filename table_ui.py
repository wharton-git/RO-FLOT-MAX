# table_ui.py
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, QTableView, QWidget
from PyQt5.QtCore import pyqtSignal
import numpy as np
from table_logic import MyTableModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QTableView, QVBoxLayout, QWidget, QPushButton, QInputDialog
from table_logic import MyTableModel
from PyQt5.QtCore import Qt

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tableau Dynamique avec Graphique")

        # Initialisation du splitter
        self.splitter = QSplitter(Qt.Horizontal)

        # Création du canvas Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.splitter.addWidget(self.canvas)

        # Création du conteneur principal
        self.layout = QVBoxLayout(self)

        # Création d'un bouton pour configurer le tableau
        self.config_button = QPushButton("Configurer le tableau", self)
        self.config_button.clicked.connect(self.open_config_dialog)

        # Initialisation du tableau avec des valeurs 0
        self.setup_table(["A", "B", "C"], ["X", "Y"])

        # Ajout des widgets
        self.layout.addWidget(self.splitter)
        self.layout.addWidget(self.config_button)

    def setup_table(self, row_labels, col_labels):
        """Initialise ou met à jour le tableau et le graphique."""
        self.row_labels = row_labels
        self.col_labels = col_labels

        # Création d'un tableau rempli de 0
        data = np.zeros((len(row_labels), len(col_labels))).tolist()
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
        """Met à jour le graphique lorsque les données changent."""
        self.plot_graph()

    def open_config_dialog(self):
        """Ouvre une fenêtre pop-up pour configurer le tableau."""
        dialog = InputDialog(self)
        if dialog.exec_():
            rows, cols = dialog.get_inputs()
            if rows and cols:  # Vérifie que les entrées ne sont pas vides
                self.setup_table(rows, cols)
