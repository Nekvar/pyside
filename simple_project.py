import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QCheckBox, QComboBox
)


class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример PySide6 - Форма")
        self.setGeometry(100, 100, 500, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()

        # 1. Горизонтальный layout для имени
        name_layout = QHBoxLayout()
        name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        # 2. Выпадающий список
        combo_label = QLabel("Выберите страну:")
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Россия", "США", "Германия", "Япония", "Китай"])

        # 3. Чекбоксы
        self.checkbox1 = QCheckBox("Согласен с условиями")
        self.checkbox2 = QCheckBox("Подписаться на рассылку")

        # 4. Текстовое поле для вывода
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # 5. Кнопки
        buttons_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Отправить")
        self.clear_btn = QPushButton("Очистить")
        self.exit_btn = QPushButton("Выход")

        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.exit_btn)

        # Добавляем всё в основной layout
        main_layout.addLayout(name_layout)
        main_layout.addWidget(combo_label)
        main_layout.addWidget(self.country_combo)
        main_layout.addWidget(self.checkbox1)
        main_layout.addWidget(self.checkbox2)
        main_layout.addWidget(self.output_text)
        main_layout.addLayout(buttons_layout)

        central_widget.setLayout(main_layout)

        # Подключаем сигналы
        self.submit_btn.clicked.connect(self.on_submit)
        self.clear_btn.clicked.connect(self.on_clear)
        self.exit_btn.clicked.connect(self.close)

    def on_submit(self):
        name = self.name_input.text()
        country = self.country_combo.currentText()
        terms = "Да" if self.checkbox1.isChecked() else "Нет"
        newsletter = "Да" if self.checkbox2.isChecked() else "Нет"

        result = f"""Данные отправлены:
        Имя: {name}
        Страна: {country}
        Согласие с условиями: {terms}
        Рассылка: {newsletter}
        """

        self.output_text.setText(result)

    def on_clear(self):
        self.name_input.clear()
        self.country_combo.setCurrentIndex(0)
        self.checkbox1.setChecked(False)
        self.checkbox2.setChecked(False)
        self.output_text.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())