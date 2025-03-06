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

class ValueAssignmentDialog(QDialog):
    def __init__(self, row_labels, col_labels, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assigner les valeurs S et T")

        layout = QFormLayout()
        self.values = {}

        # Créer des champs de texte pour chaque valeur "S-ligne" et "colonne-T"
        for row in row_labels:
            self.values[f"S-{row}"] = QLineEdit(self)
            layout.addRow(f"Valeur S-{row} :", self.values[f"S-{row}"])

        for col in col_labels:
            self.values[f"{col}-T"] = QLineEdit(self)
            layout.addRow(f"Valeur {col}-T :", self.values[f"{col}-T"])

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_values(self):
        """Retourne un dictionnaire avec les valeurs des champs."""
        return {key: int(value.text()) for key, value in self.values.items() if value.text().strip().isdigit()}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tableau Dynamique avec Graphique")

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

    
    def setup_table(self, row_labels, col_labels, values=None):
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
        self.table_info = self.get_table_info(values)

        # Afficher les informations dans le QTextEdit
        self.update_table_info_display()

    def get_table_info(self, values=None):
        """Retourne les informations sous la forme d'une liste de tuples, y compris les valeurs fictives S et T."""
        table_info = []
        if values:  # Si des valeurs ont été assignées, les utiliser
            for i, row in enumerate(self.model._data):
                # Ajouter la valeur fictive "S" pour chaque ligne
                table_info.append(("S", self.model.row_labels[i], values.get(f"S-{self.model.row_labels[i]}", 0)))
                for j, value in enumerate(row):
                    # Ajouter la valeur de la table avec les indices de ligne et colonne
                    table_info.append((self.model.row_labels[i], self.model.col_labels[j], value))
                # Ajouter la valeur fictive "T" pour chaque colonne
                table_info.append((self.model.col_labels[j], "T", values.get(f"{self.model.col_labels[j]}-T", 0)))
        else:
            for i, row in enumerate(self.model._data):
                # Ajouter la valeur fictive "S" pour chaque ligne
                table_info.append(("S", self.model.row_labels[i], 0))
                for j, value in enumerate(row):
                    # Ajouter la valeur de la table avec les indices de ligne et colonne
                    table_info.append((self.model.row_labels[i], self.model.col_labels[j], value))
                # Ajouter la valeur fictive "T" pour chaque colonne
                table_info.append((self.model.col_labels[j], "T", 0))
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
        """Met à jour le graphique lorsque les données changent."""
        self.plot_graph()
        # Mettre à jour les informations de la table après modification
        self.table_info = self.get_table_info()
        self.update_table_info_display()

    def open_config_dialog(self):
            """Ouvre une fenêtre pop-up pour configurer le tableau."""
            dialog = InputDialog(self)
            if dialog.exec_():
                rows, cols = dialog.get_inputs()
                if rows and cols:  # Vérifie que les entrées ne sont pas vides
                    # Ouvre le dialogue pour assigner les valeurs S et T après la configuration du tableau
                    value_dialog = ValueAssignmentDialog(rows, cols, self)
                    if value_dialog.exec_():
                        values = value_dialog.get_values()
                        self.setup_table(rows, cols, values)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
