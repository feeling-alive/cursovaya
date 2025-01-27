# contragents_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QFormLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
from data_manager import DataManager

class ContragentDialog(QDialog):
    """Диалоговое окно для добавления/редактирования контрагента."""

    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать контрагента")
        self.resize(350, 600)
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

        # Форма ввода данных контрагента с метками над полями
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)  # Отступ между элементами

        # Организация
        org_label = QLabel("Организация:")
        org_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(org_label)

        self.org_input = QLineEdit()
        self.org_input.setPlaceholderText("Введите название организации")
        self.org_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.org_input)

        # Название товара
        product_label = QLabel("Название товара:")
        product_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(product_label)

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Введите название товара")
        self.product_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.product_input)

        # Спецификация
        spec_label = QLabel("Спецификация:")
        spec_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(spec_label)

        self.spec_input = QComboBox()
        self.spec_input.addItems(["Спецификация 1", "Спецификация 2", "Спецификация 3"])
        self.spec_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.spec_input)

        # Адрес
        address_label = QLabel("Адрес:")
        address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(address_label)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите адрес")
        self.address_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.address_input)

        # Реквизиты счёта
        account_label = QLabel("Реквизиты счёта:")
        account_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(account_label)

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Введите реквизиты счёта")
        self.account_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.account_input)

        # Роль
        role_label = QLabel("Роль:")
        role_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(role_label)

        self.role_input = QComboBox()
        self.role_input.addItems(["Поставщик", "Покупатель"])
        self.role_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(self.role_input)

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
        """Собирает данные из полей ввода и возвращает их в виде списка."""
        return [
            self.org_input.text().strip(),
            self.product_input.text().strip(),
            self.spec_input.currentText(),
            self.address_input.text().strip(),
            self.account_input.text().strip(),
            self.role_input.currentText()
        ]

    def set_data(self, data):
        """Заполняет поля ввода данными для редактирования."""
        if len(data) == 6:
            self.org_input.setText(data[0])
            self.product_input.setText(data[1])
            index = self.spec_input.findText(data[2])
            if index != -1:
                self.spec_input.setCurrentIndex(index)
            self.address_input.setText(data[3])
            self.account_input.setText(data[4])
            index = self.role_input.findText(data[5])
            if index != -1:
                self.role_input.setCurrentIndex(index)


class ContragentTab(QWidget):
    """Вкладка с таблицей контрагентов."""

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager  # Хранение экземпляра DataManager для последующего использования

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        header_label = QLabel("<b>Управление контрагентами</b>")
        layout.addWidget(header_label)

        # Таблица контрагентов
        self.contragent_table = QTableWidget()
        self.contragent_table.setColumnCount(6)
        self.contragent_table.setHorizontalHeaderLabels(
            ["Организация", "Название товара", "Спецификация", "Адрес", "Реквизиты счёта", "Роль"]
        )
        self.contragent_table.horizontalHeader().setStretchLastSection(True)
        self.contragent_table.horizontalHeader().setDefaultSectionSize(150)
        self.contragent_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contragent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.contragent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.contragent_table)

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
        add_button.clicked.connect(self.add_contragent)
        edit_button.clicked.connect(self.edit_contragent)
        delete_button.clicked.connect(self.delete_contragent)

        self.load_data()

    def load_data(self):
        """Загружает данные контрагентов из DataManager и отображает их в таблице."""
        self.contragent_table.setRowCount(0)
        for contragent in self.data_manager.contragents:
            self.add_contragent_to_table(contragent)

    def add_contragent_to_table(self, contragent):
        """Добавляет контрагента в таблицу."""
        row = self.contragent_table.rowCount()
        self.contragent_table.insertRow(row)
        self.contragent_table.setItem(row, 0, QTableWidgetItem(contragent["name"]))
        self.contragent_table.setItem(row, 1, QTableWidgetItem(contragent["product"]))
        self.contragent_table.setItem(row, 2, QTableWidgetItem(contragent["specification"]))
        self.contragent_table.setItem(row, 3, QTableWidgetItem(contragent["address"]))
        self.contragent_table.setItem(row, 4, QTableWidgetItem(contragent["account_number"]))
        self.contragent_table.setItem(row, 5, QTableWidgetItem(contragent["role"]))

    def add_contragent(self):
        """Открывает диалог для добавления нового контрагента."""
        dialog = ContragentDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.validate_data(data):
                new_contragent = {
                    "name": data[0],
                    "product": data[1],
                    "specification": data[2],
                    "address": data[3],
                    "account_number": data[4],
                    "role": data[5]
                }
                # Проверка уникальности, если необходимо (например, по имени организации)
                if any(c["name"] == new_contragent["name"] for c in self.data_manager.contragents):
                    QMessageBox.warning(self, "Ошибка", "Контрагент с таким названием уже существует.")
                    return

                self.data_manager.add_contragent(new_contragent)
                self.add_contragent_to_table(new_contragent)
                QMessageBox.information(self, "Успех", "Контрагент успешно добавлен.")
            else:
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")

    def edit_contragent(self):
        """Открывает диалог для редактирования выбранного контрагента."""
        selected_row = self.contragent_table.currentRow()
        if selected_row >= 0:
            contragent = self.data_manager.contragents[selected_row]
            dialog = ContragentDialog(data=[
                contragent["name"],
                contragent["product"],
                contragent["specification"],
                contragent["address"],
                contragent["account_number"],
                contragent["role"]
            ])
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()
                if self.validate_data(new_data):
                    updated_contragent = {
                        "name": new_data[0],
                        "product": new_data[1],
                        "specification": new_data[2],
                        "address": new_data[3],
                        "account_number": new_data[4],
                        "role": new_data[5]
                    }
                    # Проверка уникальности имени организации, если оно изменилось
                    if updated_contragent["name"] != contragent["name"]:
                        if any(c["name"] == updated_contragent["name"] for c in self.data_manager.contragents):
                            QMessageBox.warning(self, "Ошибка", "Контрагент с таким названием уже существует.")
                            return

                    self.data_manager.update_contragent(selected_row, updated_contragent)
                    # Обновляем таблицу
                    for i, key in enumerate(["name", "product", "specification", "address", "account_number", "role"]):
                        self.contragent_table.setItem(selected_row, i, QTableWidgetItem(str(updated_contragent[key])))
                    QMessageBox.information(self, "Успех", "Контрагент успешно обновлён.")
                else:
                    QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите контрагента для редактирования.")

    def delete_contragent(self):
        """Удаляет выбранного контрагента."""
        selected_row = self.contragent_table.currentRow()
        if selected_row >= 0:
            confirmation = QMessageBox.question(
                self,
                "Удаление контрагента",
                "Вы уверены, что хотите удалить этого контрагента?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data_manager.delete_contragent(selected_row)
                self.contragent_table.removeRow(selected_row)
                QMessageBox.information(self, "Успех", "Контрагент успешно удалён.")
        else:
            QMessageBox.warning(self, "Выбор строки", "Пожалуйста, выберите контрагента для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        return all(field.strip() for field in data)
