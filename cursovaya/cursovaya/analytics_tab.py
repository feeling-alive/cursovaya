# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
#     QMessageBox, QDialog, QFormLayout, QSizePolicy
# )
# from PyQt6.QtCore import Qt, QTimer
# from data_manager import DataManager
#
#
# class ConfirmationDialog(QDialog):
#     """Диалог подтверждения заказа."""
#
#     def __init__(self, shipment, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Подтверждение заказа")
#         self.setModal(True)
#         self.shipment = shipment
#
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#
#         form_layout = QFormLayout()
#
#         form_layout.addRow("Номер заказа:", QLabel(self.shipment.order_number))
#         form_layout.addRow("Дата заказа:", QLabel(str(self.shipment.order_date)))
#         form_layout.addRow("Имя клиента:", QLabel(self.shipment.client_id))
#         form_layout.addRow("Адрес доставки:", QLabel(self.shipment.delivery_address))
#         form_layout.addRow("Товар:", QLabel(self.shipment.product_id))
#         form_layout.addRow("Склад:", QLabel(self.shipment.warehouse_id))
#         form_layout.addRow("Количество:", QLabel(str(self.shipment.amount)))
#         form_layout.addRow("Способ доставки:", QLabel(self.shipment.delivery_method))
#         form_layout.addRow("Общая сумма:", QLabel(str(self.shipment.total_cost)))
#
#         layout.addLayout(form_layout)
#
#         # Кнопки подтверждения и отмены
#         button_layout = QHBoxLayout()
#         self.confirm_button = QPushButton("Подтвердить")
#         self.cancel_button = QPushButton("Отмена")
#         self.confirm_button.clicked.connect(self.accept)
#         self.cancel_button.clicked.connect(self.reject)
#         button_layout.addWidget(self.confirm_button)
#         button_layout.addWidget(self.cancel_button)
#         layout.addLayout(button_layout)


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QDialog, QFormLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from data_manager import DataManager  # Убедитесь, что путь к data_manager.py корректен


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
        self.refresh_button = QPushButton("Обновить статусы")
        self.confirm_button = QPushButton("Подтвердить")
        self.cancel_button = QPushButton("Отмена")
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.refresh_button.clicked.connect(self.update_shipment_in_table)  # Обновление статусов
        self.confirm_button.clicked.connect(self.confirm_selected_order)  # Подтверждение заказа
        self.cancel_button.clicked.connect(self.cancel_selected_order)  # Отмена заказа

        # Подключаем сигнал изменения данных аналитики
        self.data_manager.analytics_changed.connect(self.load_data)  # Обновление таблицы аналитики

        self.load_data()  # Первоначальная загрузка данных при старте

    def load_data(self):
        """Загружает все данные из базы данных в таблицу аналитики."""
        self.analytics_table.setRowCount(0)  # Очистить таблицу перед загрузкой данных
        analytics = self.data_manager.get_analytics()  # Загружаем все данные из таблицы shipment_analytics
        print(f"Данные из аналитики: {len(analytics)} записей.")  # Проверка вывода данных
        for shipment in analytics:
            print(f"Заказ: {shipment.order_number}, Статус: {shipment.status}")  # Отладочный вывод
            self.add_shipment_to_table(shipment)

    def add_shipment_to_table(self, shipment):
        """Добавляет заказ из аналитики в таблицу."""
        row = self.analytics_table.rowCount()
        self.analytics_table.insertRow(row)

        # Используем правильные атрибуты для доступа к данным
        self.analytics_table.setItem(row, 0, QTableWidgetItem(shipment.order_number))  # Номер заказа
        self.analytics_table.setItem(row, 1, QTableWidgetItem(str(shipment.order_date)))  # Дата заказа
        self.analytics_table.setItem(row, 2, QTableWidgetItem(shipment.client_id))  # ID клиента
        self.analytics_table.setItem(row, 3, QTableWidgetItem(shipment.delivery_address))  # Адрес доставки
        self.analytics_table.setItem(row, 4, QTableWidgetItem(shipment.product_id))  # ID товара
        self.analytics_table.setItem(row, 5, QTableWidgetItem(shipment.warehouse_id))  # ID склада
        self.analytics_table.setItem(row, 6, QTableWidgetItem(str(shipment.amount)))  # Количество
        self.analytics_table.setItem(row, 7, QTableWidgetItem(shipment.delivery_method))  # Способ доставки
        self.analytics_table.setItem(row, 8, QTableWidgetItem(str(shipment.total_cost)))  # Общая сумма
        self.analytics_table.setItem(row, 9, QTableWidgetItem(shipment.status))  # Статус
        self.analytics_table.setItem(row, 10, QTableWidgetItem(shipment.time_info or ""))  # Время

    def confirm_selected_order(self):
        """Подтверждает выбранный заказ через форму."""
        selected_row = self.analytics_table.currentRow()
        if selected_row >= 0:
            # Получаем номер заказа для поиска в DataManager
            order_number = self.analytics_table.item(selected_row, 0).text()
            analytics = self.data_manager.get_analytics()
            shipment = next((s for s in analytics if s.order_number == order_number), None)
            if shipment:
                if shipment.status == "Завершён":
                    QMessageBox.warning(self, "Ошибка", "Этот заказ уже завершён.")
                    return
                if shipment.status != "Ждёт подтверждения":
                    QMessageBox.warning(self, "Ошибка", "Этот заказ уже подтверждён или не ожидает подтверждения.")
                    return

                # Обновление статуса на "Формируется" и присваиваем время формирования
                shipment.status = "Формируется"
                shipment.time_info = "Формируется: 1 мин"
                self.data_manager.update_analytics()  # Обновляем данные аналитики

                # Обновляем строку в таблице
                self.update_shipment_in_table(selected_row)

                # Запускаем таймер для изменения статуса на "Отправлен" через 1 минуту
                self.start_timer(selected_row, "Формируется", "Отправлен", minutes=1)

                QMessageBox.information(self, "Успех", f"Статус заказа изменён на 'Формируется'.")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти заказ.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для подтверждения.")

    def start_timer(self, row, current_status, next_status, minutes=1):
        """Запускает таймер для обновления статуса заказа."""
        timer = QTimer(self)
        timer.setInterval(minutes * 60 * 1000)  # минуты в миллисекунды
        timer.timeout.connect(lambda: self.update_status(row, current_status, next_status))
        timer.start()
        # Сохраняем таймер в словарь по номеру строки
        self.timers[row] = timer

    def update_status(self, row, current_status, next_status):
        """Обновляет статус заказа на следующий шаг."""
        shipment = self.data_manager.get_analytics()[row]
        if shipment.status == current_status:
            shipment.status = next_status
            if next_status == "Отправлен":
                shipment.time_info = "Отправлен: 1 мин"
                # Запускаем таймер для изменения статуса на "Завершён"
                self.start_timer(row, "Отправлен", "Завершён", minutes=1)
            elif next_status == "Завершён":
                shipment.time_info = "Завершён"
            self.data_manager.update_analytics()  # Обновляем данные аналитики
            self.update_shipment_in_table(row)

    def cancel_selected_order(self):
        """Отменяет выбранный заказ."""
        selected_row = self.analytics_table.currentRow()
        if selected_row >= 0:
            # Получаем номер заказа для поиска в DataManager
            order_number = self.analytics_table.item(selected_row, 0).text()
            shipment = next((s for s in self.data_manager.get_analytics() if s.order_number == order_number), None)
            if shipment:
                if shipment.status == "Ждёт подтверждения":
                    confirmation = QMessageBox.question(
                        self,
                        "Отмена заказа",
                        "Вы уверены, что хотите отменить этот заказ?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if confirmation == QMessageBox.StandardButton.Yes:
                        # Передаем индекс строки, а не сам объект
                        self.data_manager.delete_shipment(selected_row)  # Удаляем заказ
                        self.load_data()  # Обновляем таблицу
                        QMessageBox.information(self, "Успех", "Заказ успешно отменён.")
                else:
                    QMessageBox.warning(self, "Ошибка",
                                        "Невозможно отменить заказ, так как его статус не позволяет это.")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти заказ.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите строку для отмены.")

    def update_shipment_in_table(self, row):
        """Обновляет данные строки в таблице аналитики."""
        shipment = self.data_manager.get_analytics()[row]
        self.analytics_table.setItem(row, 9, QTableWidgetItem(shipment.status))
        self.analytics_table.setItem(row, 10, QTableWidgetItem(shipment.time_info or ""))