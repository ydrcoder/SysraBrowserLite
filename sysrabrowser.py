import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel, QAction,
    QMessageBox, QDialog, QToolButton, QMenu, QSpacerItem, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt


class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()

        homepage_path = os.path.join(os.path.dirname(__file__), "sysra_home.html")
        self.browser.setUrl(QUrl.fromLocalFile(homepage_path))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("←")
        self.back_button.setFixedWidth(30)
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton("→")
        self.forward_button.setFixedWidth(30)
        self.forward_button.clicked.connect(self.browser.forward)

        self.reload_button = QPushButton("⟳")
        self.reload_button.setFixedWidth(30)
        self.reload_button.clicked.connect(self.browser.reload)

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.url_bar)

        self.layout.addLayout(nav_layout)
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        # Is this URL?
        if url.startswith("http://") or url.startswith("https://"):
            self.browser.setUrl(QUrl(url))
        else:
            # Domain System
            if '.' in url and ' ' not in url:
                self.browser.setUrl(QUrl("https://" + url))
            else:
                # DuckDuckGo Search
                arama = url.replace(' ', '+')
                self.browser.setUrl(QUrl(f"https://duckduckgo.com/?q={arama}"))

    def update_url(self, qurl):
        self.url_bar.setText(qurl.toString())

    def load_html(self, html):
        self.browser.setHtml(html)


class AccountPanel(QDialog):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.setWindowTitle("Account Panel")
        self.setMinimumSize(300, 200)
        self.username = username

        layout = QVBoxLayout()
        user_label = QLabel(f"User: <b>{self.username}</b>")
        layout.addWidget(user_label)

        if self.username == "ydrc":
            admin_btn = QPushButton("Admin Panel")
            admin_btn.clicked.connect(self.open_admin_panel)
            layout.addWidget(admin_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def open_admin_panel(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Admin Panel")
        dialog.setMinimumSize(300, 150)

        layout = QVBoxLayout()

        devtools_button = QPushButton("Open Dev Tools")
        devtools_button.clicked.connect(lambda: self.open_dev_tools(dialog))
        layout.addWidget(devtools_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def open_dev_tools(self, dialog):
        main_window = self.parent()
        if not hasattr(main_window, 'dev_tools'):
            main_window.dev_tools = QWebEngineView()
            main_window.dev_tools.setWindowTitle("Dev Console")
            main_window.dev_tools.resize(900, 700)

        current_tab = main_window.tabs.currentWidget()
        if current_tab:
            page = current_tab.browser.page()
            main_window.dev_tools.setPage(page)

        main_window.dev_tools.show()


class MainWindow(QMainWindow):
    def __init__(self, username="No account"):
        super().__init__()
        self.setWindowTitle("Sysra Browser Lite")
        self.setGeometry(100, 100, 1200, 800)
        self.username = username

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tabs)

        # Yeni sekme açma butonu: sekmelerin sonunda
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedWidth(30)
        self.new_tab_button.clicked.connect(self.add_new_tab)

        # Sekmelerin tab bar'ına buton eklemek için workaround:
        self.tabs.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)

        self.add_new_tab()

        menubar = self.menuBar()

        dosya_menu = menubar.addMenu("File")

        ozellestir_action = QAction("Customize Sysra", self)
        ozellestir_action.triggered.connect(self.customize)
        dosya_menu.addAction(ozellestir_action)

        # Sağ üst hesap butonu ve menü
        top_right_widget = QWidget()
        top_right_layout = QHBoxLayout()
        top_right_layout.setContentsMargins(0, 0, 0, 0)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_right_layout.addItem(spacer)

        self.account_btn = QToolButton()
        self.account_btn.setText(self.username)
        self.account_btn.setPopupMode(QToolButton.InstantPopup)

        account_menu = QMenu()
        hesap_paneli_action = QAction("Account Panel", self)
        hesap_paneli_action.triggered.connect(self.open_account_panel)
        account_menu.addAction(hesap_paneli_action)

        self.account_btn.setMenu(account_menu)

        top_right_layout.addWidget(self.account_btn)
        top_right_widget.setLayout(top_right_layout)

        menubar.setCornerWidget(top_right_widget, Qt.TopRightCorner)

        # Durum çubuğu
        if self.username == "ydrc":
            self.statusBar().showMessage(f"🛡 Login: {self.username} | Admin Mode : Active")
        else:
            self.statusBar().showMessage(f"Login: {self.username}")

    def add_new_tab(self):
        new_tab = BrowserTab()
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def customize(self):
        QMessageBox.information(self, "Customize", "Themes and options are coming soon.")

    def open_account_panel(self):
        panel = AccountPanel(self, self.username)
        panel.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    kullanici = sys.argv[1] if len(sys.argv) > 1 else "No account"

    pencere = MainWindow(username=kullanici)
    pencere.show()

    sys.exit(app.exec_())
