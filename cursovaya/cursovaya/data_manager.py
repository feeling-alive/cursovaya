from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from db import SessionLocal
from PyQt6.QtCore import QObject, pyqtSignal

# Создание базы для моделей
Base = declarative_base()

# Модели таблиц
class Contragent(Base):
    __tablename__ = 'contragents'

    id = Column(String(50), primary_key=True)
    product = Column(String(255))
    specification = Column(String(255))
    address = Column(String(255))
    account_number = Column(String(100))
    role = Column(String(100))

class Product(Base):
    __tablename__ = 'products'

    id = Column(String(50), primary_key=True)
    product_name = Column(String(255), nullable=False)
    warehouse_number = Column(String(50), ForeignKey('warehouses.id'))
    supplier = Column(String(50), ForeignKey('contragents.id'))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.00)
    purchase_price = Column(Float, default=0.00)

class Warehouse(Base):
    __tablename__ = 'warehouses'

    id = Column(String(50), primary_key=True)
    address = Column(String(255), nullable=False)
    type = Column(String(100))
    max_capacity = Column(Integer, default=0)
    capacity = Column(Integer, default=0)

class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(50), unique=True, nullable=False)
    order_date = Column(Date, nullable=False)
    client_id = Column(String(50), ForeignKey('contragents.id'))
    delivery_address = Column(String(255), nullable=False)
    product_id = Column(String(50), ForeignKey('products.id'))
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'))
    amount = Column(Integer, nullable=False)
    delivery_method = Column(String(100))
    total_cost = Column(Float, default=0.00)
    status = Column(String(100), nullable=False)
    time_info = Column(String(255))

class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

