# warehouse_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QFormLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from data_manager import DataManager

class WarehouseDialog(QDialog):
    """Диалоговое окно для добавления/редактирования склада."""

    def __init__(self, data=None, data_manager=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать склад")
        self.resize(400, 500)
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

        self.data_manager = data_manager
        self.data = data

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Форма ввода данных склада
        form_layout = QVBoxLayout()

        # Номер склада
        code_label = QLabel("Номер склада:")
        code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(code_label)

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Введите номер склада")
        self.number_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.number_input)

        form_layout.addSpacing(15)

        # Тип склада
        type_label = QLabel("Тип склада:")
        type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(type_label)

        self.type_input = QComboBox()
        self.type_input.addItems(["Основной", "Вторичный", "Специальный"])
        form_layout.addWidget(self.type_input)

        form_layout.addSpacing(15)

        # Адрес склада
        address_label = QLabel("Адрес склада:")
        address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(address_label)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите адрес склада")
        self.address_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.address_input)

        form_layout.addSpacing(15)

        # Максимальная вместимость
        max_capacity_label = QLabel("Максимальная вместимость:")
        max_capacity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(max_capacity_label)

        self.max_capacity_input = QLineEdit()
        self.max_capacity_input.setPlaceholderText("Введите максимальную вместимость")
        self.max_capacity_input.setValidator(QIntValidator())  # Только числа
        self.max_capacity_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.max_capacity_input)

        form_layout.addSpacing(15)

        # Текущая загрузка
        load_label = QLabel("Текущая загрузка:")
        load_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(load_label)

        self.load_input = QLineEdit()
        self.load_input.setPlaceholderText("Введите текущую загрузку")
        self.load_input.setValidator(QIntValidator())  # Только числа
        self.load_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.load_input)

        form_layout.addSpacing(15)

        # Кнопки "Сохранить" и "Отмена"
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        save_button = QPushButton("Сохранить")
        save_button.setFixedWidth(376)
        save_button.setFixedHeight(54)
        save_button.clicked.connect(self.save_warehouse)
        button_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(316)
        cancel_button.setFixedHeight(49)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout.addStretch()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        if not data:  # Новое добавление
            try:
                next_code = self.data_manager.get_next_warehouse_code()  # Получаем следующий уникальный код склада
                self.number_input.setText(next_code)  # Устанавливаем его в поле ввода
                self.number_input.setEnabled(
                    False)  # Делаем поле только для чтения, чтобы пользователь не мог изменить код
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать код склада: {str(e)}")
                self.number_input.setText("ERROR")
                self.number_input.setEnabled(False)

        # Если это редактирование, заполняем поля данными
        if self.data:
            self.set_data(self.data)

    def set_data(self, data):
        """Заполняем поля для редактирования."""
        # Используем точечный доступ для объекта Warehouse
        self.number_input.setText(data.id)  # Используем data.id, а не data["id"]
        self.type_input.setCurrentText(data.type)
        self.address_input.setText(data.address)
        self.max_capacity_input.setText(str(data.max_capacity))
        self.load_input.setText(str(data.capacity))

    def get_data(self):
        """Возвращает данные из формы в виде словаря."""
        return {
            "id": self.number_input.text().strip(),
            "type": self.type_input.currentText(),
            "address": self.address_input.text().strip(),
            "max_capacity": int(self.max_capacity_input.text().strip()),
            "capacity": int(self.load_input.text().strip())
        }

    def save_warehouse(self):
        """Сохраняет данные о складе в базе данных."""
        data = self.get_data()
        try:
            if self.data:
                # Обновление склада, если редактирование
                self.data_manager.update_warehouse(self.data.id, data)  # Исправлено на self.data.id
            else:
                # Добавление нового склада
                self.data_manager.add_warehouse(data)
            self.accept()  # Закрытие окна после сохранения
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении склада: {str(e)}")

    def save_warehouse(self):
        """Сохраняет данные о складе в базе данных."""
        data = self.get_data()

        # Проверяем, чтобы текущая загрузка не превышала максимальную вместимость
        try:
            max_capacity = int(self.max_capacity_input.text())
            current_load = int(self.load_input.text())

            if current_load > max_capacity:
                QMessageBox.warning(self, "Ошибка", "Текущая загрузка не может превышать максимальную вместимость.")
                return  # Выход из метода, если загрузка больше вместимости

        except ValueError:
            pass  # Если значение не является числом, просто не выполняем проверку

        try:
            if self.data:
                # Обновление склада, если редактирование
                self.data_manager.update_warehouse(self.data.id, data)
            else:
                # Добавление нового склада
                self.data_manager.add_warehouse(data)
            self.accept()  # Закрытие окна после сохранения
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении склада: {str(e)}")


