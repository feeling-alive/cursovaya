# data_manager.py
from PyQt6.QtCore import QObject, pyqtSignal

class DataManager(QObject):
    # Сигналы для уведомления об изменениях
    shipments_changed = pyqtSignal()
    warehouses_changed = pyqtSignal()
    products_changed = pyqtSignal()
    contragents_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Инициализация данных
        self.clients = {
            "Компания А": "Москва",
            "Компания Б": "Санкт-Петербург",
            "Компания В": "Новосибирск"
        }
        self.products_list = [
            {
                "product_code": "P001",
                "product_name": "Товар 1",
                "warehouse_number": "WH001",
                "supplier": "Поставщик A",
                "quantity": 100,
                "price": 100.0,
                "purchase_price": 80.0
            },
            {
                "product_code": "P002",
                "product_name": "Товар 2",
                "warehouse_number": "WH002",
                "supplier": "Поставщик B",
                "quantity": 200,
                "price": 200.0,
                "purchase_price": 150.0
            }
        ]
        self.warehouses = [
            {
                "warehouse_number": "WH001",
                "address": "ул. Ленина, д. 1, Москва",
                "type": "Основной",
                "max_capacity": 1000,
                "load": 500
            },
            {
                "warehouse_number": "WH002",
                "address": "пр. Мира, д. 2, Санкт-Петербург",
                "type": "Вторичный",
                "max_capacity": 800,
                "load": 300
            }
        ]
        self.shipments = [
            {
                "order_number": "ORD001",
                "order_date": "2024-12-20",
                "client": "Компания А",
                "delivery_address": "Москва, ул. Ленина, д.1",
                "product": "Товар 1",
                "warehouse": "WH001",
                "quantity": "10",
                "delivery_method": "Автомобильная",
                "total_amount": "1000.00",
                "status": "Ждёт подтверждения",
                "time": ""
            }
        ]
        self.contragents = [
            {
                "name": "Контрагент А",
                "product": "Товар X",
                "specification": "Спецификация 1",
                "address": "Москва, ул. Ленина, д.1",
                "account_number": "Р/с 1234567890",
                "role": "Поставщик"
            },
            {
                "name": "Контрагент Б",
                "product": "Товар Y",
                "specification": "Спецификация 2",
                "address": "Санкт-Петербург, пр. Мира, д.2",
                "account_number": "Р/с 0987654321",
                "role": "Покупатель"
            }
        ]

    # Методы для управления заказами
    def add_shipment(self, shipment):
        self.shipments.append(shipment)
        self.shipments_changed.emit()

    def update_shipment(self, index, shipment):
        if 0 <= index < len(self.shipments):
            self.shipments[index] = shipment
            self.shipments_changed.emit()

    def delete_shipment(self, index):
        if 0 <= index < len(self.shipments):
            del self.shipments[index]
            self.shipments_changed.emit()

    # Методы для управления складами
    def add_warehouse(self, warehouse):
        self.warehouses.append(warehouse)
        self.warehouses_changed.emit()

    def update_warehouse(self, index, warehouse):
        if 0 <= index < len(self.warehouses):
            self.warehouses[index] = warehouse
            self.warehouses_changed.emit()

    def delete_warehouse(self, index):
        if 0 <= index < len(self.warehouses):
            del self.warehouses[index]
            self.warehouses_changed.emit()

    # Методы для управления контрагентами
    def add_contragent(self, contragent):
        self.contragents.append(contragent)
        self.contragents_changed.emit()

    def update_contragent(self, index, contragent):
        if 0 <= index < len(self.contragents):
            self.contragents[index] = contragent
            self.contragents_changed.emit()

    def delete_contragent(self, index):
        if 0 <= index < len(self.contragents):
            del self.contragents[index]
            self.contragents_changed.emit()

    # Методы для управления продуктами
    def add_product(self, product):
        self.products_list.append(product)
        self.products_changed.emit()

    def update_product(self, index, product):
        if 0 <= index < len(self.products_list):
            self.products_list[index] = product
            self.products_changed.emit()

    def delete_product(self, index):
        if 0 <= index < len(self.products_list):
            del self.products_list[index]
            self.products_changed.emit()
