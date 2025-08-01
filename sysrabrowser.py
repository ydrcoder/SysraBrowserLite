import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel,
    QComboBox, QSplitter, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from deep_translator import GoogleTranslator

NOTES_FILE = "sysra_notes.txt"


class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        homepage = os.path.join(os.path.dirname(__file__), "sysra_home.html")
        self.browser.setUrl(QUrl.fromLocalFile(homepage))

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search query...")
        self.url_bar.returnPressed.connect(self.navigate)

        nav = QHBoxLayout()
        for sym, func in [("←", self.browser.back), ("→", self.browser.forward), ("⟳", self.browser.reload)]:
            btn = QPushButton(sym)
            btn.setFixedWidth(30)
            btn.clicked.connect(func)
            nav.addWidget(btn)

        nav.addWidget(self.url_bar)
        layout.addLayout(nav)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.browser.urlChanged.connect(lambda u: self.url_bar.setText(u.toString()))
        self.browser.titleChanged.connect(lambda t: self.update_tab_title(t))

    def update_tab_title(self, title):
        parent = self.parentWidget()
        if parent:
            main_window = parent.parentWidget()
            if main_window and hasattr(main_window, "tabs"):
                index = main_window.tabs.indexOf(self)
                if index != -1:
                    main_window.tabs.setTabText(index, title if title else "New Tab")

    def navigate(self):
        val = self.url_bar.text().strip()
        if not val:
            return
        if val.startswith("http"):
            url = val
        elif "." in val and " " not in val:
            url = "https://" + val
        else:
            url = f"https://duckduckgo.com/?q={val.replace(' ', '+')}"
        self.browser.setUrl(QUrl(url))


class TranslateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("🌐 Sysra Translate")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        lang_h = QHBoxLayout()
        self.from_lang = QComboBox()
        self.to_lang = QComboBox()
        langs = {"auto": "Detect", "en": "English", "tr": "Turkish", "de": "German", "fr": "French", "es": "Spanish"}
        for code, name in langs.items():
            self.from_lang.addItem(name, userData=code)
            self.to_lang.addItem(name, userData=code)
        self.from_lang.setCurrentIndex(0)
        self.to_lang.setCurrentIndex(1)
        lang_h.addWidget(self.from_lang)
        lang_h.addWidget(QLabel("→"))
        lang_h.addWidget(self.to_lang)
        layout.addLayout(lang_h)

        self.input = QTextEdit()
        self.input.setPlaceholderText("Enter text to translate...")
        layout.addWidget(self.input)

        self.btn = QPushButton("Translate")
        self.btn.clicked.connect(self.do_translate)
        layout.addWidget(self.btn)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText("Translation will appear here...")
        layout.addWidget(self.result)

        self.setLayout(layout)
        self.translator = GoogleTranslator(source='auto', target='en')

    def do_translate(self):
        text = self.input.toPlainText().strip()
        if not text:
            self.result.setPlainText("⚠️ No text entered.")
            return
        src = self.from_lang.currentData()
        tgt = self.to_lang.currentData()
        try:
            self.translator = GoogleTranslator(source=src, target=tgt)
            translated = self.translator.translate(text)
            self.result.setPlainText(translated)
        except Exception as e:
            self.result.setPlainText("Error: " + str(e))


class NotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("📝 Sysra Notes")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.save_btn = QPushButton("Save Notes")
        self.save_btn.clicked.connect(self.save_notes)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_notes()

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())

    def save_notes(self):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write(self.text_edit.toPlainText())
        QMessageBox.information(self, "Saved", "Notes saved successfully.")


class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("🧮 Sysra Calculator")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        input_layout = QHBoxLayout()
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Number 1")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Number 2")
        input_layout.addWidget(self.input1)
        input_layout.addWidget(self.input2)
        layout.addLayout(input_layout)

        btn_layout = QHBoxLayout()
        for sym, func in [("+", self.add), ("-", self.sub), ("*", self.mul), ("/", self.div)]:
            btn = QPushButton(sym)
            btn.clicked.connect(func)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.result = QLabel("Result: ")
        self.result.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result)

        self.setLayout(layout)

    def get_inputs(self):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())
            return num1, num2
        except ValueError:
            QMessageBox.warning(self, "Input error", "Please enter valid numbers.")
            return None, None

    def add(self):
        nums = self.get_inputs()
        if nums is not None:
            self.result.setText(f"Result: {nums[0] + nums[1]}")

    def sub(self):
        nums = self.get_inputs()
        if nums is not None:
            self.result.setText(f"Result: {nums[0] - nums[1]}")

    def mul(self):
        nums = self.get_inputs()
        if nums is not None:
            self.result.setText(f"Result: {nums[0] * nums[1]}")

    def div(self):
        nums = self.get_inputs()
        if nums is not None:
            if nums[1] == 0:
                QMessageBox.warning(self, "Math error", "Cannot divide by zero.")
            else:
                self.result.setText(f"Result: {nums[0] / nums[1]}")


class MainWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.setWindowTitle("Sysra Browser Lite 3.0")
        self.setGeometry(50, 50, 1200, 800)

        splitter = QSplitter(Qt.Horizontal)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tabs)

        plugin_panel = QTabWidget()
        plugin_panel.addTab(TranslateWidget(), "Translate")
        plugin_panel.addTab(NotesWidget(), "Notes")
        plugin_panel.addTab(CalculatorWidget(), "Calculator")
        splitter.addWidget(plugin_panel)

        splitter.setSizes([900, 300])
        self.setCentralWidget(splitter)

        plus = QPushButton("+")
        plus.setFixedWidth(30)
        plus.setToolTip("New Tab")
        plus.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(plus, Qt.TopRightCorner)

        self.add_tab()
        self.statusBar().showMessage(f"User: {username}")

    def add_tab(self):
        tab = BrowserTab()
        self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentWidget(tab)

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = sys.argv[1] if len(sys.argv) > 1 else "Guest"
    window = MainWindow(username=user)
    window.show()
    sys.exit(app.exec_())

