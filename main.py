import sys
import wikipedia
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QSplitter, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class ModelLoader(QThread):
    finished = pyqtSignal(str)

    def __init__(self, text, tokenizer, model, max_length=150):
        super().__init__()
        self.text = text
        self.tokenizer = tokenizer
        self.model = model
        self.max_length = max_length

    def run(self):
        try:
            inputs = self.tokenizer(
                self.text,
                max_length=1024,
                return_tensors="pt",
                truncation=True
            )

            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=self.max_length,
                min_length=30,
                num_beams=4,
                forced_bos_token_id=0
            )

            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summary = " ".join(summary.split())
            self.finished.emit(summary)
        except Exception as e:
            self.finished.emit(f"Error generating summary: {str(e)}")

class WikipediaSummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WikiAI | The Future of Automatic Summarization")
        self.setGeometry(100, 100, 1000, 700)

        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass

        # Load a lighter model
        self.model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

        self.init_ui()

    def init_ui(self):
        splitter = QSplitter()

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2980b9;
                border-radius: 5px;
            }
        """)

        self.add_sidebar_item("🔍 Search", 0)
        self.add_sidebar_item("💼 Business (Coming Soon)", 1)
        self.add_sidebar_item("⚙️ Settings (Coming Soon)", 2)
        self.sidebar.currentRowChanged.connect(self.switch_tab)

        self.stacked_widget = QStackedWidget()

        self.search_tab = QWidget()
        self.init_search_tab()
        self.stacked_widget.addWidget(self.search_tab)

        self.business_tab = QWidget()
        self.init_business_tab()
        self.stacked_widget.addWidget(self.business_tab)

        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.stacked_widget.addWidget(self.settings_tab)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.stacked_widget)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)
        self.apply_stylesheet()

    def add_sidebar_item(self, text, index):
        item = QListWidgetItem(text)
        item.setSizeHint(QSize(20, 40))
        self.sidebar.addItem(item)

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def init_search_tab(self):
        layout = QVBoxLayout()

        welcome_label = QLabel()
        welcome_label.setText(
            "<h1>Welcome to WikiAI!</h1>"
            "<p>We have solved the problem of automatic summarization. Now you can:</p>"
            "<ul>"
            "<li>Search for any topic on Wikipedia.</li>"
            "<li>Get clear and precise summaries in seconds.</li>"
            "<li>Save time and improve your productivity.</li>"
            "</ul>"
            "<p><b>WikiAI is your personal assistant for knowledge.</b></p>"
        )
        welcome_label.setWordWrap(True)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        search_group = QWidget()
        search_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.topic_label = QLabel("Search for a topic:")
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("E.g. Artificial Intelligence, Austria, Photosynthesis...")
        self.search_button = QPushButton("Generate Summary")
        self.search_button.clicked.connect(self.on_search_clicked)

        input_layout.addWidget(self.topic_label)
        input_layout.addWidget(self.topic_input)
        input_layout.addWidget(self.search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Your summary will appear here...")

        search_layout.addLayout(input_layout)
        search_layout.addWidget(self.result_text)
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        self.search_tab.setLayout(layout)

    def init_business_tab(self):
        layout = QVBoxLayout()
        coming_soon_label = QLabel()
        coming_soon_label.setText(
            "<h1>💼 WikiAI Business</h1>"
            "<p>We are working on a <b>professional</b> version of WikiAI with:</p>"
            "<ul>"
            "<li>Advanced summaries with premium AI models.</li>"
            "<li>Automatic translation in over 50 languages.</li>"
            "<li>Integration with business tools (Slack, Google Drive, etc.).</li>"
            "<li>Priority support and dedicated assistance.</li>"
            "</ul>"
            "<p><b>Coming Soon!</b></p>"
            "<p>Stay tuned for updates.</p>"
        )
        coming_soon_label.setWordWrap(True)
        coming_soon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(coming_soon_label)
        self.business_tab.setLayout(layout)

    def init_settings_tab(self):
        layout = QVBoxLayout()
        coming_soon_label = QLabel()
        coming_soon_label.setText(
            "<h1>⚙️ Settings</h1>"
            "<p>This section will allow you to:</p>"
            "<ul>"
            "<li>Customize the interface (dark/light theme).</li>"
            "<li>Manage language preferences.</li>"
            "<li>Configure automatic saving options.</li>"
            "<li>Access advanced settings.</li>"
            "</ul>"
            "<p><b>Coming Soon!</b></p>"
            "<p>We are working to give you maximum control over VisioWikiAI.</p>"
        )
        coming_soon_label.setWordWrap(True)
        coming_soon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(coming_soon_label)
        self.settings_tab.setLayout(layout)

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QTextEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QPushButton {
                padding: 12px 24px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QStackedWidget {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            QFrame[shape="HLine"] {
                background-color: #eee;
                margin: 10px 0;
            }
        """)

    def on_search_clicked(self):
        topic = self.topic_input.text().strip()
        if not topic:
            self.result_text.setPlainText("⚠️ Please enter a valid topic.")
            return

        self.result_text.setPlainText("🔍 Searching...")

        text = self.search_wikipedia(topic, language="en")
        if not text:
            self.result_text.setPlainText("❌ Topic not found on Wikipedia. Try a different term!")
            return

        self.result_text.setPlainText("🤖 Generating summary...")
        self.loader = ModelLoader(text, self.tokenizer, self.model)
        self.loader.finished.connect(self.on_summary_generated)
        self.loader.start()

    def on_summary_generated(self, summary):
        self.result_text.setPlainText(summary)

    def search_wikipedia(self, topic, language="en"):
        """Search for a topic on Wikipedia and return the page content."""
        wikipedia.set_lang(language)
        try:
            page = wikipedia.page(topic)
            return page.content
        except wikipedia.exceptions.PageError:
            return None
        except wikipedia.exceptions.DisambiguationError:
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WikipediaSummarizerApp()
    window.show()
    sys.exit(app.exec_())
