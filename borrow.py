import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import db

class BorrowWindow:
    def __init__(self, master, librarian_data, dashboard_root):
        self.master = master
        self.librarian_data = librarian_data
        self.dashboard_root = dashboard_root

        master.title("Borrow Book")
        master.geometry("550x350")

        tk.Label(master, text="Borrow Book", font=("Arial", 18, "bold")).grid(row=0, columnspan=2, pady=10)

        # Student dropdown
        tk.Label(master, text="Student:").grid(row=2, column=0, sticky="w", padx=10)
        self.student_cb = ttk.Combobox(master, width=40)
        self.student_cb.grid(row=2, column=1, padx=10, pady=5)

        # Book dropdown
        tk.Label(master, text="Book:").grid(row=3, column=0, sticky="w", padx=10)
        self.book_cb = ttk.Combobox(master, width=40)
        self.book_cb.grid(row=3, column=1, padx=10, pady=5)

        # Librarian (read only)
        tk.Label(master, text="Librarian:").grid(row=4, column=0, sticky="w", padx=10)
        self.librarian_label = tk.Label(master, text=f"{self.librarian_data['first_name']} {self.librarian_data['last_name']} (ID: {self.librarian_data['librarian_id']})")
        self.librarian_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Borrow date
        tk.Label(master, text="Borrow Date:").grid(row=5, column=0, sticky="w", padx=10)
        self.borrow_date_entry = tk.Entry(master, width=20)
        self.borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.borrow_date_entry.grid(row=5, column=1, padx=10, pady=5)

        # Due date
        tk.Label(master, text="Due Date:").grid(row=6, column=0, sticky="w", padx=10)
        self.due_date_entry = tk.Entry(master, width=20)
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        self.due_date_entry.grid(row=6, column=1, padx=10, pady=5)

        # Submit button
        tk.Button(master, text="Submit Borrow Request",
                  bg="#4CAF50", fg="white", width=25,
                  command=self.submit_borrow).grid(row=7, columnspan=2, pady=15)

        # Back button
        tk.Button(master, text="⬅ Back to Dashboard", bg="#d9534f", fg="white",
                  width=25, command=self.go_back).grid(row=8, columnspan=2, pady=5)

        self.load_dropdowns()

    def load_dropdowns(self):
        students = db.execute_query("SELECT student_id, first_name, last_name FROM student")
        self.student_map = {f"{s['first_name']} {s['last_name']} (ID:{s['student_id']})": s['student_id'] for s in students}
        self.student_cb['values'] = list(self.student_map.keys())

        books = db.execute_query("SELECT book_id, title FROM book WHERE quantity > 0")
        self.book_map = {f"{b['title']} (ID:{b['book_id']})": b['book_id'] for b in books}
        self.book_cb['values'] = list(self.book_map.keys())

    def submit_borrow(self):
        if not self.student_cb.get() or not self.book_cb.get():
            messagebox.showerror("Input Error", "Please select both a student and a book.")
            return

        student_id = self.student_map[self.student_cb.get()]
        book_id = self.book_map[self.book_cb.get()]
        librarian_id = self.librarian_data["librarian_id"]
        borrow_date = self.borrow_date_entry.get()
        due_date = self.due_date_entry.get()

        query = """
            INSERT INTO borrow_transaction (book_id, student_id, librarian_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s, 'Active')
        """

        if db.execute_query(query, (book_id, student_id, librarian_id, borrow_date, due_date), fetch=False):
            db.execute_query("UPDATE book SET quantity = quantity - 1 WHERE book_id = %s", (book_id,), fetch=False)

            messagebox.showinfo("Success", "Borrow recorded successfully!")

            # Close window and return to dashboard
            self.go_back()

        else:
            messagebox.showerror("Error", "Failed to process borrow request.")

    def go_back(self):
        self.master.destroy() 
        self.dashboard_root.deiconify()
        messagebox.showinfo("Success", "Borrow recorded successfully!")
    

