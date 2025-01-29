# analytics_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QDialog, QFormLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from data_manager import DataManager  # Убедитесь, что путь к data_manager.py корректен


class ConfirmationDialog(QDialog):
    """Диалог подтверждения заказа."""

    def __init__(self, shipment, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение заказа")
        self.setModal(True)
        self.shipment = shipment

        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QFormLayout()

        form_layout.addRow("Номер заказа:", QLabel(shipment["order_number"]))
        form_layout.addRow("Дата заказа:", QLabel(shipment["order_date"]))
        form_layout.addRow("Имя клиента:", QLabel(shipment["client"]))
        form_layout.addRow("Адрес доставки:", QLabel(shipment["delivery_address"]))
        form_layout.addRow("Товар:", QLabel(shipment["product"]))
        form_layout.addRow("Склад:", QLabel(shipment["warehouse"]))
        form_layout.addRow("Количество:", QLabel(shipment["quantity"]))
        form_layout.addRow("Способ доставки:", QLabel(shipment["delivery_method"]))
        form_layout.addRow("Общая сумма:", QLabel(shipment["total_amount"]))

        layout.addLayout(form_layout)

        # Кнопки подтверждения и отмены
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Подтвердить")
        self.cancel_button = QPushButton("Отмена")
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)


class AnalyticsTab(QWidget):
    """Вкладка для ведения аналитики продаж компании."""

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.timers = {}  # Словарь для хранения таймеров по заказам

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        header_label = QLabel("<b>Аналитика продаж</b>")
        layout.addWidget(header_label)

        # Таблица аналитики
        self.analytics_table = QTableWidget()
        self.analytics_table.setColumnCount(11)  # Включая статус и время
        self.analytics_table.setHorizontalHeaderLabels([
            "Номер заказа", "Дата заказа", "Имя клиента", "Адрес доставки",
            "Товар", "Склад", "Количество", "Способ доставки", "Общая сумма", "Статус", "Время"
        ])
        self.analytics_table.horizontalHeader().setStretchLastSection(True)
        self.analytics_table.horizontalHeader().setDefaultSectionSize(120)
        self.analytics_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.analytics_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.analytics_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.analytics_table)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Обновить")
        self.confirm_button = QPushButton("Подтвердить")
        self.cancel_button = QPushButton("Отмена")
        self.refresh_button.clicked.connect(self.load_data)
        self.confirm_button.clicked.connect(self.confirm_selected_order)
        self.cancel_button.clicked.connect(self.cancel_selected_order)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Подключаем сигнал изменения заказов
        self.data_manager.shipments_changed.connect(self.load_data)

        self.load_data()

    def load_data(self):
        """Загружает данные заказов в таблицу аналитики."""
        self.analytics_table.setRowCount(0)
        shipments = self.data_manager.get_shipments()  # Используем метод
        for shipment in shipments:
            # Добавляем заказы всех интересующих статусов
            if shipment.status in ["Ожидает доп подтверждения", "Формируется", "В пути", "Завершён"]:
                self.add_shipment_to_table(shipment)

        # Проверяем, нужно ли активировать кнопку "Подтвердить"
        selected_row = self.analytics_table.currentRow()
        if selected_row >= 0:
            shipment = shipments[selected_row]
            if shipment.status != "Ожидает доп подтверждения":
                self.confirm_button.setDisabled(True)
            else:
                self.confirm_button.setEnabled(True)

    def add_shipment_to_table(self, shipment):
        """Добавляет заказ в таблицу аналитики."""
        row = self.analytics_table.rowCount()
        self.analytics_table.insertRow(row)
        self.analytics_table.setItem(row, 0, QTableWidgetItem(shipment["order_number"]))
        self.analytics_table.setItem(row, 1, QTableWidgetItem(shipment["order_date"]))
        self.analytics_table.setItem(row, 2, QTableWidgetItem(shipment["client"]))
        self.analytics_table.setItem(row, 3, QTableWidgetItem(shipment["delivery_address"]))
        self.analytics_table.setItem(row, 4, QTableWidgetItem(shipment["product"]))
        self.analytics_table.setItem(row, 5, QTableWidgetItem(shipment["warehouse"]))
        self.analytics_table.setItem(row, 6, QTableWidgetItem(shipment["quantity"]))
        self.analytics_table.setItem(row, 7, QTableWidgetItem(shipment["delivery_method"]))
        self.analytics_table.setItem(row, 8, QTableWidgetItem(shipment["total_amount"]))
        self.analytics_table.setItem(row, 9, QTableWidgetItem(shipment["status"]))
        self.analytics_table.setItem(row, 10, QTableWidgetItem(shipment.get("time", "")))

    def confirm_selected_order(self):
        """Подтверждает выбранный заказ через форму."""
        selected_row = self.analytics_table.currentRow()
        if selected_row >= 0:
            # Получаем номер заказа для поиска в DataManager
            order_number = self.analytics_table.item(selected_row, 0).text()
            shipments = self.data_manager.get_shipments()
            shipment = next((s for s in shipments if s.order_number == order_number), None)
            if shipment:
                if shipment.status == "Завершён":
                    QMessageBox.warning(self, "Ошибка", "Этот заказ уже завершён.")
                    return
                if shipment.status != "Ожидает доп подтверждения":
                    QMessageBox.warning(self, "Ошибка", "Этот заказ уже подтверждён.")
                    return

                dialog = ConfirmationDialog(shipment, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # Определяем новый статус
                    new_status = "Формируется"
                    minutes = 15

                    # Обновляем статус заказа
                    shipment.status = new_status
                    shipment.time_info = f"{new_status}: {minutes} мин"
                    self.data_manager.update_shipment(shipment.id, shipment)

                    # Обновляем таблицу
                    self.update_shipment_in_table(selected_row)

                    QMessageBox.information(self, "Успех", f"Статус заказа изменён на '{new_status}'.")

                    # Если статус не "Завершён", запускаем таймер
                    if new_status != "Завершён":
                        self.start_timer(selected_row, new_status, minutes)

                    # Отключаем кнопку "Подтвердить", если она относится к текущей строке
                    self.confirm_button.setDisabled(True)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти заказ.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для подтверждения.")

    def cancel_selected_order(self):
        """Отменяет выбранный заказ. Отмена возможна только для заказов со статусом "Подтверждён"."""
        selected_row = self.analytics_table.currentRow()
        if selected_row >= 0:
            # Получаем номер заказа для поиска в DataManager
            order_number = self.analytics_table.item(selected_row, 0).text()
            shipment = next((s for s in self.data_manager.shipments if s["order_number"] == order_number), None)
            if shipment and shipment["status"] == "Ожидает доп подтверждения":
                confirmation = QMessageBox.question(
                    self,
                    "Отмена заказа",
                    "Вы уверены, что хотите отменить этот заказ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirmation == QMessageBox.StandardButton.Yes:
                    # Удаляем заказ из DataManager
                    self.data_manager.delete_shipment(self.data_manager.shipments.index(shipment))
                    # Обновляем таблицу
                    self.load_data()
                    QMessageBox.information(self, "Успех", "Заказ успешно отменён.")
            elif shipment and shipment["status"] in ["Формируется", "В пути"]:
                QMessageBox.warning(
                    self,
                    "Невозможно отменить",
                    "Отмена заказа невозможна, так как он уже в процессе формирования или доставки."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Статус заказа",
                    "Этот заказ уже завершён или не существует."
                )
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для отмены.")

    def update_shipment_in_table(self, row):
        """Обновляет статус и время заказа в таблице аналитики."""
        shipment = self.data_manager.shipments[row]
        self.analytics_table.setItem(row, 9, QTableWidgetItem(shipment["status"]))
        self.analytics_table.setItem(row, 10, QTableWidgetItem(shipment.get("time", "")))

    def start_timer(self, row, current_status, minutes):
        """Запускает таймер для обновления статуса заказа."""
        if row in self.timers:
            self.timers[row].stop()
            del self.timers[row]

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.setInterval(minutes * 60 * 1000)  # минуты в миллисекунды
        timer.timeout.connect(lambda: self.update_status(row, current_status))
        timer.start()
        self.timers[row] = timer
        self.analytics_table.setItem(row, 10, QTableWidgetItem(f"{minutes} мин до следующего статуса"))

    def update_status(self, row, current_status):
        """Обновляет статус заказа и запускает следующий таймер, если необходимо."""
        order_number = self.analytics_table.item(row, 0).text()
        shipment = next((s for s in self.data_manager.shipments if s["order_number"] == order_number), None)
        if shipment:
            if shipment["status"] == "Завершён":
                QMessageBox.information(self, "Информация", "Этот заказ уже завершён.")
                return

            if current_status == "Формируется":
                new_status = "В пути"
                minutes = 10
            elif current_status == "В пути":
                new_status = "Завершён"
                minutes = 0
            else:
                return

            shipment["status"] = new_status
            shipment["time"] = f"{new_status}: {minutes} мин" if minutes > 0 else "Завершён"
            self.data_manager.update_shipment(self.data_manager.shipments.index(shipment), shipment)
            self.update_shipment_in_table(row)

            if new_status == "Завершён":
                QMessageBox.information(self, "Информация", "Заказ успешно завершён.")
            else:
                self.start_timer(row, new_status, minutes)
