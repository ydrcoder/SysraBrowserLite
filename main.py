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
        "role": "Kurucu Hesabı"
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
        self.setWindowTitle("Sysra Web Tarayıcı Giriş")
        self.setFixedSize(360, 240)

        layout = QVBoxLayout()

        self.title = QLabel("🌐 Sysra Tarayıcıya Giriş Yap")
        layout.addWidget(self.title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı Adı (isteğe bağlı)")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Yönetici Şifresi (isteğe bağlı)")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.create_button = QPushButton("Yeni Kullanıcı Oluştur")
        self.create_button.clicked.connect(self.create_user)
        layout.addWidget(self.create_button)

        self.anon_button = QPushButton("🔓 Anonim Devam Et")
        self.anon_button.clicked.connect(self.anonymous_login)
        layout.addWidget(self.anon_button)

        self.setLayout(layout)

    def handle_login(self):
        name = self.username.text().strip()
        pwd = self.password.text().strip()

        if name in ADMIN_ACCOUNTS:
            if pwd == ADMIN_ACCOUNTS[name]["password"]:
                QMessageBox.information(self, "Giriş Başarılı", f"{ADMIN_ACCOUNTS[name]['role']} olarak giriş yapıldı.")
                self.launch_browser(name)
            else:
                QMessageBox.warning(self, "Şifre Hatalı", "Yönetici şifresi yanlış.")
        else:
            users = load_users()
            if name in users:
                QMessageBox.information(self, "Hoşgeldin", f"{name} ile giriş yapıldı.")
                self.launch_browser(name)
            else:
                QMessageBox.warning(self, "Kullanıcı Yok", "Bu kullanıcı kayıtlı değil.")

    def create_user(self):
        name = self.username.text().strip()
        if not name:
            QMessageBox.warning(self, "Uyarı", "Kullanıcı adı boş olamaz.")
            return
        save_user(name)
        QMessageBox.information(self, "Başarılı", f"{name} adlı kullanıcı oluşturuldu.")

    def anonymous_login(self):
        self.launch_browser("Anonim")

    def launch_browser(self, username):
        try:
            browser_path = os.path.join(os.path.dirname(__file__), "sysrabrowser.py")
            subprocess.Popen([sys.executable, browser_path, username])
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Tarayıcı açılamadı:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = LoginWindow()
    pencere.show()
    sys.exit(app.exec_())