class WarehouseTab(QWidget):
    """Вкладка с таблицей складов."""

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager  # Хранение экземпляра DataManager для последующего использования

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        header_label = QLabel("<b>Управление складами</b>")
        layout.addWidget(header_label)

        # Таблица складов
        self.warehouse_table = QTableWidget()
        self.warehouse_table.setColumnCount(5)
        self.warehouse_table.setHorizontalHeaderLabels(
            ["Номер склада", "Тип склада", "Адрес", "Максимальная вместимость", "Текущая загрузка"]
        )
        self.warehouse_table.horizontalHeader().setStretchLastSection(True)
        self.warehouse_table.horizontalHeader().setDefaultSectionSize(150)
        self.warehouse_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.warehouse_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.warehouse_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.warehouse_table)

        # Кнопки управления: "Добавить", "Изменить", "Удалить"
        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить")
        edit_button = QPushButton("Изменить")
        delete_button = QPushButton("Удалить")
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        # Подключение кнопок к методам
        add_button.clicked.connect(self.add_warehouse)
        edit_button.clicked.connect(self.edit_warehouse)
        delete_button.clicked.connect(self.delete_warehouse)

        # Подключение сигнала изменения складов для обновления таблицы
        self.data_manager.warehouses_changed.connect(self.load_data)

        self.load_data()

    def load_data(self):
        """Загружает данные складов и отображает в таблице."""
        self.warehouse_table.setRowCount(0)  # Очищаем таблицу перед загрузкой данных
        warehouses = self.data_manager.get_warehouses()
        for warehouse in warehouses:
            row = self.warehouse_table.rowCount()
            self.warehouse_table.insertRow(row)
            self.warehouse_table.setItem(row, 0, QTableWidgetItem(warehouse.id))
            self.warehouse_table.setItem(row, 1, QTableWidgetItem(warehouse.type))
            self.warehouse_table.setItem(row, 2, QTableWidgetItem(warehouse.address))
            self.warehouse_table.setItem(row, 3, QTableWidgetItem(str(warehouse.max_capacity)))
            self.warehouse_table.setItem(row, 4, QTableWidgetItem(str(warehouse.capacity)))

    def add_warehouse_to_table(self, warehouse):
        """Добавляет склад в таблицу."""
        row = self.warehouse_table.rowCount()
        self.warehouse_table.insertRow(row)
        self.warehouse_table.setItem(row, 0, QTableWidgetItem(warehouse.id))  # Используем точечный доступ
        self.warehouse_table.setItem(row, 1, QTableWidgetItem(warehouse.type or ""))  # Используем type
        self.warehouse_table.setItem(row, 2, QTableWidgetItem(warehouse.address or ""))  # Используем address
        self.warehouse_table.setItem(row, 3, QTableWidgetItem(str(warehouse.max_capacity)))  # Используем max_capacity
        self.warehouse_table.setItem(row, 4, QTableWidgetItem(str(warehouse.capacity)))  # Используем capacity

    def add_warehouse(self):
        """Открывает диалог для добавления нового склада."""
        dialog = WarehouseDialog(data_manager=self.data_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            # Проверка корректности данных
            if not self.validate_data(data):
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
                return

            try:
                # Преобразуем данные и добавляем склад
                new_warehouse = {
                    "id": data["id"],  # Идентификатор склада
                    "type": data["type"],
                    "address": data["address"],
                    "max_capacity": int(data["max_capacity"]),
                    "capacity": int(data["capacity"]),
                }

                self.data_manager.add_warehouse(new_warehouse)
                self.load_data()  # Обновляем таблицу складов
                QMessageBox.information(self, "Успех", "Склад успешно добавлен.")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении склада: {str(e)}")

    def edit_warehouse(self):
        """Открывает диалог для редактирования выбранного склада."""
        selected_row = self.warehouse_table.currentRow()
        if selected_row >= 0:
            warehouse_id = self.warehouse_table.item(selected_row, 0).text()
            warehouse = self.data_manager.get_warehouse_by_id(warehouse_id)

            if warehouse:
                dialog = WarehouseDialog(data=warehouse, data_manager=self.data_manager)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_data = dialog.get_data()

                    # Проверка корректности данных
                    if not self.validate_data(new_data):
                        QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
                        return

                    # Обновление склада
                    self.data_manager.update_warehouse(warehouse.id, new_data)
                    self.load_data()  # Обновляем таблицу с новыми данными

                    QMessageBox.information(self, "Успех", "Склад успешно обновлён.")
            else:
                QMessageBox.warning(self, "Ошибка", "Склад не найден.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите склад для редактирования.")

    def delete_warehouse(self):
        """Удаляет выбранный склад."""
        selected_row = self.warehouse_table.currentRow()
        if selected_row >= 0:
            warehouse_id = self.warehouse_table.item(selected_row, 0).text()
            confirmation = QMessageBox.question(
                self,
                "Удаление склада",
                f"Вы уверены, что хотите удалить склад с ID {warehouse_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                try:
                    self.data_manager.delete_warehouse(warehouse_id)
                    self.load_data()  # Обновляем таблицу после удаления склада
                    QMessageBox.information(self, "Успех", "Склад успешно удалён.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении склада: {str(e)}")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите склад для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        # Проверяем только строки с использованием strip() для строковых значений
        required_fields = [data["id"], data["type"], data["address"], data["max_capacity"], data["capacity"]]
        if not all(str(field).strip() if isinstance(field, str) else field for field in required_fields):
            return False
        try:
            # Преобразуем max_capacity и capacity в целые числа
            max_capacity = int(data["max_capacity"])
            capacity = int(data["capacity"])
            if max_capacity <= 0 or capacity < 0:
                return False
            if capacity > max_capacity:
                return False
        except ValueError:
            return False
        return True
