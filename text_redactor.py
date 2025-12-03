import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QLabel, QDialog, QVBoxLayout,
    QPushButton, QLineEdit
)
from PySide6.QtGui import QAction, QIcon, QKeySequence, QFont
from PySide6.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(100, 100, 800, 600)

        self.current_file = None
        self.init_ui()

    def init_ui(self):
        # Центральный виджет - текстовое поле
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Создаем меню
        self.create_menu()

        # Создаем тулбар
        self.create_toolbar()

        # Создаем статус-бар
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Готов")
        self.status_bar.addPermanentWidget(self.status_label)

        # Показываем количество символов
        self.text_edit.textChanged.connect(self.update_status)
        self.update_status()

    def create_menu(self):
        # Меню "Файл"
        file_menu = self.menuBar().addMenu("&Файл")

        new_action = QAction("&Новый", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)

        open_action = QAction("&Открыть...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("&Сохранить", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction("Сохранить &как...", self)
        save_as_action.triggered.connect(self.save_file_as)

        exit_action = QAction("&Выход", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Меню "Правка"
        edit_menu = self.menuBar().addMenu("&Правка")

        undo_action = QAction("&Отменить", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction("&Повторить", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.text_edit.redo)

        cut_action = QAction("&Вырезать", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_edit.cut)

        copy_action = QAction("&Копировать", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)

        paste_action = QAction("&Вставить", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_edit.paste)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # Меню "Справка"
        help_menu = self.menuBar().addMenu("&Справка")

        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Панель инструментов")

        # Кнопка "Новый"
        new_btn = QAction("Новый", self)
        new_btn.triggered.connect(self.new_file)
        toolbar.addAction(new_btn)

        # Кнопка "Открыть"
        open_btn = QAction("Открыть", self)
        open_btn.triggered.connect(self.open_file)
        toolbar.addAction(open_btn)

        # Кнопка "Сохранить"
        save_btn = QAction("Сохранить", self)
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)

        toolbar.addSeparator()

        # Кнопки форматирования
        bold_btn = QAction("Жирный", self)
        bold_btn.setCheckable(True)
        bold_btn.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_btn)

    def new_file(self):
        if self.check_save():
            self.text_edit.clear()
            self.current_file = None
            self.setWindowTitle("Текстовый редактор - Новый файл")
            self.update_status()

    def open_file(self):
        if self.check_save():
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Открыть файл", "",
                "Текстовые файлы (*.txt);;Все файлы (*)"
            )

            if file_name:
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.text_edit.setText(content)

                    self.current_file = file_name
                    self.setWindowTitle(f"Текстовый редактор - {file_name}")
                    self.update_status()

                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_name:
            if not file_name.endswith('.txt'):
                file_name += '.txt'

            self.save_to_file(file_name)
            self.current_file = file_name
            self.setWindowTitle(f"Текстовый редактор - {file_name}")

    def save_to_file(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())

            self.status_label.setText(f"Файл сохранен: {file_name}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def check_save(self):
        if self.text_edit.toPlainText():
            reply = QMessageBox.question(
                self, "Сохранить изменения?",
                "Сохранить изменения в текущем файле?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )

            if reply == QMessageBox.Save:
                self.save_file()
                return True
            elif reply == QMessageBox.Discard:
                return True
            else:
                return False

        return True

    def toggle_bold(self):
        cursor = self.text_edit.textCursor()
        format = cursor.charFormat()
        format.setFontWeight(
            QFont.Bold if format.fontWeight() != QFont.Bold else QFont.Normal
        )
        cursor.mergeCharFormat(format)

    def update_status(self):
        text = self.text_edit.toPlainText()
        chars = len(text)
        words = len(text.split())
        lines = text.count('\n') + 1

        self.status_label.setText(f"Символов: {chars} | Слов: {words} | Строк: {lines}")

    def show_about(self):
        QMessageBox.about(
            self, "О программе",
            "Текстовый редактор v1.0\n\n"
            "Пример приложения на PySide6\n"
            "Создано для обучения GUI-программированию"
        )

    def closeEvent(self, event):
        if self.check_save():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())