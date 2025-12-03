import customtkinter as ctk

# Настройка внешнего вида
ctk.set_appearance_mode("dark")  # Режимы: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Темы: "blue", "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Тестовое приложение")
        self.geometry("400x300")

        # Создаем виджеты
        self.label = ctk.CTkLabel(self, text="Привет, Мир!",
                                  font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Введите текст")
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Нажми меня",
                                    command=self.button_clicked)
        self.button.pack(pady=10)

        self.switch = ctk.CTkSwitch(self, text="Темная тема",
                                    command=self.switch_event)
        self.switch.pack(pady=20)

    def button_clicked(self):
        text = self.entry.get()
        self.label.configure(text=f"Вы ввели: {text}")

    def switch_event(self):
        if self.switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")


if __name__ == "__main__":
    app = App()
    app.mainloop()