# shipment_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont  # Если вы используете QFont


class ShipmentDialog(QDialog):
    """Диалоговое окно для создания/редактирования заказа."""

    def __init__(self, clients=None, products=None, warehouses=None, data=None):
        super().__init__()
        self.setWindowTitle("Создать/Редактировать заказ")
        self.resize(400, 600)  # Устанавливаем размер окна
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 15px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #55B2FF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #7792A8;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Отступ сверху
        main_layout.addSpacing(20)

        # Форма ввода данных заказа с отступами между полями
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)  # Отступ между элементами

        # Номер заказа
        order_number_label = QLabel("Номер заказа:")
        order_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(order_number_label)

        self.order_number_input = QLineEdit()
        self.order_number_input.setPlaceholderText("Введите номер заказа")
        self.order_number_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.order_number_input)

        # Дата заказа
        order_date_label = QLabel("Дата заказа:")
        order_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(order_date_label)

        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDate(QDate.currentDate())
        self.order_date_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.order_date_input)

        # Имя клиента
        client_label = QLabel("Имя клиента:")
        client_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(client_label)

        self.client_input = QComboBox()
        self.client_input.addItems(clients if clients else [])
        self.client_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.client_input)

        # Адрес доставки
        delivery_address_label = QLabel("Адрес доставки:")
        delivery_address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(delivery_address_label)

        self.delivery_address_input = QLineEdit()
        self.delivery_address_input.setPlaceholderText("Введите адрес доставки")
        self.delivery_address_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.delivery_address_input)

        # Товар
        product_label = QLabel("Товар:")
        product_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(product_label)

        self.product_input = QComboBox()
        self.product_input.addItems(products if products else [])
        self.product_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.product_input)

        # Склад
        warehouse_label = QLabel("Склад:")
        warehouse_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(warehouse_label)

        self.warehouse_input = QComboBox()
        self.warehouse_input.addItems(warehouses if warehouses else [])
        self.warehouse_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.warehouse_input)

        # Количество
        quantity_label = QLabel("Количество:")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(quantity_label)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Введите количество")
        self.quantity_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.quantity_input)

        # Способ доставки
        delivery_method_label = QLabel("Способ доставки:")
        delivery_method_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(delivery_method_label)

        self.delivery_method_input = QComboBox()
        self.delivery_method_input.addItems(["Автомобильная", "Железнодорожная", "Морская", "Авиадоставка"])
        self.delivery_method_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.delivery_method_input)

        # Общая сумма
        total_amount_label = QLabel("Общая сумма:")
        total_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(total_amount_label)

        self.total_amount_input = QLineEdit()
        self.total_amount_input.setPlaceholderText("0.00")
        self.total_amount_input.setReadOnly(True)
        self.total_amount_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.total_amount_input)

        # Подключение обновления общей суммы при изменении товара или количества
        self.product_input.currentIndexChanged.connect(self.update_total_amount)
        self.quantity_input.textChanged.connect(self.update_total_amount)

        # Добавляем форму в основной layout
        main_layout.addLayout(form_layout)

        # Отступ перед кнопками
        main_layout.addSpacing(20)

        # Кнопки "Создать" и "Отмена" расположенные вертикально
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)  # Отступ между кнопками

        # Кнопка "Создать"
        create_button = QPushButton("Создать")
        create_button.setFixedWidth(200)
        create_button.setFixedHeight(40)
        create_button.clicked.connect(self.create_order)
        button_layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(200)
        cancel_button.setFixedHeight(40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем кнопки в основной layout
        main_layout.addLayout(button_layout)

        # Отступ снизу
        main_layout.addSpacing(20)

        # Если данные переданы для редактирования, заполняем поля
        if data:
            self.set_data(data)

    def get_data(self):
        """Собирает данные из полей ввода и возвращает их в виде словаря."""
        return {
            "order_number": self.order_number_input.text(),
            "order_date": self.order_date_input.date().toString("yyyy-MM-dd"),
            "client": self.client_input.currentText(),
            "delivery_address": self.delivery_address_input.text(),
            "product": self.product_input.currentText(),
            "warehouse": self.warehouse_input.currentText(),
            "quantity": self.quantity_input.text(),
            "delivery_method": self.delivery_method_input.currentText(),
            "total_amount": self.total_amount_input.text()
        }

    def set_data(self, data):
        """Заполняет поля ввода данными для редактирования."""
        self.order_number_input.setText(data.get("order_number", ""))
        self.order_date_input.setDate(QDate.fromString(data.get("order_date", ""), "yyyy-MM-dd"))
        index = self.client_input.findText(data.get("client", ""))
        if index != -1:
            self.client_input.setCurrentIndex(index)
        self.delivery_address_input.setText(data.get("delivery_address", ""))
        index = self.product_input.findText(data.get("product", ""))
        if index != -1:
            self.product_input.setCurrentIndex(index)
        index = self.warehouse_input.findText(data.get("warehouse", ""))
        if index != -1:
            self.warehouse_input.setCurrentIndex(index)
        self.quantity_input.setText(data.get("quantity", ""))
        index = self.delivery_method_input.findText(data.get("delivery_method", ""))
        if index != -1:
            self.delivery_method_input.setCurrentIndex(index)
        self.total_amount_input.setText(data.get("total_amount", ""))

    def create_order(self):
        """Обработка нажатия кнопки "Создать"."""
        data = self.get_data()
        if self.validate_data(data):
            # Здесь можно добавить код для сохранения заказа в базу данных или список
            # Для примера просто закроем диалог с принятием
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        try:
            quantity = int(data["quantity"])
            if quantity <= 0:
                return False
        except ValueError:
            return False

        # Проверяем, что все обязательные поля заполнены
        required_fields = [
            data["order_number"],
            data["order_date"],
            data["client"],
            data["delivery_address"],
            data["product"],
            data["warehouse"],
            data["delivery_method"],
            data["total_amount"]
        ]
        return all(field.strip() for field in required_fields)

    def update_total_amount(self):
        """Обновляет общую сумму заказа на основе выбранного товара и количества."""
        product = self.product_input.currentText()
        quantity_text = self.quantity_input.text()
        try:
            quantity = int(quantity_text)
        except ValueError:
            quantity = 0

        # Предположим, что цена товара хранится где-то (например, в списке продуктов)
        # Для примера возьмем фиксированные цены
        product_prices = {
            "Товар 1": 100,
            "Товар 2": 200,
            "Товар 3": 150,
            "Товар 4": 250
        }
        price = product_prices.get(product, 0)
        total = price * quantity
        self.total_amount_input.setText(f"{total:.2f}")
