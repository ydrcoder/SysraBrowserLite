import sys
import json
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

USERS_FILE = "users.json"

ADMIN_ACCOUNTS = {
    "ydrc": {
        "password": "abuzi.com123",
        "role": "Adminstrator Account"
    }
}

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_user(username):
    users = load_users()
    if username not in users:
        users.append(username)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sysra Browser Lite 2.0 Login Page")
        self.setFixedSize(360, 240)

        layout = QVBoxLayout()

        self.title = QLabel("Login to Sysra Web")
        layout.addWidget(self.title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Nickname")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.create_button = QPushButton("Create New User")
        self.create_button.clicked.connect(self.create_user)
        layout.addWidget(self.create_button)

        self.anon_button = QPushButton("Countinue as no account")
        self.anon_button.clicked.connect(self.anonymous_login)
        layout.addWidget(self.anon_button)

        self.setLayout(layout)

    def handle_login(self):
        name = self.username.text().strip()
        pwd = self.password.text().strip()

        if name in ADMIN_ACCOUNTS:
            if pwd == ADMIN_ACCOUNTS[name]["password"]:
                QMessageBox.information(self, "Hello!", f"{ADMIN_ACCOUNTS[name]['role']}")
                self.launch_browser(name)
            else:
                QMessageBox.warning(self, "Password is uncorrect.", "Password is uncorrect.")
        else:
            users = load_users()
            if name in users:
                QMessageBox.information(self, "Hello!", f"{name}")
                self.launch_browser(name)
            else:
                QMessageBox.warning(self, "No users", "This user is not registered.")

    def create_user(self):
        name = self.username.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Username cannot be empty.")
            return
        save_user(name)
        QMessageBox.information(self,f"{name} Has been registered Yay!")

    def anonymous_login(self):
        self.launch_browser("No account.")

    def launch_browser(self, username):
        try:
            browser_path = os.path.join(os.path.dirname(__file__), "sysrabrowser.py")
            subprocess.Popen([sys.executable, browser_path, username])
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Warning", f"browser could not be opened:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = LoginWindow()
    pencere.show()
    sys.exit(app.exec_())