# DataManager
class DataManager(QObject):
    warehouses_changed = pyqtSignal()
    products_changed = pyqtSignal()
    contragents_changed = pyqtSignal()
    shipments_changed = pyqtSignal()

    def __init__(self, session):
        super().__init__()
        self.session = session


    # Warehouses
    def get_warehouses(self):
        """Возвращает список всех складов."""
        try:
            return self.session.query(Warehouse).all()
        except Exception as e:
            raise Exception(f"Ошибка при получении складов: {str(e)}")

    def get_warehouse_by_id(self, warehouse_id):
        """Возвращает склад по его ID."""
        try:
            return self.session.query(Warehouse).filter_by(id=warehouse_id).first()
        except Exception as e:
            raise Exception(f"Ошибка при получении склада по ID: {str(e)}")

    def get_next_warehouse_code(self):
        """Возвращает следующий уникальный код склада в формате WH001."""
        try:
            # Получаем последний склад по ID, отсортированный по убыванию
            last_warehouse = self.session.query(Warehouse).order_by(Warehouse.id.desc()).first()

            if last_warehouse:
                # Извлекаем числовую часть после префикса 'WH' и увеличиваем числовую часть
                numeric_part = int(last_warehouse.id[2:])  # Пропускаем 'WH' и увеличиваем числовую часть
                next_code = numeric_part + 1
            else:
                next_code = 1  # Если складов нет, начинаем с "WH001"

            # Формируем следующий ID склада с префиксом 'WH' и числовой частью
            next_id = f"WH{next_code:03d}"

            # Проверяем, существует ли уже такой код склада
            while self.session.query(Warehouse).filter_by(id=next_id).first() is not None:
                next_code += 1
                next_id = f"WH{next_code:03d}"

            return next_id
        except Exception as e:
            raise Exception(f"Ошибка при генерации кода склада: {str(e)}")


        except Exception as e:
            raise Exception(f"Ошибка при генерации кода склада: {str(e)}")

    def get_next_product_code(self):
        """Возвращает следующий уникальный код товара в формате P00001."""
        try:
            last_product = self.session.query(Product).order_by(Product.id.desc()).first()
            if last_product:
                # Проверяем, является ли идентификатор корректным и увеличиваем числовую часть
                numeric_part = int(last_product.id[1:])  # Извлекаем числовую часть
                next_code = numeric_part + 1
            else:
                next_code = 1  # Если товаров нет, начнем с "P00001"

            # Проверяем, существует ли уже такой код
            next_id = f"P{next_code:05d}"
            # Используем цикл, чтобы найти уникальный код
            while self.session.query(Product).filter_by(id=next_id).first() is not None:
                next_code += 1
                next_id = f"P{next_code:05d}"

            return next_id
        except Exception as e:
            raise Exception(f"Ошибка при генерации кода товара: {str(e)}")

            return next_id
        except Exception as e:
            raise Exception(f"Ошибка при генерации кода товара: {str(e)}")

    def get_product_by_id(self, product_id):
        """Возвращает товар по его ID."""
        return self.session.query(Product).filter_by(id=product_id).first()

    def add_warehouse(self, warehouse_data):
        """Добавляет новый склад или обновляет существующий."""
        try:
            # Попытка найти склад с таким же ID
            existing_warehouse = self.session.query(Warehouse).filter_by(id=warehouse_data['id']).first()

            if existing_warehouse:
                # Если склад существует, обновляем его
                for key, value in warehouse_data.items():
                    setattr(existing_warehouse, key, value)  # Обновляем поля склада
                self.session.commit()
                self.warehouses_changed.emit()  # Сигнал об изменениях
                print(f"Склад с ID {warehouse_data['id']} обновлен.")
            else:
                # Если склада нет, добавляем новый
                warehouse = Warehouse(**warehouse_data)
                self.session.add(warehouse)
                self.session.commit()
                self.warehouses_changed.emit()  # Сигнал об изменениях
                print(f"Склад с ID {warehouse_data['id']} добавлен.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при добавлении/обновлении склада: {str(e)}")

    def get_products(self):
        """Возвращает список всех продуктов."""
        return self.session.query(Product).all()

    def update_warehouse(self, warehouse_id, warehouse_data):
        """Обновляет данные склада."""
        try:
            warehouse = self.session.query(Warehouse).filter_by(id=warehouse_id).first()
            if warehouse:
                for key, value in warehouse_data.items():
                    setattr(warehouse, key, value)
                self.session.commit()  # Сохраняем изменения
                self.warehouses_changed.emit()
            else:
                raise Exception(f"Склад с ID {warehouse_id} не найден.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при обновлении склада: {str(e)}")

    def delete_warehouse(self, warehouse_id):
        """Удаляет склад."""
        try:
            warehouse = self.session.query(Warehouse).filter_by(id=warehouse_id).first()
            if warehouse:
                # Проверка, используется ли склад в товарах или отправлениях
                if self.session.query(Product).filter_by(warehouse_number=warehouse_id).count() > 0:
                    raise Exception("Невозможно удалить склад, так как на нем находятся товары.")
                if self.session.query(Shipment).filter_by(warehouse_id=warehouse_id).count() > 0:
                    raise Exception("Невозможно удалить склад, так как он используется в отправлениях.")

                self.session.delete(warehouse)
                self.session.commit()
                self.warehouses_changed.emit()
            else:
                raise Exception(f"Склад с ID {warehouse_id} не найден.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при удалении склада: {str(e)}")

    # Products
    def update_total_amount(self):
        """Обновляет общую сумму заказа на основе выбранного товара и количества."""
        product = self.product_input.currentText()
        quantity_text = self.quantity_input.text()

        try:
            quantity = int(quantity_text)
        except ValueError:
            quantity = 0

        # Получаем список продуктов из DataManager
        price = 0
        for p in self.data_manager.get_products():  # Используем метод вместо несуществующего атрибута
            if p.product_name == product:
                price = p.price
                break

        total = price * quantity
        self.total_amount_input.setText(f"{total:.2f}")

    def add_product(self, product_data):
        """Добавляет новый продукт или обновляет существующий."""
        try:
            # Попытка найти продукт с таким же ID
            existing_product = self.session.query(Product).filter_by(id=product_data['id']).first()

            if existing_product:
                # Если продукт существует, обновляем его
                for key, value in product_data.items():
                    setattr(existing_product, key, value)  # Обновляем поля продукта
                self.session.commit()
                self.products_changed.emit()  # Сигнал об изменениях
                print(f"Продукт с кодом {product_data['id']} обновлен.")
            else:
                # Если продукта нет, добавляем новый
                product = Product(**product_data)
                self.session.add(product)
                self.session.commit()
                self.products_changed.emit()  # Сигнал об изменениях
                print(f"Продукт с кодом {product_data['id']} добавлен.")

        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при добавлении/обновлении продукта: {str(e)}")

    def update_product(self, product_id, product_data):
        """Обновляет данные продукта."""
        product = self.session.query(Product).filter_by(id=product_id).first()
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            self.session.commit()
            self.products_changed.emit()

    def delete_product(self, product_id):
        """Удаляет продукт."""
        product = self.session.query(Product).filter_by(id=product_id).first()
        if product:
            self.session.delete(product)
            self.session.commit()
            self.products_changed.emit()

    # Contragents
    def get_contragents(self):
        """Возвращает список всех контрагентов."""
        try:
            return self.session.query(Contragent).all()
        except Exception as e:
            raise Exception(f"Ошибка при получении контрагентов: {str(e)}")

    def get_next_contragent_code(self):
        """Возвращает следующий уникальный код контрагента в формате C00001."""
        try:
            last_contragent = self.session.query(Contragent).order_by(Contragent.id.desc()).first()

            if last_contragent and last_contragent.id.startswith("C"):
                numeric_part = last_contragent.id[1:]  # Извлекаем числовую часть
                if numeric_part.isdigit():  # Проверяем, является ли это числом
                    next_code = int(numeric_part) + 1
                else:
                    next_code = 1  # Если ID не числовой, начинаем с 1
            else:
                next_code = 1  # Если контрагентов нет, начинаем с C00001

            # Генерация уникального ID
            next_id = f"C{next_code:03d}"
            while self.session.query(Contragent).filter_by(id=next_id).first() is not None:
                next_code += 1
                next_id = f"C{next_code:03d}"

            return next_id
        except Exception as e:
            raise Exception(f"Ошибка при генерации кода контрагента: {str(e)}")

    def add_contragent(self, contragent_data):
        """Добавляет нового контрагента или обновляет существующего."""
        try:
            # Попытка найти контрагента с таким же ID
            existing_contragent = self.session.query(Contragent).filter_by(id=contragent_data['id']).first()

            if existing_contragent:
                # Если контрагент существует, обновляем его
                for key, value in contragent_data.items():
                    setattr(existing_contragent, key, value)  # Обновляем поля контрагента
                self.session.commit()
                self.contragents_changed.emit()  # Сигнал об изменениях
                print(f"Контрагент с ID {contragent_data['id']} обновлён.")
            else:
                # Если контрагента нет, добавляем нового
                contragent = Contragent(**contragent_data)
                self.session.add(contragent)
                self.session.commit()
                self.contragents_changed.emit()  # Сигнал об изменениях
                print(f"Контрагент с ID {contragent_data['id']} добавлен.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при добавлении/обновлении контрагента: {str(e)}")

    def update_contragent(self, contragent_id, contragent_data):
        """Обновляет данные контрагента."""
        try:
            contragent = self.session.query(Contragent).filter_by(id=contragent_id).first()
            if contragent:
                for key, value in contragent_data.items():
                    setattr(contragent, key, value)  # Обновляем поля контрагента
                self.session.commit()
                self.contragents_changed.emit()
                print(f"Контрагент с ID {contragent_id} обновлён.")
            else:
                raise Exception(f"Контрагент с ID {contragent_id} не найден.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при обновлении контрагента: {str(e)}")

    def delete_contragent(self, contragent_id):
        """Удаляет контрагента."""
        try:
            contragent = self.session.query(Contragent).filter_by(id=contragent_id).first()
            if contragent:
                self.session.delete(contragent)
                self.session.commit()
                self.contragents_changed.emit()
                print(f"Контрагент с ID {contragent_id} удалён.")
            else:
                raise Exception(f"Контрагент с ID {contragent_id} не найден.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при удалении контрагента: {str(e)}")

    def get_clients(self):
        """Возвращает список клиентов (контрагентов с ролью 'Клиент')."""
        return [contragent for contragent in self.get_contragents() if contragent.role.lower() == 'клиент']

    def get_shipments(self):
        """Возвращает список всех отправлений."""
        return self.session.query(Shipment).all()

    def add_shipment(self, shipment_data):
        """Добавляет новое отправление."""
        shipment = Shipment(**shipment_data)
        self.session.add(shipment)
        self.session.commit()

    def delete_entity(self, entity):
        """Удаляет переданный объект."""
        self.session.delete(entity)
        self.session.commit()

    def close_session(self):
        """Закрывает сессию."""
        self.session.close()

# Инициализация базы (если нужно создать таблицы)
if __name__ == "__main__":
    Base.metadata.create_all(bind=SessionLocal().get_bind())
