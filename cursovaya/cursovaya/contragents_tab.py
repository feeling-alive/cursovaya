# contragents_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from data_manager import DataManager

class ContragentDialog(QDialog):
    """Диалоговое окно для добавления/редактирования контрагента."""

    def __init__(self, data=None, data_manager=None):
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

        self.data_manager = data_manager
        self.data = data

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addSpacing(20)

        # Форма ввода данных контрагента
        form_layout = QVBoxLayout()

        # Организация (ID)
        self.organization_input = QLineEdit()
        self.organization_input.setReadOnly(True)
        form_layout.addWidget(QLabel("Организация (ID):"))
        form_layout.addWidget(self.organization_input)

        # Название товара
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        form_layout.addWidget(QLabel("Название товара:"))
        form_layout.addWidget(self.name_input)

        # Спецификация (ручной ввод)
        self.specification_input = QLineEdit()
        self.specification_input.setPlaceholderText("Введите спецификацию")
        form_layout.addWidget(QLabel("Спецификация:"))
        form_layout.addWidget(self.specification_input)

        # Адрес
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите адрес")
        form_layout.addWidget(QLabel("Адрес:"))
        form_layout.addWidget(self.address_input)

        # Реквизиты счета
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Введите реквизиты счета")
        self.account_input.setValidator(QIntValidator())
        form_layout.addWidget(QLabel("Реквизиты счета:"))
        form_layout.addWidget(self.account_input)

        # Роль (Поставщик/Покупатель)
        self.role_input = QComboBox()
        self.role_input.addItems(["Поставщик", "Покупатель"])
        form_layout.addWidget(QLabel("Роль:"))
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
        save_button.clicked.connect(self.save_contragent)
        button_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.setFixedWidth(316)
        cancel_button.setFixedHeight(49)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем растяжение, если необходимо
        button_layout.addStretch()

        # Добавляем button_layout в основной layout
        main_layout.addLayout(button_layout)

        if not data:
            try:
                new_id = self.data_manager.get_next_contragent_code()
                self.organization_input.setText(new_id)
                self.organization_input.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать код контрагента: {str(e)}")
                self.organization_input.setText("ERROR")
                self.organization_input.setEnabled(False)

        # Если данные переданы для редактирования, заполняем поля
        if data:
            self.set_data(data)

    def get_data(self):
        """Возвращает данные из формы в виде словаря."""
        return {
            "id": self.organization_input.text().strip(),
            "product": self.name_input.text().strip(),
            "specification": self.specification_input.text().strip(),
            "address": self.address_input.text().strip(),
            "account_number": self.account_input.text().strip(),
            "role": self.role_input.currentText()
        }

    def set_data(self, data):
        """Заполняет поля формы данными."""
        self.organization_input.setText(data.get("id", ""))
        self.name_input.setText(data.get("product", ""))
        self.specification_input.setText(data.get("specification", ""))
        self.address_input.setText(data.get("address", ""))
        self.account_input.setText(data.get("account_number", ""))
        self.role_input.setCurrentText(data.get("role", ""))

    def save_contragent(self):
        """Сохраняет контрагента в базе данных."""
        data = self.get_data()

        if not data["product"] or not data["address"] or not data["account_number"]:
            QMessageBox.warning(self, "Ошибка ввода", "Заполните все обязательные поля.")
            return

        try:
            if self.data:
                self.data_manager.update_contragent(data["id"], data)
            else:
                self.data_manager.add_contragent(data)

            self.accept()  # Закрытие окна после успешного сохранения
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении контрагента: {str(e)}")


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
            ["Организация (ID)", "Название товара", "Спецификация", "Адрес", "Реквизиты счета", "Роль"]
        )
        self.contragent_table.horizontalHeader().setStretchLastSection(True)
        self.contragent_table.horizontalHeader().setDefaultSectionSize(150)
        self.contragent_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contragent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.contragent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.contragent_table)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить контрагента")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить контрагента")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Подключение кнопок к методам
        self.add_button.clicked.connect(self.add_contragent)
        self.edit_button.clicked.connect(self.edit_contragent)
        self.delete_button.clicked.connect(self.delete_contragent)

        self.load_data()

    def load_data(self):
        """Загружает данные контрагентов и отображает в таблице."""
        self.contragent_table.setRowCount(0)
        contragents = self.data_manager.get_contragents()

        for contragent in contragents:
            row = self.contragent_table.rowCount()
            self.contragent_table.insertRow(row)
            self.contragent_table.setItem(row, 0, QTableWidgetItem(contragent.id))
            self.contragent_table.setItem(row, 1, QTableWidgetItem(contragent.product))  # Было contragent.name
            self.contragent_table.setItem(row, 2, QTableWidgetItem(contragent.specification))
            self.contragent_table.setItem(row, 3, QTableWidgetItem(contragent.address))
            self.contragent_table.setItem(row, 4, QTableWidgetItem(contragent.account_number))
            self.contragent_table.setItem(row, 5, QTableWidgetItem(contragent.role))

    def add_contragent_to_table(self, contragent):
        """Добавляет контрагента в таблицу."""
        row = self.contragent_table.rowCount()
        self.contragent_table.insertRow(row)
        self.contragent_table.setItem(row, 0, QTableWidgetItem(contragent["id"]))
        self.contragent_table.setItem(row, 1, QTableWidgetItem(contragent["product"]))
        self.contragent_table.setItem(row, 2, QTableWidgetItem(contragent["specification"]))
        self.contragent_table.setItem(row, 3, QTableWidgetItem(contragent["address"]))
        self.contragent_table.setItem(row, 4, QTableWidgetItem(contragent["account_number"]))
        self.contragent_table.setItem(row, 5, QTableWidgetItem(contragent["role"]))

    def add_contragent(self):
        """Открывает диалог для добавления нового контрагента."""
        dialog = ContragentDialog(data_manager=self.data_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()  # Получаем данные из диалога

            # Проверка корректности данных
            if not self.validate_data(data):
                QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
                return

            try:
                # Формируем объект контрагента
                new_contragent = {
                    "id": data["id"],
                    "product": data["product"],
                    "specification": data["specification"],
                    "address": data["address"],
                    "account_number": data["account_number"],
                    "role": data["role"]
                }

                # Добавляем или обновляем контрагента (встроенная проверка уже есть в add_contragent)
                self.data_manager.add_contragent(new_contragent)

                # Обновляем таблицу контрагентов
                self.load_data()
                QMessageBox.information(self, "Успех", "Контрагент успешно добавлен.")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении контрагента: {str(e)}")

    def edit_contragent(self):
        """Открывает диалог для редактирования выбранного контрагента."""
        selected_row = self.contragent_table.currentRow()
        if selected_row >= 0:
            contragents = self.data_manager.get_contragents()  # Получаем список контрагентов
            if selected_row >= len(contragents):  # Проверяем, что индекс в пределах списка
                QMessageBox.warning(self, "Ошибка", "Выбранный контрагент не найден.")
                return

            contragent = contragents[selected_row]  # Выбираем нужного контрагента

            dialog = ContragentDialog(data={
                "id": contragent.id,
                "product": contragent.product,
                "specification": contragent.specification,
                "address": contragent.address,
                "account_number": contragent.account_number,
                "role": contragent.role
            }, data_manager=self.data_manager)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()
                if self.validate_data(new_data):
                    updated_contragent = {
                        "id": new_data["id"],
                        "product": new_data["product"],
                        "specification": new_data["specification"],
                        "address": new_data["address"],
                        "account_number": new_data["account_number"],
                        "role": new_data["role"]
                    }

                    # Проверка уникальности ID, если оно изменилось
                    if updated_contragent["id"] != contragent.id:
                        if any(c.id == updated_contragent["id"] for c in self.data_manager.get_contragents()):
                            QMessageBox.warning(self, "Ошибка", "Контрагент с таким ID уже существует.")
                            return

                    self.data_manager.update_contragent(contragent.id, updated_contragent)

                    # Обновляем данные в таблице
                    for i, key in enumerate(["id", "product", "specification", "address", "account_number", "role"]):
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
            contragent_id = self.contragent_table.item(selected_row, 0).text()  # Получаем ID контрагента из таблицы

            confirmation = QMessageBox.question(
                self,
                "Удаление контрагента",
                f"Вы уверены, что хотите удалить контрагента с ID {contragent_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                try:
                    self.data_manager.delete_contragent(contragent_id)  # Передаем корректный ID
                    self.contragent_table.removeRow(selected_row)  # Удаляем строку из таблицы
                    QMessageBox.information(self, "Успех", "Контрагент успешно удалён.")
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении контрагента: {str(e)}")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите контрагента для удаления.")

    def validate_data(self, data):
        """Проверяет корректность введенных данных."""
        return all(field.strip() for field in data)
