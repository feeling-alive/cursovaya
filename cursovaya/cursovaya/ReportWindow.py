from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QDateEdit, QComboBox, QFormLayout, QLineEdit, QGroupBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import QDate
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt6.QtCore import QDate

class ReportWindow(QWidget):
    """Окно для формирования отчётов."""

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setWindowTitle("Формирование отчёта")
        self.resize(800, 600)

        layout = QHBoxLayout()

        # Левая часть: предпросмотр отчёта
        left_panel = QVBoxLayout()

        # Заголовок предпросмотра отчёта
        preview_label = QLabel("<b>Предпросмотр отчёта</b>")
        left_panel.addWidget(preview_label)

        # Таблица для предпросмотра отчёта
        self.report_preview_table = QTableWidget()
        self.report_preview_table.setColumnCount(5)  # Столбцы для отчётов
        self.report_preview_table.setHorizontalHeaderLabels(["Номер заказа", "Дата", "Сумма", "Прибыль", "Статус"])
        self.report_preview_table.horizontalHeader().setStretchLastSection(True)
        self.report_preview_table.horizontalHeader().setDefaultSectionSize(120)
        left_panel.addWidget(self.report_preview_table)

        layout.addLayout(left_panel, 3)  # Добавляем левую панель с предпросмотром

        # Правая часть: настройки отчёта
        right_panel = QVBoxLayout()

        # Фильтры для отчёта
        filters_group = QGroupBox("Настройки отчёта")
        filters_layout = QFormLayout()

        # Дата начала
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate().addMonths(-1))  # Предустановленный месяц назад
        self.start_date_input.setCalendarPopup(True)
        filters_layout.addRow("Дата начала:", self.start_date_input)

        # Дата окончания
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())  # Сегодня
        self.end_date_input.setCalendarPopup(True)
        filters_layout.addRow("Дата окончания:", self.end_date_input)

        # Убираем выпадающий список и добавляем текст
        self.report_type_combo = QLabel("Завершённые заказы и прибыль")
        filters_layout.addRow("Тип отчёта:", self.report_type_combo)

        filters_group.setLayout(filters_layout)
        right_panel.addWidget(filters_group)

        # Кнопка для формирования отчёта
        self.generate_button = QPushButton("Сформировать отчёт")
        self.generate_button.clicked.connect(self.generate_report)
        right_panel.addWidget(self.generate_button)

        # Кнопка для скачивания отчёта в PDF
        self.download_button = QPushButton("Скачать в PDF")
        self.download_button.clicked.connect(self.download_report)
        right_panel.addWidget(self.download_button)

        layout.addLayout(right_panel, 1)  # Добавляем правую панель с настройками

        self.setLayout(layout)

    def generate_report(self):
        """Метод для формирования отчёта (теперь только завершённые заказы и прибыль)."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        # В этом случае отчёт только по завершённым заказам с расчётом прибыли
        self.generate_completed_orders_report(start_date, end_date)

    def generate_completed_orders_report(self, start_date, end_date):
        """Генерирует отчёт по завершённым заказам за период и выводит прибыль как текст."""
        # Получаем завершённые заказы из базы данных (из shipment_analytics)
        analytics = self.data_manager.get_analytics()  # Получаем данные из аналитики
        completed_orders = [
            shipment for shipment in analytics
            if shipment.status == "Завершён" and start_date <= str(shipment.order_date) <= end_date
        ]

        self.report_preview_table.setRowCount(len(completed_orders))  # Обновляем количество строк

        # Заполняем таблицу данными
        total_profit = 0  # Инициализируем общую прибыль

        for i, shipment in enumerate(completed_orders):
            # Получаем товар по ID
            product = self.data_manager.get_product_by_id(shipment.product_id)

            # Рассчитываем прибыль, если товар найден
            if product:
                profit = shipment.total_cost - (product.purchase_price * shipment.amount)
                total_profit += profit
            else:
                profit = 0  # Если товар не найден, прибыль равна 0

            # Заполняем таблицу
            self.report_preview_table.setItem(i, 0, QTableWidgetItem(str(shipment.order_number)))
            self.report_preview_table.setItem(i, 1, QTableWidgetItem(str(shipment.order_date)))
            self.report_preview_table.setItem(i, 2, QTableWidgetItem(str(shipment.total_cost)))
            self.report_preview_table.setItem(i, 3, QTableWidgetItem(f"{profit:.2f}"))  # Выводим прибыль
            self.report_preview_table.setItem(i, 4, QTableWidgetItem(shipment.status))

        # Показываем общую прибыль в статусе
        QMessageBox.information(self, "Прибыль", f"Общая прибыль за период: {total_profit:.2f}")

    def download_report(self):
        """Скачивает отчёт в PDF."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        # Мы генерируем отчет типа "completed_orders"
        report_type = "completed_orders"

        # Генерация отчёта в PDF для завершённых заказов
        self.generate_pdf_report(start_date, end_date, report_type)

    def generate_pdf_report(self, start_date, end_date, report_type):
        """Генерирует PDF отчёт по выбранному типу отчёта."""
        file_name = f"report_{report_type}_{start_date}_to_{end_date}.pdf"
        c = canvas.Canvas(file_name, pagesize=A4)

        # Загружаем шрифт с поддержкой кириллицы
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        c.setFont('FreeSans', 12)

        # Заголовок отчёта
        c.drawString(100, 750, f"Отчёт: Завершённые заказы и прибыль")
        c.drawString(100, 730, f"Период: {start_date} - {end_date}")
        c.drawString(100, 710, f"Дата генерации: {QDate.currentDate().toString('yyyy-MM-dd')}")

        # Формирование таблицы данных
        y_position = 690  # Начальная позиция для таблицы

        # Заголовки таблицы
        c.setFont("FreeSans", 10)
        c.drawString(100, y_position, "Номер заказа")
        c.drawString(200, y_position, "Дата заказа")
        c.drawString(300, y_position, "Сумма")
        c.drawString(400, y_position, "Прибыль")
        c.drawString(500, y_position, "Статус")
        y_position -= 20  # Опускаемся вниз на 20 единиц

        # Восстанавливаем шрифт для данных
        c.setFont("FreeSans", 10)

        # Получаем данные из аналитики
        analytics = self.data_manager.get_analytics()  # Получаем данные из shipment_analytics
        completed_orders = [
            shipment for shipment in analytics
            if shipment.status == "Завершён" and start_date <= str(shipment.order_date) <= end_date
        ]

        total_profit = 0  # Инициализируем общую прибыль

        # Заполняем таблицу данными
        for shipment in completed_orders:
            # Рассчитываем прибыль
            product = self.data_manager.get_product_by_id(shipment.product_id)
            if product:
                profit = shipment.total_cost - (product.purchase_price * shipment.amount)
                total_profit += profit
            else:
                profit = 0

            c.drawString(100, y_position, str(shipment.order_number))
            c.drawString(200, y_position, str(shipment.order_date))
            c.drawString(300, y_position, f"{shipment.total_cost}")
            c.drawString(400, y_position, f"{profit:.2f}")
            c.drawString(500, y_position, shipment.status)
            y_position -= 20

            # Останавливаем вывод, если слишком много строк
            if y_position < 100:
                c.showPage()
                y_position = 750

        # Отображаем общую прибыль внизу
        c.setFont("FreeSans", 10)
        c.drawString(100, y_position - 20, f"Общая прибыль: {total_profit:.2f}")
        c.save()

        QMessageBox.information(self, "Отчёт", f"Отчёт сохранён как {file_name}")
