from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from db import SessionLocal
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import ( QMessageBox )

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

class ShipmentAnalytics(Base):
    __tablename__ = 'shipment_analytics'

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

# DataManager
class DataManager(QObject):
    warehouses_changed = pyqtSignal()
    products_changed = pyqtSignal()
    contragents_changed = pyqtSignal()
    shipments_changed = pyqtSignal()
    analytics_changed = pyqtSignal()

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

    def get_product_by_name(self, product_name):
        """Поиск товара по имени в базе данных, игнорируя регистр."""
        # Ищем товар по имени, игнорируя пробелы и регистр
        for product in self.get_products():
            if product.product_name.strip().lower() == product_name.strip().lower():
                return product
        return None

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

    def delete_product(self, product_id):
        """Удаляет товар из базы данных."""
        try:
            # Находим товар по ID
            product = self.session.query(Product).filter(Product.id == product_id).first()

            if not product:
                raise Exception(f"Товар с кодом {product_id} не найден.")

            # Удаляем товар из базы данных
            self.session.delete(product)
            self.session.commit()
            print(f"Товар с кодом {product_id} успешно удалён.")  # Логирование
        except Exception as e:
            self.session.rollback()  # Откатываем транзакцию в случае ошибки
            raise Exception(f"Ошибка при удалении товара: {str(e)}")

    def delete_product_record(self, product_id):
        """Удаляет товар и обновляет склад."""
        try:
            # Получаем товар по ID
            product = self.get_product_by_id(product_id)

            if not product:
                raise Exception(f"Продукт с кодом {product_id} не найден.")

            # Проверим, что warehouse_number не пустой
            if not product.warehouse_number:
                raise Exception(f"Продукт с кодом {product_id} не привязан к складу.")

            print(f"Товар с кодом {product_id} найден, warehouse_number: {product.warehouse_number}")  # Отладка

            # Получаем склад, на котором находится товар
            warehouse = self.get_warehouse_by_id(product.warehouse_number)

            if not warehouse:
                raise Exception(f"Склад с ID {product.warehouse_number} не найден.")

            print(f"Склад с ID {warehouse.id} найден, текущая загруженность: {warehouse.capacity}")  # Отладка

            # Уменьшаем загруженность склада на количество удаляемого товара
            warehouse.capacity -= product.quantity
            self.update_warehouse(warehouse.id, {"capacity": warehouse.capacity})

            # Удаляем товар
            print(f"Удаляем товар с ID: {product.id}")  # Отладка
            self.delete_product(product.id)

            # Попробуем заново найти товар, чтобы убедиться, что он удалён
            deleted_product = self.get_product_by_id(product.id)
            if deleted_product:
                raise Exception(f"Ошибка: товар с кодом {product.id} не был удалён.")

            print(f"Товар с кодом {product_id} успешно удалён.")  # Отладка
            return product  # Возвращаем удалённый товар, чтобы обновить склад

        except Exception as e:
            # Выводим ошибку с использованием исключения
            raise Exception(f"Ошибка при удалении товара: {str(e)}")

    def update_warehouse_capacity(self, warehouse_id, quantity):
        """Уменьшает загруженность склада на количество удаляемого товара."""
        try:
            # Получаем склад по ID
            warehouse = self.data_manager.get_warehouse_by_id(warehouse_id)

            if not warehouse:
                raise Exception(f"Склад с ID {warehouse_id} не найден.")

            # Уменьшаем загруженность склада
            warehouse.capacity -= quantity
            self.data_manager.update_warehouse(warehouse.id, {"capacity": warehouse.capacity})

        except Exception as e:
            raise Exception(f"Ошибка при обновлении склада: {str(e)}")


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

    def update_product(self, product_id, product_data):
        """Обновляет данные продукта."""
        try:
            # Получаем товар по ID
            product = self.session.query(Product).filter_by(id=product_id).first()
            if product:
                # Обновляем данные товара
                for key, value in product_data.items():
                    setattr(product, key, value)
                self.session.commit()
                self.products_changed.emit()  # Сигнал об изменениях

                print(f"[DEBUG] Продукт с кодом {product_id} обновлен.")
            else:
                print(f"[DEBUG] Продукт с кодом {product_id} не найден.")
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при обновлении продукта: {str(e)}")


    def add_product(self, product_data):
        """Добавляет новый продукт или обновляет существующий."""
        try:
            # Получаем склад, на котором будет добавлен товар
            warehouse = self.session.query(Warehouse).filter_by(id=product_data['warehouse_number']).first()

            if not warehouse:
                raise Exception("Склад не найден. Убедитесь, что указали правильный склад.")

            print(
                f"[DEBUG] Добавление продукта: Код товара = {product_data['id']}, Количество = {product_data['quantity']}")

            # Проверка, если на складе достаточно места для добавления товара
            if warehouse.capacity + product_data['quantity'] > warehouse.max_capacity:
                raise Exception("На складе недостаточно места для добавления товара.")

            # Попытка найти продукт с таким же ID
            existing_product = self.session.query(Product).filter_by(id=product_data['id']).first()

            if existing_product:
                # Если продукт существует, обновляем его количество
                existing_product.quantity += product_data['quantity']
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

            # Обновляем вместимость склада после добавления товара
            warehouse.capacity += product_data['quantity']
            print(f"[DEBUG] Обновление склада: Новый уровень загрузки склада = {warehouse.capacity}")
            self.session.commit()  # Сохраняем изменения в складе

        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при добавлении/обновлении продукта: {str(e)}")

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
        """Возвращает все заказы из базы данных."""
        try:
            return self.session.query(Shipment).all()  # Получаем все записи из таблицы Shipment
        except Exception as e:
            raise Exception(f"Ошибка при получении заказов: {str(e)}")

    def add_shipment(self, shipment_data):
        """Добавляет новый заказ в таблицу заказов."""
        try:
            shipment = Shipment(**shipment_data)
            self.session.add(shipment)
            self.session.commit()  # Сохраняем изменения в базе данных
            self.shipments_changed.emit()  # Эмитируем сигнал об изменениях
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при добавлении заказа: {str(e)}")

    def add_shipment_to_analytics(self, shipment):
        """Перемещает заказ в аналитику и обновляет статус."""
        existing_shipment = self.session.query(ShipmentAnalytics).filter_by(order_number=shipment.order_number).first()

        if existing_shipment:
            existing_shipment.status = "Ждёт подтверждения"
            self.session.commit()
            print(f"Заказ {shipment.order_number} уже существует в аналитике, обновили его статус.")
        else:
            shipment_analytics = ShipmentAnalytics(
                order_number=shipment.order_number,
                order_date=shipment.order_date,
                client_id=shipment.client_id,
                delivery_address=shipment.delivery_address,
                product_id=shipment.product_id,
                warehouse_id=shipment.warehouse_id,
                amount=shipment.amount,
                delivery_method=shipment.delivery_method,
                total_cost=shipment.total_cost,
                status="Ждёт подтверждения",
                time_info=None
            )
            self.session.add(shipment_analytics)
            self.session.commit()
            print(f"Заказ {shipment.order_number} был добавлен в аналитику.")

    def delete_entity(self, entity):
        """Удаляет переданный объект."""
        self.session.delete(entity)
        self.session.commit()

    def get_analytics(self):
        """Метод для получения данных из shipment_analytics."""
        try:
            analytics = self.session.query(ShipmentAnalytics).all()  # Загружаем все записи
            print(f"Данные из аналитики: {len(analytics)} записей.")  # Проверка вывода
            return analytics
        except Exception as e:
            print("Ошибка при получении данных аналитики:", e)
            return []

    def update_analytics(self):
        """Метод для обновления данных в аналитике и эмитирования сигнала."""
        try:
            # Пример логики обновления аналитики. Например, мы можем изменить статус или время.
            # Здесь добавьте вашу логику для обновления данных в shipment_analytics
            self.session.commit()
            # После изменения данных отправляем сигнал
            self.analytics_changed.emit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Ошибка при обновлении аналитики: {str(e)}")

    def delete_shipment(self, row_index):
        """Удаляет заказ из базы данных и возвращает товар на склад."""
        shipments = self.get_shipments()
        shipment = shipments[row_index]  # Получаем заказ по индексу строки

        try:
            # Получаем товар и склад, к которому он относится
            product = self.get_product_by_id(shipment.product_id)  # Получаем товар по ID
            warehouse = self.get_warehouse_by_id(shipment.warehouse_id)  # Получаем склад по ID

            # Проверяем, что товар и склад существуют
            if not product or not warehouse:
                raise Exception("Не удалось найти товар или склад для восстановления.")

            # Возвращаем количество товара на склад
            warehouse.capacity += shipment.amount
            product.quantity += shipment.amount

            # Обновляем склад и товар в базе данных
            self.update_warehouse(warehouse.id, {"capacity": warehouse.capacity})
            self.update_product(product.id, {"quantity": product.quantity})

            # Удаляем запись об отправке из базы данных
            self.session.delete(shipment)
            self.session.commit()  # Сохраняем изменения в базе данных

            self.shipments_changed.emit()  # Эмитируем сигнал об изменениях
        except Exception as e:
            self.session.rollback()  # Откатываем изменения в случае ошибки
            raise Exception(f"Ошибка при удалении отправления и возврате товара: {str(e)}")

    def close_session(self):
        """Закрывает сессию."""
        self.session.close()
