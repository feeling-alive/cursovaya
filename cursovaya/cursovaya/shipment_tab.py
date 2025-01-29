from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QDialog, QFormLayout, QSizePolicy, QLineEdit, QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate, QTimer
from data_manager import DataManager
from shipment_dialog import ShipmentDialog  # Убедитесь, что этот модуль существует и корректен

class ShipmentTab(QWidget):
    """Вкладка для управления отправкой заказов."""

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        header_label = QLabel("<b>Управление отправкой заказов</b>")
        layout.addWidget(header_label)

        # Форма для создания заказа
        form_layout = QHBoxLayout()

        # Левая часть формы
        left_form = QVBoxLayout()

        # Номер заказа
        self.order_number_input = QLineEdit()
        self.order_number_input.setPlaceholderText("Номер заказа")
        left_form.addWidget(QLabel("Номер заказа:"))
        left_form.addWidget(self.order_number_input)

        # Дата заказа
        self.order_date_input = QDateEdit()
        self.order_date_input.setDate(QDate.currentDate())
        self.order_date_input.setCalendarPopup(True)
        left_form.addWidget(QLabel("Дата заказа:"))
        left_form.addWidget(self.order_date_input)

        # Имя клиента
        self.client_input = QComboBox()
        self.load_clients()  # Загрузка клиентов
        self.client_input.currentTextChanged.connect(self.update_delivery_address)
        left_form.addWidget(QLabel("Имя клиента:"))
        left_form.addWidget(self.client_input)

        # Адрес доставки (автоматически заполняется)
        self.delivery_address_input = QLineEdit()
        self.delivery_address_input.setPlaceholderText("Адрес доставки")
        self.delivery_address_input.setReadOnly(True)
        left_form.addWidget(QLabel("Адрес доставки:"))
        left_form.addWidget(self.delivery_address_input)

        # Способ доставки
        self.delivery_method_input = QComboBox()
        self.delivery_method_input.addItems(["Автомобильная", "Железнодорожная", "Авиадоставка"])
        self.delivery_method_input.currentIndexChanged.connect(self.calculate_delivery_time)
        left_form.addWidget(QLabel("Способ доставки:"))
        left_form.addWidget(self.delivery_method_input)

        form_layout.addLayout(left_form)

        # Правая часть формы
        right_form = QVBoxLayout()

        # Товар
        self.product_input = QComboBox()
        self.product_input.addItems([product.product_name for product in self.data_manager.get_products()])
        self.product_input.currentIndexChanged.connect(self.update_total_amount_and_time)
        right_form.addWidget(QLabel("Товар:"))
        right_form.addWidget(self.product_input)

        # Склад
        self.warehouse_input = QComboBox()
        self.warehouse_input.addItems([warehouse.id for warehouse in self.data_manager.get_warehouses()])
        self.warehouse_input.currentIndexChanged.connect(self.calculate_delivery_time)
        right_form.addWidget(QLabel("Склад:"))
        right_form.addWidget(self.warehouse_input)

        # Количество
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Количество")
        self.quantity_input.textChanged.connect(self.update_total_amount_and_time)
        right_form.addWidget(QLabel("Количество:"))
        right_form.addWidget(self.quantity_input)

        # Общая сумма
        self.total_amount_input = QLineEdit()
        self.total_amount_input.setPlaceholderText("0.00")
        self.total_amount_input.setReadOnly(True)
        right_form.addWidget(QLabel("Общая сумма:"))
        right_form.addWidget(self.total_amount_input)

        # Время доставки
        self.delivery_time_label = QLabel("Время доставки: Не рассчитано")
        right_form.addWidget(QLabel("Время доставки:"))
        right_form.addWidget(self.delivery_time_label)

        # Кнопки
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.create_shipment)
        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.update_shipment)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.clear_button)

        right_form.addLayout(button_layout)

        form_layout.addLayout(right_form)

        layout.addLayout(form_layout)

        # Таблица заказов
        self.shipment_table = QTableWidget()
        self.shipment_table.setColumnCount(10)
        self.shipment_table.setHorizontalHeaderLabels([
            "Номер заказа", "Дата заказа", "Имя клиента", "Адрес доставки",
            "Товар", "Склад", "Количество", "Способ доставки",
            "Общая сумма", "Статус"
        ])
        self.shipment_table.horizontalHeader().setStretchLastSection(True)
        self.shipment_table.horizontalHeader().setDefaultSectionSize(120)
        self.shipment_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.shipment_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.shipment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.shipment_table.cellClicked.connect(self.load_shipment_into_form)
        layout.addWidget(QLabel("<b>Управление заказами</b>"))
        layout.addWidget(self.shipment_table)

        # Кнопки управления
        manage_button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_shipment)
        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.clicked.connect(self.confirm_shipment)
        manage_button_layout.addStretch()
        manage_button_layout.addWidget(self.delete_button)
        manage_button_layout.addWidget(self.confirm_button)
        manage_button_layout.addStretch()
        layout.addLayout(manage_button_layout)

        # Подключение сигналов изменения данных для обновления комбобоксов
        self.data_manager.warehouses_changed.connect(self.update_warehouses)
        self.data_manager.products_changed.connect(self.update_products)
        self.data_manager.contragents_changed.connect(self.update_clients)

        self.load_data()

    def update_products(self):
        """Обновляет список продуктов в выпадающем списке product_input."""
        current_selection = self.product_input.currentText()
        self.product_input.clear()
        self.product_input.addItems([product.product_name for product in self.data_manager.get_products()])
        index = self.product_input.findText(current_selection)
        if index != -1:
            self.product_input.setCurrentIndex(index)

    def update_warehouses(self):
        """Обновляет список складов в выпадающем списке warehouse_input."""
        current_selection = self.warehouse_input.currentText()
        self.warehouse_input.clear()
        self.warehouse_input.addItems([warehouse.id for warehouse in self.data_manager.get_warehouses()])
        index = self.warehouse_input.findText(current_selection)
        if index != -1:
            self.warehouse_input.setCurrentIndex(index)

    def load_clients(self):
        """Загружает клиентов из базы данных."""
        clients = [contragent for contragent in self.data_manager.get_contragents() if contragent.role == "Клиент"]
        self.client_input.addItems([client.id for client in clients])

    def update_clients(self):
        """Обновляет список клиентов в комбобоксе."""
        current_selection = self.client_input.currentText()
        self.client_input.clear()
        self.load_clients()
        index = self.client_input.findText(current_selection)
        if index != -1:
            self.client_input.setCurrentIndex(index)
        self.update_delivery_address(current_selection)

    def update_delivery_address(self, client_name):
        """Автоматически заполняет адрес доставки на основе выбранного клиента."""
        clients = {client.id: client.address for client in self.data_manager.get_contragents() if client.role == "Клиент"}
        self.delivery_address_input.setText(clients.get(client_name, ""))
        self.calculate_delivery_time()

    def calculate_delivery_time(self):
        """Рассчитывает время доставки и ограничивает способы доставки, если склад и клиент в одном городе."""
        client_city = self.delivery_address_input.text().strip()
        warehouse_number = self.warehouse_input.currentText()
        warehouse_info = self.get_warehouse_info(warehouse_number)

        if not warehouse_info:
            self.delivery_time_label.setText("Время доставки: Неизвестно")
            return

        # В SQLAlchemy доступ к атрибутам через точку, а не через ["ключ"]
        warehouse_city = warehouse_info.address.split(",")[-1].strip()

        delivery_method = self.delivery_method_input.currentText()
        same_city = client_city.lower() == warehouse_city.lower()

        # Ограничение способов доставки
        if same_city:
            # Только автомобильная доставка доступна
            index_auto = self.delivery_method_input.findText("Автомобильная")
            index_jd = self.delivery_method_input.findText("Железнодорожная")
            index_ad = self.delivery_method_input.findText("Авиадоставка")

            # Отключаем железнодорожную и авиадоставку
            if index_jd != -1:
                self.delivery_method_input.model().item(index_jd).setEnabled(False)
                if delivery_method == "Железнодорожная":
                    self.delivery_method_input.setCurrentIndex(index_auto)
            if index_ad != -1:
                self.delivery_method_input.model().item(index_ad).setEnabled(False)
                if delivery_method == "Авиадоставка":
                    self.delivery_method_input.setCurrentIndex(index_auto)
        else:
            # В разных городах все способы доставки доступны
            for i in range(self.delivery_method_input.count()):
                self.delivery_method_input.model().item(i).setEnabled(True)

        # Расчет времени доставки
        if delivery_method == "Автомобильная":
            time = "1-3 часа"
        elif delivery_method == "Железнодорожная":
            time = "12-24 часа"
        elif delivery_method == "Авиадоставка":
            time = "4-8 часов"
        else:
            time = "Неизвестно"

        if not client_city:
            time = "Неизвестно"

        self.delivery_time_label.setText(f"{time}")

    def get_warehouse_info(self, warehouse_number):
        """Возвращает информацию о складе по его номеру."""
        for wh in self.data_manager.get_warehouses():  # Используем get_warehouses() вместо несуществующего атрибута
            if wh.id == warehouse_number:  # В SQLAlchemy ID — это атрибут объекта
                return wh
        return None

    def update_total_amount_and_time(self):
        """Обновляет общую сумму заказа на основе выбранного товара и количества, а также пересчитывает время доставки."""
        self.update_total_amount()
        self.calculate_delivery_time()

    def update_total_amount(self):
        """Обновляет общую сумму заказа на основе выбранного товара и количества."""
        product = self.product_input.currentText()
        quantity_text = self.quantity_input.text()

        try:
            quantity = int(quantity_text)
        except ValueError:
            quantity = 0

        # Получаем список продуктов из базы данных
        price = 0
        for p in self.data_manager.get_products():  # Заменяем products_list на get_products()
            if p.product_name == product:  # Доступ к атрибутам SQLAlchemy через точку
                price = p.price
                break

        total = price * quantity
        self.total_amount_input.setText(f"{total:.2f}")

    def create_shipment(self):
        """Создает новый заказ."""
        data = self.get_data_from_form()
        if self.validate_data(data):
            # Добавляем статус
            data["status"] = "Ждёт подтверждения"
            # Добавляем в DataManager
            self.data_manager.add_shipment(data)
            # Добавляем в таблицу
            self.add_shipment_to_table(data)
            # Очистка формы
            self.clear_form()
            QMessageBox.information(self, "Успех", "Заказ успешно создан.")
        else:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")

    def update_shipment(self):
        """Обновляет выбранный заказ."""
        selected_row = self.shipment_table.currentRow()
        if selected_row >= 0:
            data = self.get_data_from_form()
            if self.validate_data(data):
                # Обновляем статус, если он не подтвержден или уже в процессе
                existing_shipment = self.data_manager.shipments[selected_row]
                data["status"] = existing_shipment.get("status", "Ждёт подтверждения")
                # Обновляем в DataManager
                self.data_manager.update_shipment(selected_row, data)
                # Обновляем таблицу
                for i, key in enumerate(["order_number", "order_date", "client", "delivery_address",
                                         "product", "warehouse", "quantity", "delivery_method",
                                         "total_amount", "status"]):
                    self.shipment_table.setItem(selected_row, i, QTableWidgetItem(str(data[key])))
                QMessageBox.information(self, "Успех", "Заказ успешно обновлён.")
            else:
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для обновления.")

    def delete_shipment(self):
        """Удаляет выбранный заказ."""
        selected_row = self.shipment_table.currentRow()
        if selected_row >= 0:
            confirmation = QMessageBox.question(
                self,
                "Удаление заказа",
                "Вы уверены, что хотите удалить этот заказ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                # Удаляем из DataManager
                self.data_manager.delete_shipment(selected_row)
                # Удаляем из таблицы
                self.shipment_table.removeRow(selected_row)
                # Очистка формы
                self.clear_form()
                QMessageBox.information(self, "Успех", "Заказ успешно удалён.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для удаления.")

    def confirm_shipment(self):
        """Подтверждает выбранный заказ и отправляет его во вкладку аналитики."""
        selected_row = self.shipment_table.currentRow()
        if selected_row >= 0:
            shipment = self.data_manager.shipments[selected_row]
            if shipment["status"] != "Ждёт подтверждения":
                QMessageBox.warning(self, "Статус заказа", "Этот заказ уже подтвержден или находится в процессе.")
                return

            confirmation = QMessageBox.question(
                self,
                "Подтверждение заказа",
                "Вы уверены, что хотите подтвердить этот заказ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                # Обновляем статус заказа
                self.data_manager.shipments[selected_row]["status"] = "Ожидает доп подтверждения"
                self.shipment_table.setItem(selected_row, 9, QTableWidgetItem("Ожидает доп подтверждения"))
                QMessageBox.information(self, "Успех", "Заказ подтверждён и отправлен во вкладку 'Аналитика'.")
                # Эмитируем сигнал для обновления аналитики
                self.data_manager.shipments_changed.emit()
                # Удаляем заказ из таблицы "Отправка"
                self.shipment_table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для подтверждения.")

    def load_shipment_into_form(self, row, column):
        """Загружает данные выбранного заказа в форму для редактирования."""
        shipment = self.data_manager.shipments[row]
        self.order_number_input.setText(shipment["order_number"])
        self.order_date_input.setDate(QDate.fromString(shipment["order_date"], "yyyy-MM-dd"))
        client_index = self.client_input.findText(shipment["client"])
        if client_index != -1:
            self.client_input.setCurrentIndex(client_index)
        self.delivery_address_input.setText(shipment["delivery_address"])
        product_index = self.product_input.findText(shipment["product"])
        if product_index != -1:
            self.product_input.setCurrentIndex(product_index)
        warehouse_index = self.warehouse_input.findText(shipment["warehouse"])
        if warehouse_index != -1:
            self.warehouse_input.setCurrentIndex(warehouse_index)
        self.quantity_input.setText(shipment["quantity"])
        delivery_method_index = self.delivery_method_input.findText(shipment["delivery_method"])
        if delivery_method_index != -1:
            self.delivery_method_input.setCurrentIndex(delivery_method_index)
        self.update_total_amount_and_time()

    def get_data_from_form(self):
        """Собирает данные из формы ввода."""
        return {
            "order_number": self.order_number_input.text().strip(),
            "order_date": self.order_date_input.date().toString("yyyy-MM-dd"),
            "client": self.client_input.currentText(),
            "delivery_address": self.delivery_address_input.text().strip(),
            "product": self.product_input.currentText(),
            "warehouse": self.warehouse_input.currentText(),
            "quantity": self.quantity_input.text().strip(),
            "delivery_method": self.delivery_method_input.currentText(),
            "total_amount": self.total_amount_input.text().strip(),
            "status": "Ждёт подтверждения"
        }

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        try:
            quantity = int(data["quantity"])
            if quantity <= 0:
                return False
        except ValueError:
            return False

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
        return all(field for field in required_fields)

    def clear_form(self):
        """Очищает форму ввода."""
        self.order_number_input.clear()
        self.order_date_input.setDate(QDate.currentDate())
        self.client_input.setCurrentIndex(0)
        self.delivery_address_input.clear()
        self.product_input.setCurrentIndex(0)
        self.warehouse_input.setCurrentIndex(0)
        self.quantity_input.clear()
        self.delivery_method_input.setCurrentIndex(0)
        self.total_amount_input.clear()
        self.delivery_time_label.setText("Время доставки: Не рассчитано")

    def add_shipment_to_table(self, shipment):
        """Добавляет заказ в таблицу."""
        row = self.shipment_table.rowCount()
        self.shipment_table.insertRow(row)
        self.shipment_table.setItem(row, 0, QTableWidgetItem(shipment["order_number"]))
        self.shipment_table.setItem(row, 1, QTableWidgetItem(shipment["order_date"]))
        self.shipment_table.setItem(row, 2, QTableWidgetItem(shipment["client"]))
        self.shipment_table.setItem(row, 3, QTableWidgetItem(shipment["delivery_address"]))
        self.shipment_table.setItem(row, 4, QTableWidgetItem(shipment["product"]))
        self.shipment_table.setItem(row, 5, QTableWidgetItem(shipment["warehouse"]))
        self.shipment_table.setItem(row, 6, QTableWidgetItem(shipment["quantity"]))
        self.shipment_table.setItem(row, 7, QTableWidgetItem(shipment["delivery_method"]))
        self.shipment_table.setItem(row, 8, QTableWidgetItem(shipment["total_amount"]))
        self.shipment_table.setItem(row, 9, QTableWidgetItem(shipment["status"]))

    def load_data(self):
        """Загружает данные заказов в таблицу."""
        self.shipment_table.setRowCount(0)
        shipments = self.data_manager.get_shipments()  # Используем метод вместо атрибута
        for shipment in shipments:
            self.add_shipment_to_table(shipment)

    def update_shipment_in_table(self, row):
        """Обновляет статус и время заказа в таблице аналитики."""
        shipment = self.data_manager.shipments[row]
        self.shipment_table.setItem(row, 9, QTableWidgetItem(shipment["status"]))
        # Предполагается, что в таблице "Отправка" нет столбца "Время"
        # Если есть, добавьте соответствующее обновление

    def start_timer(self, row, current_status, next_status, minutes=5):
        """Запускает таймер для обновления статуса заказа."""
        timer = QTimer(self)
        timer.setInterval(minutes * 60 * 1000)  # минуты в миллисекунды
        timer.timeout.connect(lambda: self.update_status(row, next_status))
        timer.start()
        # Можно хранить таймеры, если необходимо управлять ими позже
        # Например: self.timers[row] = timer
        self.delivery_time_label.setText(f"{minutes} мин до '{next_status}'")

    def update_status(self, row, new_status):
        """Обновляет статус заказа и запускает следующий таймер, если необходимо."""
        self.data_manager.shipments[row]["status"] = new_status

        if new_status == "В пути":
            self.data_manager.shipments[row]["time"] = "В пути: Отсчет времени"
            self.update_shipment_in_table(row)
            QMessageBox.information(self, "Статус заказа", "Заказ находится в пути.")

            # Запуск таймера для изменения статуса на "Завершён"
            self.start_timer(row, "В пути", "Завершён", minutes=10)  # 10 минут
        elif new_status == "Завершён":
            self.data_manager.shipments[row]["time"] = "Завершён"
            self.update_shipment_in_table(row)
            QMessageBox.information(self, "Статус заказа", "Заказ завершён.")

        # Останавливаем и удаляем текущий таймер, если они хранятся
        # if row in self.timers:
        #     self.timers[row].stop()
        #     del self.timers[row]
