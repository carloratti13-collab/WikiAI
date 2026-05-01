# 🌍 WikiAI

**WikiAI** is a Python application that allows you to **search for topics on Wikipedia** and **generate automatic summaries** using natural language processing (NLP) models. The application includes an **intuitive graphical user interface (GUI)** developed with **PyQt5**, making it easy to interact with the system.
## Attributions This project uses the **distilbart-cnn-6-6** model of [sshleifer](https://huggingface.co/sshleifer), released under [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0). For licensing details, see the ['third_party_licenses/'](third_party_licenses/) folder. At May of 2026 you can get the .app for MacOS and .exe Windows.

The computer need to had 8GB of RAM or more.

---

## ✨ Features
- 🔍 **Wikipedia Search**: Search for any topic on Wikipedia in multiple languages.
- 📝 **Automatic Summarization**: Generate clear and concise summaries of the retrieved text using NLP models.
- 🖥️ **Graphical User Interface**: A simple and intuitive user interface built with **PyQt5**.
- 🌐 **English supported**

---

## 🛠️ Requirements
To run **VisioWikiAI**, ensure you have **Python 3.7 or higher** installed, along with the following libraries:

### Required Libraries
- `wikipediaapi`: For searching Wikipedia.
- `transformers`: For natural language processing (NLP).
- `torch`: Backend for NLP models (PyTorch).
- `PyQt5`: For the graphical user interface.
- `sentencepiece`: Support for model tokenizers.

---

## 📥 Installation

### 1. Clone the Repository (Optional)
If you are working with a Git repository, clone it using:
```bash
git clone https://github.com/your-username/WikiAI.git
cd WikiAI

