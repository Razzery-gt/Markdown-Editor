import markdown
from tkinter import *
from tkinter import scrolledtext, filedialog, messagebox

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Editor")
        self.root.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap='word', width=70, height=15)
        self.text_area.pack(padx=10, pady=(10, 5))

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=5)

        self.render_button = Button(self.button_frame, text="Преобразовать в HTML", command=self.render_markdown)
        self.render_button.pack(side=LEFT, padx=5)

        self.copy_button = Button(self.button_frame, text="Копировать HTML", command=self.copy_html)
        self.copy_button.pack(side=LEFT, padx=5)

        self.clear_button = Button(self.button_frame, text="Очистить", command=self.clear_fields)
        self.clear_button.pack(side=LEFT, padx=5)

        self.html_area = scrolledtext.ScrolledText(self.root, wrap='word', width=70, height=15)
        self.html_area.pack(padx=10, pady=(5, 10))

        self.create_menu()

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu.add_cascade(label="Файл", menu=file_menu)

    def render_markdown(self):
        markdown_text = self.text_area.get("1.0", END)
        try:
            html = markdown.markdown(markdown_text)
            self.html_area.delete("1.0", END)
            self.html_area.insert(END, html)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось преобразовать Markdown в HTML:\n{e}")

    def copy_html(self):
        html_text = self.html_area.get("1.0", END)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(html_text)
            messagebox.showinfo("Успех", "HTML успешно скопирован в буфер обмена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать HTML в буфер обмена:\n{e}")

    def clear_fields(self):
        self.text_area.delete("1.0", END)
        self.html_area.delete("1.0", END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".md",
                                                filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.delete("1.0", END)
                    self.text_area.insert(END, file.read())
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md",
                                                   filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get("1.0", END).strip())
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == "__main__":
    root = Tk()
    app = MarkdownEditor(root)
    root.mainloop()
