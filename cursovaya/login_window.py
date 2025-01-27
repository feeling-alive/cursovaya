# login_window.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton,
    QFormLayout, QLineEdit, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginDialog(QDialog):
    """Диалоговое окно для входа пользователя."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.resize(1000, 700)  # Устанавливаем начальный размер окна

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 15px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005f6a;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #008CBA;
            }
        """)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Добавление вертикального пространства сверху для центрирования элементов
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Отступ
        main_layout.addSpacing(30)

        # Форма входа
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        # Метки и поля ввода
        username_label = QLabel("Логин:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите ваш логин")
        self.username_input.setFixedWidth(250)

        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setFixedWidth(250)

        # Добавление меток и полей в форму
        form_layout.addRow(username_label, self.username_input)
        form_layout.addRow(password_label, self.password_input)

        # Добавление формы в основной layout
        main_layout.addLayout(form_layout)

        # Отступ
        main_layout.addSpacing(20)

        # Сообщение об ошибке
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label)

        # Отступ
        main_layout.addSpacing(20)

        # Кнопка "Войти" центрирована
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        login_button = QPushButton("Войти")
        login_button.setFixedWidth(300)  # Фиксированная ширина кнопки
        login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(login_button)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(button_layout)

        # Добавление вертикального пространства снизу для центрирования элементов
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("Пожалуйста, введите логин и пароль.")
            return

        if password == "123":
            self.accept()
        else:
            self.error_label.setText("Неверный пароль или логин.")
