import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QLabel, QLineEdit, QComboBox,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from login_window import LoginDialog  # Импортируем LoginDialog из login_window.py
from contragents_tab import ContragentTab
from shipment_tab import ShipmentTab # Импортируем ShipmentTab из shipment_tab.py
from analytics_tab import AnalyticsTab  # Импортируем AnalyticsTab из analytics_tab.py
from warehouse_tab import WarehouseTab  # Импортируем WarehouseTab из warehouse_tab.py
from products_tab import ProductTab  # Импортируем ProductTab из product_tab.py
from data_manager import DataManager  # Импортируем DataManager из data_manager.py
from db import SessionLocal
from ReportWindow import ReportWindow

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информационная система для торговой компании")
        self.resize(1280, 920)  # Устанавливаем начальный размер окна
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F8F8;
            }
            QPushButton {
                background-color: #55B2FF;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #7792A8;
            }
            QLabel {
                font-size: 18px;
            }
        """)

        # Инициализация DataManager
        session = SessionLocal()
        self.data_manager = DataManager(session=session)


        main_layout = QVBoxLayout()

        # Верхние кнопки
        button_layout = QHBoxLayout()
        self.report_button = QPushButton("Отчёт")  # Предполагается, что у вас есть модуль отчётов
        self.product_button = QPushButton("Товары")
        self.contragent_button = QPushButton("Контрагенты")
        self.shipment_button = QPushButton("Отправка")
        self.analytics_button = QPushButton("Аналитика")
        self.warehouse_button = QPushButton("Склады")

        self.report_button.setFixedSize(170, 40)
        self.product_button.setFixedSize(170, 40)
        self.contragent_button.setFixedSize(170, 40)
        self.shipment_button.setFixedSize(170, 40)
        self.analytics_button.setFixedSize(170, 40)
        self.warehouse_button.setFixedSize(170, 40)

        button_layout.addWidget(self.report_button)
        button_layout.addWidget(self.product_button)
        button_layout.addWidget(self.contragent_button)
        button_layout.addWidget(self.shipment_button)
        button_layout.addWidget(self.analytics_button)
        button_layout.addWidget(self.warehouse_button)
        button_layout.addStretch()

        # Страницы для QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.report_tab = ReportWindow(data_manager=self.data_manager)  # Создаём вкладку отчёта
        self.product_tab = ProductTab(data_manager=self.data_manager)
        self.contragent_tab = ContragentTab(data_manager=self.data_manager)
        self.shipment_tab = ShipmentTab(data_manager=self.data_manager)
        self.analytics_tab = AnalyticsTab(data_manager=self.data_manager)
        self.warehouse_tab = WarehouseTab(data_manager=self.data_manager)

        # Добавляем вкладки в QStackedWidget
        self.stacked_widget.addWidget(self.report_tab)
        self.stacked_widget.addWidget(self.product_tab)
        self.stacked_widget.addWidget(self.contragent_tab)
        self.stacked_widget.addWidget(self.shipment_tab)
        self.stacked_widget.addWidget(self.analytics_tab)
        self.stacked_widget.addWidget(self.warehouse_tab)

        # Подключение кнопок к соответствующим вкладкам
        self.report_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.report_tab))
        self.product_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.product_tab))
        self.contragent_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.contragent_tab))
        self.shipment_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.shipment_tab))
        self.analytics_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.analytics_tab))
        self.warehouse_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.warehouse_tab))


        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)

    # Создаем и показываем диалог входа
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted:
        # Если вход успешен, показываем основное окно
        window = MyWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # Если вход отменен или не успешен, выходим из приложения
        sys.exit()

if __name__ == "__main__":
    main()
