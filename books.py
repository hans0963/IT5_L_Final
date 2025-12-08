"""
Books management GUI module
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import db
from validators import validate_book_fields
from datetime import date


class BookmanagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root
        
        self.root.title("Book Management")
        self.root.geometry("1500x700")

        ttk.Style().theme_use("clam")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_book_management()

    # --------------------------------------------
    # NAVIGATION / UTILITIES
    # --------------------------------------------

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_closing(self):
        self.go_back()

    def go_back(self):
        self.root.destroy()
        self.dashboard_root.deiconify()

    # --------------------------------------------
    # MAIN MANAGEMENT SCREEN
    # --------------------------------------------

    def show_book_management(self):
        self.clear_frame()

        main = tk.Frame(self.root, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True)

        # ---- NAV BAR ----
        nav = tk.Frame(main, bg="#2c3e50", height=60)
        nav.pack(fill=tk.X)

        tk.Button(nav, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side=tk.LEFT, padx=20, pady=12)

        tk.Label(nav, text="📚 Book Management", font=("Arial", 14, "bold"),
                 bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=20)

        tk.Label(nav, text=f"Logged in as: {self.user_data['first_name']} {self.user_data['last_name']}",
                 bg="#2c3e50", fg="white").pack(side=tk.RIGHT, padx=20)

        # ---- CONTENT ----
        content = tk.Frame(main, bg="#ecf0f1", padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # ACTION BUTTONS
        actions = tk.Frame(content, bg="#ecf0f1")
        actions.pack(fill=tk.X, pady=10)

        tk.Button(actions, text="Add Book", width=15, bg="#27ae60", fg="white",
                  command=self.add_book_dialog).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Edit Book", width=15, bg="#f39c12", fg="white",
                  command=self.edit_book).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Delete Book", width=15, bg="#e74c3c", fg="white",
                  command=self.delete_book).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Refresh", width=15, bg="#3498db", fg="white",
                  command=self.load_books).pack(side=tk.LEFT, padx=5)

        # SEARCH BAR
        search = tk.Frame(content, bg="#ecf0f1")
        search.pack(fill=tk.X, pady=10)

        tk.Label(search, text="Search:", bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search, text="Search", bg="#95a5a6", fg="white",
                  command=self.search_books).pack(side=tk.LEFT)

        # TABLE
        table_frame = tk.Frame(content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("isbn", "title", "author", "publisher", "year", "category",
                     "location", "qty", "status", "added", "created"),
            show="headings"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        headers = ["ISBN", "Title", "Author", "Publisher", "Year",
                   "Category", "Location", "Qty", "Status", "Added", "Created"]
        for col, text in zip(self.tree["columns"], headers):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120)

        self.status_label = tk.Label(content, text="Ready", bg="#ecf0f1")
        self.status_label.pack(fill=tk.X)

        self.load_books()

    # --------------------------------------------
    # DATABASE ACTIONS
    # --------------------------------------------

    def load_books(self):
        self.tree.delete(*self.tree.get_children())
        rows = db.execute_query("SELECT * FROM books ORDER BY book_id DESC")

        if rows:
            for row in rows:
                self.tree.insert("", tk.END, iid=row["book_id"], values=(
                    row["isbn"], row["title"], row["author"], row["publisher"], row["publication_year"],
                    row["category"], row["location"], row["quantity"], row["status"],
                    row["date_added"], row["created_at"]
                ))

            self.status_label.config(text=f"Loaded {len(rows)} book(s).")
        else:
            self.status_label.config(text="⚠ No books found.")

    def search_books(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            return messagebox.showwarning("Missing Input", "Please enter a search term.")

        self.tree.delete(*self.tree.get_children())

        like = f"%{keyword}%"
        query = """SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s"""

        rows = db.execute_query(query, (like, like, like))

        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=(
                    row["isbn"], row["title"], row["author"], row["publisher"], row["publication_year"],
                    row["category"], row["location"], row["quantity"], row["status"],
                    row["date_added"], row["created_at"]
                ))

            self.status_label.config(text=f"🔍 Found {len(rows)} result(s).")
        else:
            self.status_label.config(text="❌ No results.")

    # --------------------------------------------
    # ADD / EDIT / DELETE
    # --------------------------------------------

    def add_book_dialog(self):
        self.open_book_form(mode="add")

    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Select a book to edit.")

        values = self.tree.item(selected, "values")
        book_id = selected[0]
        self.open_book_form(mode="edit", book_id=book_id, values=values)

    def open_book_form(self, mode, book_id=None, values=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book" if mode == "add" else "Edit Book")
        dialog.geometry("400x570")
        dialog.configure(bg="#ecf0f1")
        dialog.grab_set()

        form = tk.Frame(dialog, bg="#ecf0f1", padx=25, pady=20)
        form.pack(fill=tk.BOTH, expand=True)

        def field(label, default=""):
            tk.Label(form, text=label, bg="#ecf0f1").pack(anchor="w")
            entry = ttk.Entry(form, width=33)
            entry.insert(0, default)
            entry.pack(pady=4)
            return entry

        isbn = field("ISBN", values[0] if values else "")
        title = field("Title", values[1] if values else "")
        author = field("Author", values[2] if values else "")
        publisher = field("Publisher", values[3] if values else "")
        year = field("Publication Year", values[4] if values else "")
        category = field("Category", values[5] if values else "")
        location = field("Location", values[6] if values else "")
        qty = field("Quantity", values[7] if values else "")

        tk.Label(form, text="Status", bg="#ecf0f1").pack(anchor="w")
        status = ttk.Combobox(form, width=30, values=["Available", "Unavailable"])
        status.set(values[8] if values else "Available")
        status.pack(pady=4)

        # ---- BUTTONS ----
        button_frame = tk.Frame(dialog, bg="#ecf0f1")
        button_frame.pack(pady=15)

        def save():
            if not qty.get().isdigit():
                return messagebox.showwarning("Invalid Entry", "Quantity must be numeric.")

            if mode == "add":
                today = str(date.today())
                query = """INSERT INTO books (isbn,title,author,publisher,publication_year,category,
                           location,quantity,status,date_added,created_at)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                params = (isbn.get(), title.get(), author.get(), publisher.get(), year.get(),
                          category.get(), location.get(), qty.get(), status.get(), today, today)
            else:
                query = """UPDATE books SET isbn=%s,title=%s,author=%s,publisher=%s,publication_year=%s,
                           category=%s,location=%s,quantity=%s,status=%s WHERE book_id=%s"""
                params = (isbn.get(), title.get(), author.get(), publisher.get(), year.get(),
                          category.get(), location.get(), qty.get(), status.get(), book_id)

            db.execute_query(query, params)
            dialog.destroy()
            self.load_books()
            messagebox.showinfo("Success", "Record saved successfully.")

        tk.Button(button_frame, text="Save", width=10, bg="#27ae60", fg="white", command=save).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel", width=10, bg="#e74c3c", fg="white",
                  command=dialog.destroy).grid(row=0, column=1, padx=10)

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Select a book to delete.")

        title = self.tree.item(selected, "values")[1]

        if messagebox.askyesno("Confirm Delete", f"Delete book '{title}'?"):
            db.execute_query("DELETE FROM books WHERE book_id=%s", (selected[0],))
            self.load_books()
            messagebox.showinfo("Deleted", "Book removed successfully.")
