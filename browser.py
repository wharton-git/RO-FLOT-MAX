import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self, html_file):
        super().__init__()
        self.setWindowTitle("Visualisation du graphe")
        self.setGeometry(100, 100, 800, 600)

        # Créer un widget de navigateur web
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(html_file))
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    # Chemin vers le fichier HTML généré
    html_file = "/home/xeon/Desktop/Projects/Python/nx.html"

    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = BrowserWindow(html_file)
    window.show()

    # Exécuter l'application
    sys.exit(app.exec_())