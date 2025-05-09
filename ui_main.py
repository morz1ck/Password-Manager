
import traceback
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from db import get_entry, insert_entry, entry_exists, delete_entry
from crypto import encrypt, decrypt
import pyperclip as pyp
import random
import string
version = '1.0.0'

class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить новый пароль")

        layout = QFormLayout(self)

        self.service_input = QLineEdit()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.comment_input = QLineEdit()

        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)

        self.generate_btn = QPushButton("Сгенерировать")
        self.generate_btn.clicked.connect(self.generate_password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_btn)
        password_layout.addWidget(self.generate_btn)

        layout.addRow("Сервис:", self.service_input)
        layout.addRow("Логин:", self.login_input)
        layout.addRow("Пароль:", password_layout)
        layout.addRow("Комментарий:", self.comment_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            parent=self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addRow(self.buttons)

    def toggle_password_visibility(self, checked):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def generate_password(self):
        length = 12
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_input.setText(password)


class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Password Manager: version {version}, by morz1ck.")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Сервис", "Логин", "Пароль", "Комментарий"])
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        self.top_buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить пароль")
        self.add_btn.clicked.connect(self.show_add_dialog)

        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.load_data)

        self.copy_btn = QPushButton("Скопировать пароль")
        self.copy_btn.clicked.connect(self.copy_password)

        self.top_buttons_layout.addWidget(self.add_btn)
        self.top_buttons_layout.addWidget(self.refresh_btn)
        self.top_buttons_layout.addWidget(self.copy_btn)

        self.layout.addLayout(self.top_buttons_layout)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self._handle_delete)
        self.layout.addWidget(self.delete_btn)
        self.delete_btn.setFixedWidth(790)

        self.delete_btn.setStyleSheet('''
            QPushButton {
                background-color: #ff4444;
                color: white;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        ''')

    def _handle_delete(self):
        try:
            self.delete_selected_entry()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить удаление: {str(e)}")
            print(f"Ошибка удаления: {traceback.format_exc()}")

    def delete_selected_entry(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            item = self.table.item(selected_row, 0)
            if item:
                entry_id = item.data(Qt.UserRole)
                confirm = QMessageBox.question(
                    self,
                    "Подтверждение удаления",
                    "Вы уверены, что хотите удалить этот пароль?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    if delete_entry(entry_id):
                        self.load_data()
                        QMessageBox.information(self, "Успех", "Запись успешно удалена")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")

    def show_add_dialog(self):
        dialog = AddPasswordDialog(self)
        if dialog.exec_():
            service = dialog.service_input.text().strip()
            login = dialog.login_input.text().strip()
            password = dialog.password_input.text()
            comment = dialog.comment_input.text().strip()

            if not service or not login or not password:
                QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля (Сервис, Логин, Пароль)!")
                return

            try:
                if entry_exists(service, login):
                    QMessageBox.warning(self, "Ошибка", "Запись с таким сервисом и логином уже существует!")
                    return

                encrypted_password = encrypt(password)
                insert_entry(service, login, encrypted_password, comment)
                self.load_data()
                QMessageBox.information(self, "Успех", "Пароль успешно добавлен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пароль: {str(e)}")

    def load_data(self):
        self.table.setRowCount(0)
        try:
            for row in get_entry():
                row_pos = self.table.rowCount()
                self.table.insertRow(row_pos)

                id_item = QTableWidgetItem()
                id_item.setData(Qt.UserRole, row[0])
                self.table.setItem(row_pos, 0, id_item)

                self.table.setItem(row_pos, 1, QTableWidgetItem(row[1]))
                self.table.setItem(row_pos, 2, QTableWidgetItem(row[2]))

                pwd_item = QTableWidgetItem("••••••••")
                pwd_item.setData(Qt.UserRole, row[3])
                self.table.setItem(row_pos, 3, pwd_item)

                self.table.setItem(row_pos, 4, QTableWidgetItem(row[4] if row[4] else ""))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def copy_password(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row >= 0:
                password_item = self.table.item(selected_row, 3)
                if password_item:
                    encrypted_password = password_item.data(Qt.UserRole)
                    if encrypted_password:
                        decrypted_password = decrypt(encrypted_password)
                        pyp.copy(decrypted_password)
                        QMessageBox.information(self, "Успех", "Пароль скопирован в буфер обмена!")
                        return

            QMessageBox.warning(self, "Ошибка", "Не удалось скопировать пароль: запись не выбрана или данные повреждены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при копировании: {str(e)}")