import sys
import wikipediaapi
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt

class WikipediaSummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wikipedia Summarizer")
        self.setGeometry(100, 100, 600, 400)

        # Widgets
        self.topic_label = QLabel("Inserisci l'argomento da cercare:")
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Es. Austria, Photosynthesis, etc.")
        self.search_button = QPushButton("Cerca e Riassumi")
        self.search_button.clicked.connect(self.on_search_clicked)

        self.result_label = QLabel("Riassunto:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.topic_label)
        input_layout.addWidget(self.topic_input)
        input_layout.addWidget(self.search_button)

        layout.addLayout(input_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Carica il modello e il tokenizer una volta sola
        self.model_name = "sshleifer/distilbart-cnn-6-6"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def on_search_clicked(self):
        argomento = self.topic_input.text().strip()
        if not argomento:
            self.result_text.setPlainText("Inserisci un argomento valido.")
            return

        # Ricerca su Wikipedia
        testo = self.ricerca_wikipedia(argomento, lingua="en")
        if not testo:
            self.result_text.setPlainText("Argomento non trovato su Wikipedia.")
            return

        # Sintetizza il testo
        riassunto = self.sintetizza_testo(testo)
        self.result_text.setPlainText(riassunto)

    def ricerca_wikipedia(self, argomento, lingua="en"):
        headers = {'User-Agent': 'VisioWikiAI/1.0 (carlo.ratti@example.com)'}
        wiki = wikipediaapi.Wikipedia(lingua, headers=headers)
        pagina = wiki.page(argomento)
        if pagina.exists():
            return pagina.text
        else:
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
        riassunto = " ".join(riassunto.split())
        return riassunto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WikipediaSummarizerApp()
    window.show()
    sys.exit(app.exec_())