import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Мое первое приложение")
label = QLabel("Привет, мир!", parent=window)
window.resize(300, 200)
window.show()
sys.exit(app.exec())