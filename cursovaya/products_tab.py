# product_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QFormLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from data_manager import DataManager

class ProductDialog(QDialog):
    """Диалоговое окно для добавления/редактирования товара."""

    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать товар")
        self.resize(350, 800)
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
            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4CAF50;
            }
        """)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Отступ
        main_layout.addSpacing(20)

        # Форма ввода данных товара с метками над полями
        form_layout = QVBoxLayout()

        # Код товара
        code_label = QLabel("Код товара:")
        code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(code_label)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Введите код товара")
        self.code_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.code_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Название товара
        name_label = QLabel("Название товара:")
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        self.name_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.name_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Номер склада
        warehouse_label = QLabel("Номер склада:")
        warehouse_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(warehouse_label)

        self.warehouse_input = QComboBox()
        self.warehouse_input.addItems(["Склад 1", "Склад 2", "Склад 3"])
        self.warehouse_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.warehouse_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Поставщик
        supplier_label = QLabel("Поставщик:")
        supplier_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(supplier_label)

        self.supplier_input = QComboBox()
        self.supplier_input.addItems(["Поставщик A", "Поставщик B", "Поставщик C"])
        self.supplier_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.supplier_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Количество
        quantity_label = QLabel("Количество:")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(quantity_label)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Введите количество")
        self.quantity_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.quantity_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Цена товара
        price_label = QLabel("Цена товара:")
        price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(price_label)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Введите цену товара")
        self.price_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.price_input)

        # Отступ между полями
        form_layout.addSpacing(15)

        # Закупочная цена
        purchase_price_label = QLabel("Закупочная цена:")
        purchase_price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(purchase_price_label)

        self.purchase_price_input = QLineEdit()
        self.purchase_price_input.setPlaceholderText("Введите закупочную цену")
        self.purchase_price_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.purchase_price_input)

        main_layout.addLayout(form_layout)

        # Отступ перед кнопками
        main_layout.addSpacing(20)

        # Кнопки "Сохранить" и "Отмена" расположенные вертикально
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)  # Отступ между кнопками

        # Кнопка "Сохранить"
        save_button = QPushButton("Сохранить")
        save_button.setFixedWidth(376)
        save_button.setFixedHeight(54)
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(316)
        cancel_button.setFixedHeight(49)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем растяжение, если необходимо
        button_layout.addStretch()

        # Добавляем button_layout в основной layout
        main_layout.addLayout(button_layout)

        # Если данные переданы для редактирования, заполняем поля
        if data:
            self.set_data(data)

    def get_data(self):
        """Собирает данные из полей ввода и возвращает их в виде словаря."""
        return {
            "product_code": self.code_input.text().strip(),
            "product_name": self.name_input.text().strip(),
            "warehouse_number": self.warehouse_input.currentText(),
            "supplier": self.supplier_input.currentText(),
            "quantity": self.quantity_input.text().strip(),
            "price": self.price_input.text().strip(),
            "purchase_price": self.purchase_price_input.text().strip()
        }

    def set_data(self, data):
        """Заполняет поля ввода данными для редактирования."""
        self.code_input.setText(data.get("product_code", ""))
        self.name_input.setText(data.get("product_name", ""))
        index = self.warehouse_input.findText(data.get("warehouse_number", ""))
        if index != -1:
            self.warehouse_input.setCurrentIndex(index)
        index = self.supplier_input.findText(data.get("supplier", ""))
        if index != -1:
            self.supplier_input.setCurrentIndex(index)
        self.quantity_input.setText(str(data.get("quantity", "")))
        self.price_input.setText(str(data.get("price", "")))
        self.purchase_price_input.setText(str(data.get("purchase_price", "")))

class ProductTab(QWidget):
    """Вкладка с таблицей товаров."""

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        header_label = QLabel("<b>Управление товарами</b>")
        layout.addWidget(header_label)

        # Таблица товаров
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(7)
        self.product_table.setHorizontalHeaderLabels(
            ["Код товара", "Название товара", "Номер склада", "Поставщик", "Количество", "Цена", "Закупочная цена"]
        )
        self.product_table.horizontalHeader().setStretchLastSection(True)
        self.product_table.horizontalHeader().setDefaultSectionSize(120)
        self.product_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.product_table)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить товар")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить товар")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Подключение кнопок к методам
        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)

        self.load_data()

    def load_data(self):
        """Загружает данные товаров из DataManager и отображает их в таблице."""
        self.product_table.setRowCount(0)
        for product in self.data_manager.products_list:
            self.add_product_to_table(product)

    def add_product_to_table(self, product):
        """Добавляет товар в таблицу."""
        row = self.product_table.rowCount()
        self.product_table.insertRow(row)
        self.product_table.setItem(row, 0, QTableWidgetItem(product["product_code"]))
        self.product_table.setItem(row, 1, QTableWidgetItem(product["product_name"]))
        self.product_table.setItem(row, 2, QTableWidgetItem(product["warehouse_number"]))
        self.product_table.setItem(row, 3, QTableWidgetItem(product["supplier"]))
        self.product_table.setItem(row, 4, QTableWidgetItem(str(product["quantity"])))
        self.product_table.setItem(row, 5, QTableWidgetItem(str(product["price"])))
        self.product_table.setItem(row, 6, QTableWidgetItem(str(product["purchase_price"])))

    def add_product(self):
        """Открывает диалог для добавления нового товара."""
        dialog = ProductDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.validate_data(data):
                # Проверка уникальности кода товара
                if any(p["product_code"] == data["product_code"] for p in self.data_manager.products_list):
                    QMessageBox.warning(self, "Ошибка", "Товар с таким кодом уже существует.")
                    return
                self.data_manager.add_product(data)
                self.add_product_to_table(data)
                QMessageBox.information(self, "Успех", "Товар успешно добавлен.")
            else:
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")

    def edit_product(self):
        """Открывает диалог для редактирования выбранного товара."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            product = self.data_manager.products_list[selected_row]
            dialog = ProductDialog(data=product)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()
                if self.validate_data(new_data):
                    # Проверка уникальности кода товара, если он изменился
                    if new_data["product_code"] != product["product_code"]:
                        if any(p["product_code"] == new_data["product_code"] for p in self.data_manager.products_list):
                            QMessageBox.warning(self, "Ошибка", "Товар с таким кодом уже существует.")
                            return
                    self.data_manager.update_product(selected_row, new_data)
                    # Обновляем таблицу
                    for i, key in enumerate(["product_code", "product_name", "warehouse_number", "supplier", "quantity", "price", "purchase_price"]):
                        self.product_table.setItem(selected_row, i, QTableWidgetItem(str(new_data[key])))
                    QMessageBox.information(self, "Успех", "Товар успешно обновлён.")
                else:
                    QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите товар для редактирования.")

    def delete_product(self):
        """Удаляет выбранный товар."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            confirmation = QMessageBox.question(
                self,
                "Удаление товара",
                "Вы уверены, что хотите удалить этот товар?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data_manager.delete_product(selected_row)
                self.product_table.removeRow(selected_row)
                QMessageBox.information(self, "Успех", "Товар успешно удалён.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите товар для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        required_fields = [
            data["product_code"],
            data["product_name"],
            data["warehouse_number"],
            data["supplier"],
            data["quantity"],
            data["price"],
            data["purchase_price"]
        ]
        if not all(field for field in required_fields):
            return False
        try:
            quantity = int(data["quantity"])
            price = float(data["price"])
            purchase_price = float(data["purchase_price"])
            if quantity < 0 or price < 0 or purchase_price < 0:
                return False
        except ValueError:
            return False
        return True
