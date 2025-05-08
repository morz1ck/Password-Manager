import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from db import get_entry, insert_entry
from crypto import encrypt, decrypt
import pyperclip as pyp

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер паролей")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Сервис", "Логин", "Пароль", "Комментарий"])
        self.layout.addWidget(self.table)

        self.refresh_btn = QPushButton("Обновить таблицу")
        self.refresh_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.refresh_btn)

        self.copy_btn = QPushButton("Скопировать выбранный пароль")
        self.copy_btn.clicked.connect(self.copy_password)
        self.layout.addWidget(self.copy_btn)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        for row_data in get_entry():
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row_data[1:]):
                if col_index == 2:  # расшифровка пароля
                    value = decrypt(value)
                self.table.setItem(row_index, col_index, QTableWidgetItem(value))

    def copy_password(self):
        selected = self.table.currentRow()
        if selected != -1:
            encrypted_pw = get_entry()[selected][2]
            pw = decrypt(encrypted_pw)
            pyp.copy(pw)