import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мое первое приложение")

        # Создаем кнопку
        self.button = QPushButton("Нажми меня!")
        self.button.clicked.connect(self.on_button_clicked)

        # Создаем layout и добавляем кнопку
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_clicked(self):
        print("Кнопка нажата!")
        self.button.setText("Нажато!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())