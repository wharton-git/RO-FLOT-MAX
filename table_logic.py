# table_logic.py
import numpy as np
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QModelIndex  # Ajoute QModelIndex ici

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
                self._data[index.row()][index.column()] = float(value)
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
