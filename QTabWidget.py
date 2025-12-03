import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QColorDialog, QMessageBox, QSpinBox,
    QCalendarWidget, QProgressBar
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, Qt


class TabbedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение с вкладками")
        self.setGeometry(100, 100, 600, 500)

        # Создаем виджет вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Создаем и добавляем вкладки
        self.create_file_tab()
        self.create_color_tab()
        self.create_calendar_tab()
        self.create_progress_tab()

    def create_file_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.file_label = QLabel("Файл не выбран")
        self.file_label.setStyleSheet("border: 1px solid gray; padding: 10px;")

        btn_open = QPushButton("Выбрать файл")
        btn_open.clicked.connect(self.open_file_dialog)

        btn_save = QPushButton("Сохранить файл")
        btn_save.clicked.connect(self.save_file_dialog)

        layout.addWidget(self.file_label)
        layout.addWidget(btn_open)
        layout.addWidget(btn_save)
        layout.addStretch()

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Файлы")

    def create_color_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.color_label = QLabel("Выбранный цвет")
        self.color_label.setStyleSheet("""
            border: 2px solid black;
            padding: 20px;
            font-weight: bold;
            font-size: 16px;
        """)
        self.color_label.setAlignment(Qt.AlignCenter)

        self.color_sample = QLabel()
        self.color_sample.setMinimumHeight(50)
        self.color_sample.setStyleSheet("background-color: white; border: 1px solid gray;")

        btn_color = QPushButton("Выбрать цвет")
        btn_color.clicked.connect(self.open_color_dialog)

        layout.addWidget(QLabel("Выберите цвет:"))
        layout.addWidget(self.color_sample)
        layout.addWidget(self.color_label)
        layout.addWidget(btn_color)
        layout.addStretch()

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Цвета")

    def create_calendar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.date_label = QLabel("Выбранная дата: ")

        self.calendar.clicked.connect(self.on_date_selected)

        layout.addWidget(QLabel("Календарь:"))
        layout.addWidget(self.calendar)
        layout.addWidget(self.date_label)
        layout.addStretch()

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Календарь")

    def create_progress_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Прогресс: 0%")

        btn_start = QPushButton("Запустить прогресс")
        btn_reset = QPushButton("Сбросить")

        btn_start.clicked.connect(self.start_progress)
        btn_reset.clicked.connect(self.reset_progress)

        layout.addWidget(QLabel("Прогресс-бар:"))
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        layout.addWidget(btn_start)
        layout.addWidget(btn_reset)
        layout.addStretch()

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Прогресс")

        # Таймер для прогресс-бара
        self.progress_timer = QTimer()
        self.progress_value = 0
        self.progress_timer.timeout.connect(self.update_progress)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "",
            "Все файлы (*);;Текстовые файлы (*.txt);;Изображения (*.png *.jpg)"
        )

        if file_name:
            self.file_label.setText(f"Выбран файл: {file_name}")

    def save_file_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_name:
            self.file_label.setText(f"Сохранено в: {file_name}")
            QMessageBox.information(self, "Успех", f"Файл сохранен:\n{file_name}")

    def open_color_dialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            # Обновляем цвет образца
            self.color_sample.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid gray;"
            )

            # Обновляем текст
            self.color_label.setText(f"Цвет: {color.name()}")
            self.color_label.setStyleSheet(
                f"border: 2px solid black; padding: 20px;"
                f"font-weight: bold; font-size: 16px;"
                f"color: {color.name()};"
            )

    def on_date_selected(self, date):
        self.date_label.setText(f"Выбранная дата: {date.toString('dd.MM.yyyy')}")

    def start_progress(self):
        if not self.progress_timer.isActive():
            self.progress_timer.start(100)  # Обновлять каждые 100 мс

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        self.progress_label.setText(f"Прогресс: {self.progress_value}%")

        if self.progress_value >= 100:
            self.progress_timer.stop()
            QMessageBox.information(self, "Завершено", "Прогресс достиг 100%!")

    def reset_progress(self):
        self.progress_timer.stop()
        self.progress_value = 0
        self.progress_bar.setValue(0)
        self.progress_label.setText("Прогресс: 0%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabbedApp()
    window.show()
    sys.exit(app.exec())