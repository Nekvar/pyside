import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt


class TableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример таблицы")
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Создаем таблицу
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Возраст", "Город"])

        # Настраиваем растяжение колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Добавляем тестовые данные
        self.add_sample_data()

        # Кнопки управления
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Добавить строку")
        delete_btn = QPushButton("Удалить выбранное")
        clear_btn = QPushButton("Очистить таблицу")

        add_btn.clicked.connect(self.add_row)
        delete_btn.clicked.connect(self.delete_row)
        clear_btn.clicked.connect(self.clear_table)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(clear_btn)

        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)

        # Подключаем двойной клик по ячейке
        self.table.cellDoubleClicked.connect(self.on_cell_double_click)

    def add_sample_data(self):
        data = [
            [1, "Иван Иванов", 25, "Москва"],
            [2, "Петр Петров", 30, "Санкт-Петербург"],
            [3, "Анна Сидорова", 22, "Казань"],
            [4, "Мария Кузнецова", 28, "Новосибирск"]
        ]

        self.table.setRowCount(len(data))

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))

                # Центрируем текст
                item.setTextAlignment(Qt.AlignCenter)

                # Делаем первую колонку неизменяемой
                if col == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table.setItem(row, col, item)

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Автоматически генерируем ID
        new_id = row_count + 1
        id_item = QTableWidgetItem(str(new_id))
        id_item.setTextAlignment(Qt.AlignCenter)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)

        self.table.setItem(row_count, 0, id_item)

        # Переходим к редактированию первой ячейки
        self.table.editItem(self.table.item(row_count, 1))

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Удалить строку {current_row + 1}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Внимание", "Выберите строку для удаления")

    def clear_table(self):
        self.table.setRowCount(0)

    def on_cell_double_click(self, row, column):
        item = self.table.item(row, column)
        if item:
            QMessageBox.information(
                self, "Информация о ячейке",
                f"Строка: {row + 1}, Колонка: {column + 1}\n"
                f"Значение: {item.text()}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.exit(app.exec())