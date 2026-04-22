import sys
import wikipedia
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QTabWidget,
    QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class WikipediaSummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisioWikiAI")
        self.setGeometry(100, 100, 800, 600)

        # Imposta l'icona (opzionale)
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass

        # Carica il modello e il tokenizer
        self.model_name = "sshleifer/distilbart-cnn-6-6"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

        # Crea i widget principali
        self.init_ui()

    def init_ui(self):
        # Crea un QTabWidget per i pannelli
        self.tabs = QTabWidget()

        # Pannello principale per la ricerca
        self.search_tab = QWidget()
        self.init_search_tab()
        self.tabs.addTab(self.search_tab, "Ricerca")

        # Pannello per il tutorial
        self.tutorial_tab = QWidget()
        self.init_tutorial_tab()
        self.tabs.addTab(self.tutorial_tab, "Tutorial")

        # Pannello per le impostazioni
        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.tabs.addTab(self.settings_tab, "Impostazioni")

        # Imposta il layout principale
        self.setCentralWidget(self.tabs)

        # Applica lo stile
        self.apply_stylesheet()

    def init_search_tab(self):
        # Layout principale per il pannello di ricerca
        layout = QVBoxLayout()

        # Gruppo per la ricerca
        search_group = QGroupBox("Cerca su Wikipedia")
        search_layout = QVBoxLayout()

        # Widget per l'input
        input_layout = QHBoxLayout()
        self.topic_label = QLabel("Argomento:")
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Es. Austria, Photosynthesis, Python...")
        self.search_button = QPushButton("Cerca e Riassumi")
        self.search_button.clicked.connect(self.on_search_clicked)

        input_layout.addWidget(self.topic_label)
        input_layout.addWidget(self.topic_input)
        input_layout.addWidget(self.search_button)

        # Aggiungi il layout di input al gruppo
        search_layout.addLayout(input_layout)

        # Widget per il risultato
        result_group = QGroupBox("Riassunto")
        result_layout = QVBoxLayout()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # Imposta il colore di sfondo e testo per result_text
        self.result_text.setStyleSheet("background-color: white; color: black;")
        self.topic_input.setStyleSheet("background-color: white; color: black;")

        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)

        # Aggiungi i gruppi al layout principale
        search_layout.addWidget(result_group)
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        # Imposta il layout per il pannello di ricerca
        self.search_tab.setLayout(layout)

    def init_tutorial_tab(self):
        # Layout per il pannello del tutorial
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Contenuto del tutorial
        tutorial_content = QWidget()
        tutorial_layout = QVBoxLayout()

        tutorial_label = QLabel()
        tutorial_label.setText(
            "<h1>Benvenuto in VisioWikiAI!</h1>"
            "<p>Questa applicazione ti permette di:</p>"
            "<ul>"
            "<li>Cercare argomenti su <b>Wikipedia</b>.</li>"
            "<li>Generare <b>riassunti automatici</b> usando l'intelligenza artificiale.</li>"
            "<li>Salvare e consultare i risultati.</li>"
            "</ul>"
            "<h2>Come usare l'app:</h2>"
            "<ol>"
            "<li>Inserisci un argomento nel campo di ricerca (es. 'Austria').</li>"
            "<li>Clicca su <b>Cerca e Riassumi</b>.</li>"
            "<li>Leggi il riassunto generato automaticamente.</li>"
            "</ol>"
            "<h2>Suggerimenti:</h2>"
            "<ul>"
            "<li>Usa argomenti specifici per risultati migliori.</li>"
            "<li>Se l'argomento non viene trovato, prova con un termine più generico.</li>"
            "</ul>"
        )
        tutorial_label.setWordWrap(True)
        tutorial_label.setAlignment(Qt.AlignLeft)
        tutorial_layout.addWidget(tutorial_label)
        tutorial_content.setLayout(tutorial_layout)
        scroll.setWidget(tutorial_content)
        layout.addWidget(scroll)
        self.tutorial_tab.setLayout(layout)

    def init_settings_tab(self):
        # Layout per il pannello delle impostazioni
        layout = QVBoxLayout()
        settings_label = QLabel("Impostazioni di VisioWikiAI (coming soon)")
        settings_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(settings_label)

        # Aggiungi altre impostazioni qui in futuro
        info_label = QLabel("Versione 1.0.0\n\nFunzionalità avanzate in arrivo!")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        self.settings_tab.setLayout(layout)

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QGroupBox {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                color: black;
            }
            QLabel {
                font-size: 14px;
                color: black;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QTextEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 8px 16px;
                background-color: #f0f2f5;
                border: none;
                border-radius: 5px 5px 0 0;
                color: black;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

    def on_search_clicked(self):
        argomento = self.topic_input.text().strip()
        if not argomento:
            self.result_text.setPlainText("⚠️ Inserisci un argomento valido.")
            return

        # Mostra un messaggio di attesa
        self.result_text.setPlainText("🔍 Ricerca in corso...")

        # Ricerca su Wikipedia (in inglese)
        testo = self.ricerca_wikipedia(argomento, lingua="en")
        if not testo:
            self.result_text.setPlainText("❌ Argomento non trovato su Wikipedia.")
            return

        # Sintetizza il testo
        try:
            riassunto = self.sintetizza_testo(testo)
            self.result_text.setPlainText(riassunto)
        except Exception as e:
            self.result_text.setPlainText(f"❌ Errore nella generazione del riassunto: {str(e)}")

    def ricerca_wikipedia(self, argomento, lingua="en"):
        """Cerca un argomento su Wikipedia e restituisce il testo della pagina."""
        wikipedia.set_lang(lingua)
        try:
            pagina = wikipedia.page(argomento)
            return pagina.content
        except wikipedia.exceptions.PageError:
            return None
        except wikipedia.exceptions.DisambiguationError:
            return None

    def sintetizza_testo(self, testo, max_length=150):
        inputs = self.tokenizer(
            testo,
            max_length=1024,
            return_tensors="pt",
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=30,
            num_beams=4,
            forced_bos_token_id=0
        )

        riassunto = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        riassunto = " ".join(riassunto.split())  # Pulisce spazi doppi
        return riassunto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WikipediaSummarizerApp()
    window.show()
    sys.exit(app.exec_())
