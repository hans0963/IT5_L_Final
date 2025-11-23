""" Books management GUI module """

import tkinter as tk
from tkinter import ttk, messagebox
from database import db

class BookmanagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root
        
        self.root.title("Book Management")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

        # Stayl Configuration
        style = ttk.Style()
        style.theme_use("clam")

        # Window Closer
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_book_management()

    def clear_frame(self):
        """ Clear all widgets from the frame """
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_closing(self):
        """ Handle window closing """
        self.go_back()

    def go_back(self):
        """ Return to Dashboard """
        self.root.destroy()
        self.dashboard_root.deiconify()

    def show_book_management(self):
        self.clear_frame()

        # Main Frame
        main_frame = tk.Frame(self.root, bg= '#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top Navigation Bar
        nav_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        # Back button
        back_button = tk.Button(
            nav_frame,
            text ="← Back to Dashboard",
            bg = '#34495e',
            fg ='white',
            cursor ='hand2',
            command = self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=20, pady=15)

        # Title
        title_label = tk.Label(
            nav_frame,
            text = "Book Management",
            bg = '#2c3e50',
            fg = 'white',
        )
        title_label.pack(side=tk.LEFT, padx=20)

        # User info
        user_label = tk.Label(
            nav_frame,
            text = f"Logged in as: {self.user_data['first_name']} {self.user_data['last_name']}",
            font = ('Arial', 10),
            bg = '#2c3e50',
            fg = 'white'
        )
        user_label.pack(side=tk.RIGHT, padx=20)

        # Content Frame
        content_frame = tk.Frame(main_frame, bg='#ecf0f1', padx = 20, pady = 20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Button Frame
        button_frame = tk.Frame(content_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=10)

        add_btn = tk.Button(
            button_frame,
            text = "Add Book",
            bg = '#27ae60',
            fg = 'white',
            cursor = 'hand2',
            width = 15,
            command = self.add_book_dialog
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(
            button_frame,
            text = "Edit Book",
            font = ('Arial', 10, 'bold'),
            bg = '#f39c12',
            fg = 'white',
            cursor = 'hand2',
            width = 15,
            command = self.edit_book
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            button_frame,
            text = "Delete Book",
            font = ('Arial', 10, 'bold'),
            bg = '#e74c3c',
            fg = 'white',
            cursor = 'hand2',
            width = 15,
            command = self.delete_book
        )
        delete_btn.pack(side=tk.LEFT, padx=10)

        refresh_btn = tk.Button(
            button_frame,
            text = "Refresh List",
            font = ('Arial', 10, 'bold'),
            bg = '#3498db',
            fg = 'white',
            cursor = 'hand2',
            width = 15,
            command = self.load_books
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Search Frame
        search_frame = tk.Frame(content_frame, bg='#ecf0f1')
        search_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            search_frame,
            text = "Search:",
            font = ('Arial', 10),
            bg = '#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(search_frame, font = ('Arial', 10), width = 30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(
            search_frame,
            text = "Search",
            font = ('Arial', 10),
            bg = '#95a5a6',
            fg = 'white',
            cursor = 'hand2',
            command = self.search_books
        )
        search_btn.pack(side=tk.LEFT, padx=5)

        # Table Frame
        table_frame = tk.Frame(content_frame, bg = 'white')
        table_frame.pack(fill = tk.BOTH, expand = True, pady = 10)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient = tk.VERTICAL)
        vsb.pack(side = tk.RIGHT, fill = tk.Y)

        hsb = ttk.Scrollbar(table_frame, orient = tk.HORIZONTAL)
        hsb.pack(side = tk.BOTTOM, fill = tk.X)

        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns = ('book_id', 'isbn', 'title', 'author', 'publisher', 'publication_year', 'category', 'location', 'quantity', 'status', 'date_added', 'created_at'),
            height = 20,
            yscrollcommand = vsb.set,
            xscrollcommand = hsb.set
        )

        vsb.config(command = self.tree.yview)
        hsb.config(command = self.tree.xview)

        # Define Columns
        self.tree.column('#0', width = 0, stretch = tk.NO)
        self.tree.column('book_id', anchor = tk.CENTER, width = 50)
        self.tree.column('isbn', anchor = tk.W, width = 100)
        self.tree.column('title', anchor = tk.W, width = 100)
        self.tree.column('author', anchor = tk.W, width = 150)
        self.tree.column('publisher', anchor = tk.W, width = 120)
        self.tree.column('publication_year', anchor = tk.W, width = 50)
        self.tree.column('category', anchor = tk.W, width = 100)
        self.tree.column('location', anchor = tk.W, width = 100)
        self.tree.column('quantity', anchor = tk.W, width = 80)
        self.tree.column('status', anchor = tk.W, width = 80)
        self.tree.column('date_added', anchor = tk.W, width = 120)
        self.tree.column('created_at', anchor = tk.W, width = 150)

        # Define Headings
        self.tree.heading('#0', text = '', anchor = tk.W)
        self.tree.heading('book_id', text = 'ID', anchor = tk.CENTER)
        self.tree.heading('isbn', text = 'ISBN', anchor = tk.W)
        self.tree.heading('title', text = 'Title', anchor = tk.W)
        self.tree.heading('author', text = 'Author', anchor = tk.W)
        self.tree.heading('publisher', text = 'Publisher', anchor = tk.W)
        self.tree.heading('publication_year', text = 'Publication Year', anchor = tk.W)
        self.tree.heading('category', text = 'Category', anchor = tk.W)
        self.tree.heading('location', text = 'Location', anchor = tk.W)
        self.tree.heading('quantity', text = 'Quantity', anchor = tk.W)
        self.tree.heading('status', text = 'Status', anchor = tk.W)
        self.tree.heading('date_added', text = 'Date Added', anchor = tk.W)
        self.tree.heading('created_at', text = 'Created At', anchor = tk.W)

        # Add alternating row colors
        self.tree.tag_configure('oddrow', background = '#f0f0f0')
        self.tree.tag_configure('evenrow', background = 'white')
        self.tree.pack(fill = tk.BOTH, expand = True)

        # Status bar
        status_frame = tk.Frame(content_frame, bg = '#ecf0f1')
        status_frame.pack(fill = tk.X, pady = 5)

        self.status_label = tk.Label(
            status_frame,
            text = "Ready",
            font = ('Arial', 9),
            bg = '#ecf0f1',
            fg = '#7f8c8d',
            anchor = tk.W
        )
        self.status_label.pack(fill = tk.X, padx = 5)

        # Load books data
        self.load_books()

    def load_books(self):
        """ Load books from database """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM book ORDER BY book_id DESC"
        books = db.execute_query(query)

        if books:
            for idx, books in enumerate(books):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert(
                    '',
                    tk.END,
                    values = (
                        books['book_id'],
                        books['isbn'],
                        books['title'],
                        books['author'],
                        books['publisher'],
                        books['publication_year'],
                        books['category'],
                        books['location'],
                        books['quantity'],
                        books['status'],
                        books['date_added'],
                        books['created_at']
                    ),
                    tags = (tag,)
                )
            self.status_label.config(text = f"Loaded {len(books)} books.")
        else:
            self.status_label.config(text = "No books found.")
    
    def search_books(self):
        """ Search books based on input """
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = """
        SELECT * FROM book
        WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
        ORDER BY book_id DESC
        """
        like_term = f"%{search_term}%"
        books = db.execute_query(query, (like_term, like_term, like_term))

        if books:
            for idx, books in enumerate(books):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert(
                    '',
                    tk.END,
                    values = (
                        books['book_id'],
                        books['isbn'],
                        books['title'],
                        books['author'],
                        books['publisher'],
                        books['publication_year'],
                        books['category'],
                        books['location'],
                        books['quantity'],
                        books['status'],
                        books['date_added'],
                        books['created_at']
                    ),
                    tags = (tag,)
                )
            self.status_label.config(text = f"Found {len(books)} matching books.")
        else:
            self.status_label.config(text = "No matching books found.")

    def add_book_dialog(self):
        """ Open dialog to add a new book """
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x350")   
        dialog.resizable(False, False)
        dialog.configure(bg='#ecf0f1')

        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()

        # Form frame
        form_frame = tk.Frame(dialog, bg='#ecf0f1', padx=30, pady=20) 
        form_frame.pack(fill=tk.BOTH, expand=True)

        # ISBN
        tk.Label(form_frame, text="ISBN:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 0, column = 0, sticky = 'w', pady = 5)
        isbn_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        isbn_entry.grid(row = 1, column = 0, pady = (0, 10))

        # Title
        tk.Label(form_frame, text="Title:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 2, column = 0, sticky = 'w', pady = 5)
        title_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        title_entry.grid(row = 3, column = 0, pady = (0, 10))

        # Author
        tk.Label(form_frame, text="Author:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 4, column = 0, sticky = 'w', pady = 5)
        author_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        author_entry.grid(row = 5, column = 0, pady = (0, 10))

        # Publisher
        tk.Label(form_frame, text="Publisher:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 6, column = 0, sticky = 'w', pady = 5)
        publisher_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        publisher_entry.grid(row = 7, column = 0, pady = (0, 20))

        # Publication_Year
        tk.Label(form_frame, text="Publication Year:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 8, column = 0, sticky = 'w', pady = 5)
        publication_year_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        publication_year_entry.grid(row = 9, column = 0, pady = (0, 10))

        # Category
        tk.Label(form_frame, text="Category:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 10, column = 0, sticky = 'w', pady = 5)
        category_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        category_entry.grid(row = 11, column = 0, pady = (0, 20))

        # Location
        tk.Label(form_frame, text="Location:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 12, column = 0, sticky = 'w', pady = 5)
        location_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        location_entry.grid(row = 13, column = 0, pady = (0, 20))

        # Quantity
        tk.Label(form_frame, text="Quantity:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 14, column = 0, sticky = 'w', pady = 5)
        quantity_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        quantity_entry.grid(row = 13, column = 0, pady = (0, 20))

        # Status
        tk.Label(form_frame, text="Status:", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 16, column = 0, sticky = 'w', pady = 5)
        status_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        status_entry.grid(row = 15, column = 0, pady = (0, 20))

        # Date_Added
        tk.Label(form_frame, text="Date Added (YYYY-MM-DD):", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 18, column = 0, sticky = 'w', pady = 5)
        date_added_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        date_added_entry.grid(row = 17, column = 0, pady = (0, 20))

        # Created_At
        tk.Label(form_frame, text="Created At (YYYY-MM-DD):", bg = '#ecf0f1', font = ('Arial', 10)).grid(row = 20, column = 0, sticky = 'w', pady = 5)
        created_at_entry = ttk.Entry(form_frame, font=('Arial', 10), width = 30)
        created_at_entry.grid(row = 19, column = 0, pady = (0, 20))

        def save_book():
            isbn = isbn_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            publisher = publisher_entry.get().strip()
            publication_year = publication_year_entry.get().strip()
            category = category_entry.get().strip()
            location = location_entry.get().strip()
            quantity = quantity_entry.get().strip()
            status = status_entry.get().strip()
            date_added = date_added_entry.get().strip()
            created_at = created_at_entry.get().strip()

            if not all([isbn, title, author, publisher, publication_year, category, location, quantity, status, date_added, created_at]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return
            
            from datetime import date
            query = """
                INSERT INTO book (isbn, title, author, publisher, publication_year, category, location, quantity, status, date_added, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (isbn, title, author, publisher, publication_year, category, location, quantity, status, date_added, created_at)
            
            if db.execute_query(query, params):
                messagebox.showinfo("Success", "New book added successfully.")
                dialog.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", "Failed to add new book.")
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#ecf0f1')
        button_frame.grid(row=20, column=0, pady=10)

        save_btn = tk.Button(button_frame, text = "Save", font = ('Arial', 10, 'bold'), bg = '#27ae60', fg = 'white',
                             cursor = 'hand2', width = 10, command = save_book)
        save_btn.pack(side = tk.LEFT, padx = 5)

        cancel_btn = tk.Button(button_frame, text = "Cancel", font = ('Arial', 10, 'bold'), bg = '#e74c3c', fg = 'white',
                                 cursor = 'hand2', width = 10, command = dialog.destroy)
        cancel_btn.pack(side = tk.LEFT, padx = 5)

    def edit_book(self):
        """ Edit Selected Book """
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a book to edit.")
            return
        
        messagebox.showinfo("Info", "Edit Book - Under Development")

    def delete_book(self):
        """ Delete Selected Book """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")
            return
        
        # Get book data
        item = self.tree.item(selected[0])
        book_id = item['values'][0]
        student_name = f"{item['values'][1]} {item['values'][2]}"

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the book: {student_name}'?\n\n This action cannot be undone."
            )
        
        if confirm:
            query = "DELETE FROM book WHERE book_id = %s"
            if db.execute_query(query, (book_id), fetch = False):
                messagebox.showinfo("Success", "Book deleted Successfully!")
                self.load_books()
            else:
                messagebox.showerror("Error", "Failed to delete the book.")