import tkinter as tk
from tkinter import messagebox, ttk
import storage

class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер книг")
        self.root.geometry("600x400")

        # Frame для ввода
        input_frame = tk.Frame(root, pady=10)
        input_frame.pack(fill="x", padx=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(input_frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.entry_author = tk.Entry(input_frame, width=30)
        self.entry_author.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Год:").grid(row=2, column=0, sticky="w")
        self.entry_year = tk.Entry(input_frame, width=30)
        self.entry_year.grid(row=2, column=1, padx=5)

        btn_add = tk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        btn_add.grid(row=3, column=1, sticky="e", pady=5)

        # Frame для поиска
        search_frame = tk.Frame(root, pady=5)
        search_frame.pack(fill="x", padx=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side="left")
        self.entry_search = tk.Entry(search_frame, width=40)
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.bind("<KeyRelease>", self.search_books)

        # Список книг
        self.tree = ttk.Treeview(root, columns=("title", "author", "year"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("year", text="Год")
        
        self.tree.column("title", width=250)
        self.tree.column("author", width=200)
        self.tree.column("year", width=50)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_list()

    def refresh_list(self, books=None):
        # Очистка списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if books is None:
            books = storage.load_books()
            
        for book in books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["year"]))

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        year = self.entry_year.get()

        try:
            storage.add_book(title, author, year)
            self.refresh_list()
            # Очистка полей
            self.entry_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            self.entry_year.delete(0, tk.END)
            messagebox.showinfo("Успех", "Книга добавлена")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def search_books(self, event=None):
        query = self.entry_search.get()
        filtered = storage.filter_books(query)
        self.refresh_list(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()