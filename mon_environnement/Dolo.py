import os
import sys
import json
import csv
import xml.etree.ElementTree as ET
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Convertisseur de fichiers")
        self.setFixedSize(1000, 600)

        # Étiquette pour le nom du fichier
        self.fileNameLabel = QLabel("Nom du fichier :")
        self.fileNameLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Champ de saisie pour le nom du fichier
        self.fileNameInput = QLineEdit()

        # Bouton pour choisir un fichier
        self.chooseFileButton = QPushButton("Choisir un fichier")
        self.chooseFileButton.clicked.connect(self.choose_file)

        # Étiquette pour le format détecté
        self.detectedFormatLabel = QLabel("Format détecté :")
        self.detectedFormatLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Combobox pour choisir le format de sortie
        self.outputFormatComboBox = QComboBox()
        self.outputFormatComboBox.addItems(["XML", "JSON", "CSV", "XSL", "YAML"])

        # Bouton pour convertir le fichier
        self.convertButton = QPushButton("Convertir")
        self.convertButton.clicked.connect(self.convert_file)

        # Organisation des widgets dans un layout vertical
        layout = QVBoxLayout()
        layout.addWidget(self.fileNameLabel)
        layout.addWidget(self.fileNameInput)
        layout.addWidget(self.chooseFileButton)
        layout.addWidget(self.detectedFormatLabel)
        layout.addWidget(self.outputFormatComboBox)
        layout.addWidget(self.convertButton)

        # Définir le layout principal de la fenêtre
        self.setLayout(layout)

    def choose_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "Tous les fichiers (*.*)")
        if filename:
            self.fileNameInput.setText(filename)
            self.detect_format(filename)

    def detect_format(self, filename):
        extension = os.path.splitext(filename)[1]
        if extension == ".xml":
            detected_format = "XML"
        elif extension == ".json":
            detected_format = "JSON"
        elif extension == ".csv":
            detected_format = "CSV"
        elif extension == ".xsl":
            detected_format = "XSL"
        elif extension == ".yaml":
            detected_format = "YAML"
        else:
            detected_format = "Format inconnu"
        self.detectedFormatLabel.setText(f"Format détecté : {detected_format}")

    def convert_file(self):
        filename = self.fileNameInput.text()
        output_format =self.outputFormatComboBox.currentText()

        if not filename:
            QMessageBox.warning(self, "Erreur", "Veuillez choisir un fichier à convertir.")
            return

        try:
            # Détecter le format du fichier d'origine
            detected_format = detect_format(filename)

            # Lire le contenu du fichier
            content = read_file(filename, detected_format)

            # Écrire le contenu dans le format de sortie choisi
            new_filename = os.path.join(os.path.dirname(filename), f"{os.path.splitext(os.path.basename(filename))[0]}.{output_format.lower()}")
            write_file(new_filename, output_format, content)

            QMessageBox.information(self, "Succès", f"Le fichier a été converti avec succès au format {output_format}.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la conversion du fichier : {e}")

# Fonction detect_format corrigée
def detect_format(filename):
    extension = os.path.splitext(filename)[1]
    if extension == ".xml":
        return "XML"
    elif extension == ".json":
        return "JSON"
    elif extension == ".csv":
        return "CSV"
    elif extension == ".xsl":
        return "XSL"
    elif extension == ".yaml":
        return "YAML"
    else:
        return "Format inconnu"

# Fonction read_file
def read_file(filename, format):
    if format == "XML":
        tree = ET.parse(filename)
        root = tree.getroot()
        return root
    elif format == "JSON":
        with open(filename, 'r') as f:
            return json.load(f)
    elif format == "CSV":
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            return list(reader)
    elif format == "XSL":
        with open(filename, 'r') as f:
            return f.read()
    elif format == "YAML":
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    else:
        raise Exception("Format de fichier non pris en charge")

# Fonction write_file
def write_file(filename, format, content):
    if format == "XML":
        root = ET.Element("data")
        for key, value in content.items():
            element = ET.Element(key)
            element.text = value
            root.append(element)
        tree = ET.ElementTree(root)
        tree.write(filename)
    elif format == "JSON":
        with open(filename, 'w') as f:
            json.dump(content, f, indent=4)
    elif format == "CSV":
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in content:
                writer.writerow(row)
    elif format == "XSL":
        with open(filename, 'w') as f:
            f.write(content)
    elif format == "YAML":
        with open(filename, 'w') as f:
            yaml.dump(content, f)
    else:
        raise Exception("Format de fichier non pris en charge")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())