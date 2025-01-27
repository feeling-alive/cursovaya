# warehouse_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QFormLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
from data_manager import DataManager

class WarehouseDialog(QDialog):
    """Диалоговое окно для добавления/редактирования склада."""

    def __init__(self, data=None):
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

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Отступ сверху
        main_layout.addSpacing(20)

        # Форма ввода данных склада с метками над полями
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)  # Отступ между элементами

        # Номер склада
        number_label = QLabel("Номер склада:")
        number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(number_label)

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Введите номер склада")
        self.number_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.number_input)

        # Тип склада
        type_label = QLabel("Тип склада:")
        type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(type_label)

        self.type_input = QComboBox()
        self.type_input.addItems(["Основной", "Вторичный", "Специальный"])
        self.type_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.type_input)

        # Адрес склада
        address_label = QLabel("Адрес склада:")
        address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(address_label)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите адрес склада")
        self.address_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.address_input)

        # Максимальная вместимость
        max_capacity_label = QLabel("Максимальная вместимость:")
        max_capacity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(max_capacity_label)

        self.max_capacity_input = QLineEdit()
        self.max_capacity_input.setPlaceholderText("Введите максимальную вместимость")
        self.max_capacity_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.max_capacity_input)

        # Текущая загрузка
        load_label = QLabel("Текущая загрузка:")
        load_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(load_label)

        self.load_input = QLineEdit()
        self.load_input.setPlaceholderText("Введите текущую загрузку")
        self.load_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.load_input)

        main_layout.addLayout(form_layout)

        # Отступ перед кнопками
        main_layout.addSpacing(20)

        # Кнопки "Сохранить" и "Отмена" расположенные вертикально
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)  # Отступ между кнопками

        # Кнопка "Сохранить"
        save_button = QPushButton("Сохранить")
        save_button.setFixedWidth(376)
        save_button.setFixedHeight(54)
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(316)
        cancel_button.setFixedHeight(49)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем растяжение, если необходимо
        button_layout.addStretch()

        # Добавляем button_layout в основной layout
        main_layout.addLayout(button_layout)

        # Если данные переданы для редактирования, заполняем поля
        if data:
            self.set_data(data)

    def get_data(self):
        """Собирает данные из полей ввода и возвращает их в виде словаря."""
        return {
            "warehouse_number": self.number_input.text().strip(),
            "type": self.type_input.currentText(),
            "address": self.address_input.text().strip(),
            "max_capacity": self.max_capacity_input.text().strip(),
            "load": self.load_input.text().strip()
        }

    def set_data(self, data):
        """Заполняет поля ввода данными для редактирования."""
        self.number_input.setText(data.get("warehouse_number", ""))
        index = self.type_input.findText(data.get("type", ""))
        if index != -1:
            self.type_input.setCurrentIndex(index)
        self.address_input.setText(data.get("address", ""))
        self.max_capacity_input.setText(str(data.get("max_capacity", "")))
        self.load_input.setText(str(data.get("load", "")))

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
        """Загружает данные складов из DataManager и отображает их в таблице."""
        self.warehouse_table.setRowCount(0)
        for warehouse in self.data_manager.warehouses:
            self.add_warehouse_to_table(warehouse)

    def add_warehouse_to_table(self, warehouse):
        """Добавляет склад в таблицу."""
        row = self.warehouse_table.rowCount()
        self.warehouse_table.insertRow(row)
        self.warehouse_table.setItem(row, 0, QTableWidgetItem(warehouse["warehouse_number"]))
        self.warehouse_table.setItem(row, 1, QTableWidgetItem(warehouse["type"]))
        self.warehouse_table.setItem(row, 2, QTableWidgetItem(warehouse["address"]))
        self.warehouse_table.setItem(row, 3, QTableWidgetItem(str(warehouse["max_capacity"])))
        self.warehouse_table.setItem(row, 4, QTableWidgetItem(str(warehouse["load"])))

    def add_warehouse(self):
        """Открывает диалог для добавления нового склада."""
        dialog = WarehouseDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.validate_data(data):
                # Проверка уникальности номера склада
                if any(w["warehouse_number"] == data["warehouse_number"] for w in self.data_manager.warehouses):
                    QMessageBox.warning(self, "Ошибка", "Склад с таким номером уже существует.")
                    return
                try:
                    max_capacity = int(data["max_capacity"])
                    load = int(data["load"])
                    if load > max_capacity:
                        QMessageBox.warning(self, "Ошибка", "Текущая загрузка не может превышать максимальную вместимость.")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Максимальная вместимость и загрузка должны быть числами.")
                    return

                new_warehouse = {
                    "warehouse_number": data["warehouse_number"],
                    "type": data["type"],
                    "address": data["address"],
                    "max_capacity": max_capacity,
                    "load": load
                }
                self.data_manager.add_warehouse(new_warehouse)
                self.add_warehouse_to_table(new_warehouse)
                QMessageBox.information(self, "Успех", "Склад успешно добавлен.")
            else:
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")

    def edit_warehouse(self):
        """Открывает диалог для редактирования выбранного склада."""
        selected_row = self.warehouse_table.currentRow()
        if selected_row >= 0:
            warehouse = self.data_manager.warehouses[selected_row]
            dialog = WarehouseDialog(data=warehouse)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()
                if self.validate_data(new_data):
                    # Проверка уникальности номера склада, если он изменился
                    if new_data["warehouse_number"] != warehouse["warehouse_number"]:
                        if any(w["warehouse_number"] == new_data["warehouse_number"] for w in self.data_manager.warehouses):
                            QMessageBox.warning(self, "Ошибка", "Склад с таким номером уже существует.")
                            return
                    try:
                        max_capacity = int(new_data["max_capacity"])
                        load = int(new_data["load"])
                        if load > max_capacity:
                            QMessageBox.warning(self, "Ошибка", "Текущая загрузка не может превышать максимальную вместимость.")
                            return
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Максимальная вместимость и загрузка должны быть числами.")
                        return

                    updated_warehouse = {
                        "warehouse_number": new_data["warehouse_number"],
                        "type": new_data["type"],
                        "address": new_data["address"],
                        "max_capacity": max_capacity,
                        "load": load
                    }
                    self.data_manager.update_warehouse(selected_row, updated_warehouse)
                    # Обновляем таблицу
                    for i, key in enumerate(["warehouse_number", "type", "address", "max_capacity", "load"]):
                        self.warehouse_table.setItem(selected_row, i, QTableWidgetItem(str(updated_warehouse[key])))
                    QMessageBox.information(self, "Успех", "Склад успешно обновлён.")
                else:
                    QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите склад для редактирования.")

    def delete_warehouse(self):
        """Удаляет выбранный склад."""
        selected_row = self.warehouse_table.currentRow()
        if selected_row >= 0:
            confirmation = QMessageBox.question(
                self,
                "Удаление склада",
                "Вы уверены, что хотите удалить этот склад?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                # Проверка, используется ли склад в продуктах или заказах
                warehouse_number = self.data_manager.warehouses[selected_row]["warehouse_number"]
                used_in_products = any(p["warehouse_number"] == warehouse_number for p in self.data_manager.products_list)
                used_in_shipments = any(s["warehouse"] == warehouse_number for s in self.data_manager.shipments)
                if used_in_products or used_in_shipments:
                    QMessageBox.warning(
                        self,
                        "Невозможно удалить",
                        "Этот склад используется в продуктах или заказах и не может быть удалён."
                    )
                    return

                self.data_manager.delete_warehouse(selected_row)
                self.warehouse_table.removeRow(selected_row)
                QMessageBox.information(self, "Успех", "Склад успешно удалён.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите склад для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        required_fields = [
            data["warehouse_number"],
            data["type"],
            data["address"],
            data["max_capacity"],
            data["load"]
        ]
        if not all(field.strip() for field in required_fields):
            return False
        try:
            max_capacity = int(data["max_capacity"])
            load = int(data["load"])
            if max_capacity <= 0 or load < 0:
                return False
            if load > max_capacity:
                return False
        except ValueError:
            return False
        return True
