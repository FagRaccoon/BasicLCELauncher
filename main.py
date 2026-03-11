import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSettings, Qt
import subprocess
import linecache

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

client = r"Minecraft.Client.exe"
creds = "userInfo.txt"

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("!!!")
        self.resize(200, 100)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("You need to enter a username"), alignment=Qt.AlignCenter)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.setWindowTitle("Basic LCEMP Launcher")
        self.setWindowIcon(QIcon(resource_path("assets/cool.ico")))
        self.setGeometry(700, 300, 500, 500)
        self.setFixedSize(500, 250)

        self.initUI()

    def initUI(self):
        self.logo = QLabel()
        pixmap = QPixmap(resource_path("assets/title.png"))
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)

        self.username = QLineEdit(self)
        if os.path.exists(creds):
            username = linecache.getline(creds, 1).strip("\n")
            if username and username.strip():
                self.username.setText(username)
            else:
                self.username.setPlaceholderText("Username...")
        else:
            self.username.setPlaceholderText("Username...")

        self.ip = QLineEdit(self)
        if os.path.exists(creds):
            ip = linecache.getline(creds, 2).strip("\n")
            if ip and ip.strip():
                self.ip.setText(ip)
            else:
                self.ip.setPlaceholderText("IP...")
        else:
            self.ip.setPlaceholderText("IP...")

        self.port = QLineEdit(self)
        if os.path.exists(creds):
            port = linecache.getline(creds, 3).strip("\n")
            if port and port.strip():
                self.port.setText(port)
            else:
                self.port.setPlaceholderText("Port...")
        else:
            self.port.setPlaceholderText("Port...")

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.onClick)

        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.username)
        layout.addWidget(self.ip)
        layout.addWidget(self.port)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def onClick(self):
        userText = str(self.username.text())
        ipText = str(self.ip.text())
        portText = str(self.port.text())
        if userText:
            subprocess.Popen([client, "-name", userText, "-ip", ipText])
            #print("print")
            with open(creds, "w") as f:
                f.write(userText + "\n")
                f.write(ipText + "\n")
                f.write(portText)
            self.lineSave()
        else:
            self.sub = SubWindow()
            self.sub.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()