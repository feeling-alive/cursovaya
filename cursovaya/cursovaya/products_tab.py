from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QFormLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from data_manager import DataManager

class ProductDialog(QDialog):
    """Диалоговое окно для добавления/редактирования товара."""

    def __init__(self, data=None, data_manager=None):
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

        self.data_manager = data_manager  # Получаем data_manager

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Форма ввода данных товара
        form_layout = QVBoxLayout()

        # Код товара
        code_label = QLabel("Код товара:")
        code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(code_label)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Введите код товара")
        self.code_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.code_input)

        form_layout.addSpacing(15)

        # Название товара
        name_label = QLabel("Название товара:")
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        self.name_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.name_input)

        form_layout.addSpacing(15)

        # Номер склада
        warehouse_label = QLabel("Номер склада:")
        warehouse_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(warehouse_label)

        self.warehouse_input = QComboBox()
        self.warehouse_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.warehouse_input)

        form_layout.addSpacing(15)

        # Поставщик
        supplier_label = QLabel("Поставщик:")
        supplier_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(supplier_label)

        self.supplier_input = QComboBox()
        self.supplier_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.supplier_input)

        form_layout.addSpacing(15)

        # Количество
        quantity_label = QLabel("Количество:")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(quantity_label)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Введите количество")
        self.quantity_input.setValidator(QIntValidator())
        self.quantity_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.quantity_input)

        form_layout.addSpacing(15)

        # Цена товара
        price_label = QLabel("Цена товара:")
        price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(price_label)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Введите цену товара")
        self.price_input.setValidator(QIntValidator())
        self.price_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.price_input)

        form_layout.addSpacing(15)

        # Закупочная цена
        purchase_price_label = QLabel("Закупочная цена:")
        purchase_price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(purchase_price_label)

        self.purchase_price_input = QLineEdit()
        self.purchase_price_input.setPlaceholderText("Введите закупочную цену")
        self.purchase_price_input.setValidator(QIntValidator())
        self.purchase_price_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.purchase_price_input)

        main_layout.addLayout(form_layout)
        form_layout.addSpacing(15)

        # Кнопки "Сохранить" и "Отмена"
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        save_button = QPushButton("Сохранить")
        save_button.setFixedWidth(376)
        save_button.setFixedHeight(54)
        save_button.clicked.connect(self.save_product)
        button_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(316)
        cancel_button.setFixedHeight(49)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Загрузка данных из базы
        self.load_warehouses()
        self.load_suppliers()

        if not data:  # Новое добавление
            try:
                next_code = self.data_manager.get_next_product_code()
                self.code_input.setText(next_code)
                self.code_input.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать код товара: {str(e)}")
                self.code_input.setText("ERROR")
                self.code_input.setEnabled(False)

        if data:  # Для редактирования
            self.set_data(data)

    def load_warehouses(self):
        """Загрузка доступных складов"""
        self.warehouse_input.clear()
        try:
            warehouses = self.data_manager.get_warehouses()
            if warehouses:
                self.warehouse_input.addItems([w.id for w in warehouses])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки складов: {str(e)}")

    def load_suppliers(self):
        """Загрузка списка поставщиков"""
        self.supplier_input.clear()
        try:
            suppliers = [s for s in self.data_manager.get_contragents() if s.role.lower() == "поставщик"]
            if suppliers:
                self.supplier_input.addItems([s.id for s in suppliers])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки поставщиков: {str(e)}")

    def save_product(self):
        """Сохраняет или обновляет продукт в базе данных."""
        data = self.get_data()

        if not data["id"]:
            QMessageBox.warning(self, "Ошибка", "Код товара не может быть пустым.")
            return

        try:
            if self.data_manager.get_product_by_id(data["id"]):  # Продукт уже существует
                self.data_manager.update_product(data["id"], data)
                QMessageBox.information(self, "Успех", "Продукт успешно обновлен.")
            else:
                self.data_manager.add_product(data)
                QMessageBox.information(self, "Успех", "Продукт успешно добавлен.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении продукта: {str(e)}")


    def get_data(self):
        """Возвращает данные из формы."""
        return {
            "id": self.code_input.text().strip(),
            "product_name": self.name_input.text().strip(),
            "warehouse_number": self.warehouse_input.currentText(),
            "supplier": self.supplier_input.currentText(),
            "quantity": int(self.quantity_input.text().strip()),
            "price": float(self.price_input.text().strip()),
            "purchase_price": float(self.purchase_price_input.text().strip())
        }

    def load_warehouses(self):
        """Загружает данные складов."""
        self.warehouse_input.clear()
        try:
            warehouses = self.data_manager.get_warehouses()
            if warehouses:
                self.warehouse_input.addItems([warehouse.id for warehouse in warehouses])
            else:
                QMessageBox.warning(self, "Предупреждение", "Нет доступных складов.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки складов: {str(e)}")

    def load_suppliers(self):
        """Загружает поставщиков."""
        self.supplier_input.clear()
        try:
            suppliers = self.data_manager.get_contragents()  # Все контрагенты
            suppliers = [sup for sup in suppliers if sup.role.lower() == "поставщик"]
            if suppliers:
                self.supplier_input.addItems([supplier.id for supplier in suppliers])
            else:
                QMessageBox.warning(self, "Предупреждение", "Нет доступных поставщиков.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки поставщиков: {str(e)}")

    def set_data(self, data):
        """Заполняет поля для редактирования."""
        self.code_input.setText(data["id"])
        self.name_input.setText(data["product_name"])
        self.warehouse_input.setCurrentText(data["warehouse_number"])
        self.supplier_input.setCurrentText(data["supplier"])
        self.quantity_input.setText(str(data["quantity"]))
        self.price_input.setText(str(data["price"]))
        self.purchase_price_input.setText(str(data["purchase_price"]))


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
        self.product_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
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
        self.delete_button.clicked.connect(self.delete_selected_products)

        self.load_data()

    def load_data(self):
        """Загружает данные товаров в таблицу."""
        self.product_table.setRowCount(0)  # Очищаем таблицу перед загрузкой данных
        products = self.data_manager.get_products()
        for product in products:
            row = self.product_table.rowCount()
            self.product_table.insertRow(row)
            self.product_table.setItem(row, 0, QTableWidgetItem(product.id))
            self.product_table.setItem(row, 1, QTableWidgetItem(product.product_name))
            self.product_table.setItem(row, 2, QTableWidgetItem(product.warehouse_number or ""))
            self.product_table.setItem(row, 3, QTableWidgetItem(product.supplier or ""))
            self.product_table.setItem(row, 4, QTableWidgetItem(str(product.quantity)))
            self.product_table.setItem(row, 5, QTableWidgetItem(f"{product.price:.2f}"))
            self.product_table.setItem(row, 6, QTableWidgetItem(f"{product.purchase_price:.2f}"))

    def add_product(self):
        """Добавляет новый товар."""
        dialog = ProductDialog(data_manager=self.data_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            # Проверка корректности введенных данных
            if not self.validate_data(data):
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
                return

            # Проверка вместимости склада
            warehouse_id = data["warehouse_number"]  # ID склада
            quantity = int(data["quantity"])  # Преобразование количества в int

            try:
                warehouse = self.data_manager.get_warehouse_by_id(warehouse_id)
                if warehouse.capacity + quantity > warehouse.max_capacity:
                    QMessageBox.warning(self, "Недостаточно места",
                                        "На складе недостаточно места для добавления товара.")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные о складе: {str(e)}")
                return

            try:
                # Добавление товара в базу данных
                self.data_manager.add_product(data)

                # # Обновляем вместимость склада
                # warehouse.capacity += quantity
                # self.data_manager.update_warehouse(warehouse.id, {"capacity": warehouse.capacity})

                # Обновляем таблицу с товарами
                self.load_data()  # Теперь это обновит таблицу с товарами

                QMessageBox.information(self, "Успех", "Товар успешно добавлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении товара: {str(e)}")

    def edit_product(self):
        """Открывает диалог для редактирования выбранного товара."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            try:
                product_id = self.product_table.item(selected_row, 0).text()
                product = self.data_manager.get_product_by_id(product_id)

                if not product:
                    QMessageBox.warning(self, "Ошибка", "Товар не найден.")
                    return

                # Сбор данных о товаре для редактирования
                product_data = {
                    "id": product.id,  # Используем уже существующий код товара
                    "product_name": product.product_name,
                    "warehouse_number": product.warehouse_number,
                    "supplier": product.supplier,
                    "quantity": product.quantity,
                    "price": product.price,
                    "purchase_price": product.purchase_price,
                }

                # Передаем data_manager в диалог для редактирования товара
                dialog = ProductDialog(data=product_data, data_manager=self.data_manager)  # Передаем data_manager
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_data = dialog.get_data()
                    if self.validate_data(new_data):
                        # Проверяем склад
                        warehouse_id = new_data["warehouse_number"]
                        new_quantity = int(new_data["quantity"])
                        warehouse = self.data_manager.get_warehouse_by_id(warehouse_id)

                        if warehouse.capacity - product.quantity + new_quantity > warehouse.max_capacity:
                            QMessageBox.warning(self, "Недостаточно места",
                                                "На складе недостаточно места для обновления товара.")
                            return

                        # Обновляем товар
                        self.data_manager.update_product(product.id, new_data)

                        # Обновляем таблицу с новыми данными
                        for i, key in enumerate(
                                ["id", "product_name", "warehouse_number", "supplier", "quantity", "price",
                                 "purchase_price"]):
                            self.product_table.setItem(selected_row, i, QTableWidgetItem(str(new_data[key])))

                        QMessageBox.information(self, "Успех", "Товар успешно обновлён.")
                    else:
                        QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании товара: {str(e)}")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите товар для редактирования.")

    def delete_selected_products(self):
        """Удаляет выбранные товары."""
        selected_rows = self.product_table.selectionModel().selectedRows()  # Получаем выбранные строки

        if not selected_rows:
            QMessageBox.warning(self, "Выбор строк", "Пожалуйста, выберите товары для удаления.")
            return

        confirmation = QMessageBox.question(
            self,
            "Удаление товаров",
            "Вы уверены, что хотите удалить выбранные товары?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            product_ids_to_delete = []

            # Сбор всех ID товаров для удаления
            for row in selected_rows:
                product_id = self.product_table.item(row.row(), 0).text()  # Получаем ID товара
                product_ids_to_delete.append(product_id)

            # Удаление товаров из базы данных
            try:
                for product_id in product_ids_to_delete:
                    product = self.data_manager.get_product_by_id(product_id)
                    if product:
                        self.data_manager.delete_product(product.id)  # Удаляем товар из базы данных

                # Удаляем товары из таблицы (удаляем строки в обратном порядке)
                for row in sorted(selected_rows, reverse=True):
                    self.product_table.removeRow(row.row())  # Удаляем строку из таблицы

                QMessageBox.information(self, "Успех", "Выбранные товары успешно удалены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении товаров: {str(e)}")

    def delete_product(self):
        """Удаляет выбранный товар."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            product_id = self.product_table.item(selected_row, 0).text()  # Получаем ID товара
            confirmation = QMessageBox.question(
                self,
                "Удаление товара",
                f"Вы уверены, что хотите удалить товар с кодом {product_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                try:
                    product = self.data_manager.get_product_by_id(product_id)
                    if product:
                        self.data_manager.delete_product(product.id)  # Удаляем товар из базы
                        self.product_table.removeRow(selected_row)  # Удаляем товар из таблицы
                        QMessageBox.information(self, "Успех", "Товар успешно удалён.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении товара: {str(e)}")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите товар для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        required_fields = [
            data["id"],  # Было: 'product_code'
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
            if quantity <= 0 or price <= 0 or purchase_price < 0:
                return False
        except ValueError:
            return False
        return True

