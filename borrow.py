import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import db

# Email utils (safe import: will not break even if empty)
try:
    from email_utils import send_book_available_notification
except:
    def send_book_available_notification(*args, **kwargs):
        pass


class BorrowManagementWindow:
    def __init__(self, master, user_data=None, dashboard_root=None):
        self.master = master
        self.master.title("Borrow Management")
        self.master.geometry("1150x550")

        self.user_data = user_data
        self.dashboard_root = dashboard_root

        # ===== HEADER UI =====
        header = tk.Frame(master, bg="#2c3e50", height=50)
        header.pack(fill="x")

        tk.Button(header, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side="left", padx=10, pady=10)

        tk.Label(header, text="Borrow Management", fg="white",
                 bg="#2c3e50", font=("Arial", 15, "bold")).pack(side="left", padx=20)

        tk.Label(header, text=f"Logged in as: {self.user_data['first_name']} {self.user_data['last_name']}",
                 fg="white", bg="#2c3e50").pack(side="right", padx=10)

        # ===== CONTROLS =====
        control_frame = tk.Frame(master, pady=10)
        control_frame.pack(fill="x")

        tk.Button(control_frame, text="Add Borrow Record", bg="#27ae60", fg="white",
                  command=self.borrow_dialog, width=18).pack(side="left", padx=5)

        tk.Label(control_frame, text="Search:", font=("Arial", 10)).pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(control_frame, textvariable=self.search_var, width=35).pack(side="left")

        tk.Button(control_frame, text="Search", bg="#3498db", fg="white",
                  command=self.search_records).pack(side="left", padx=8)

        tk.Button(control_frame, text="Refresh", bg="#1abc9c", fg="white",
                  command=self.load_records).pack(side="right", padx=10)

        # ===== TABLE =====
        columns = ("id", "student", "book", "borrow", "due", "status")
        self.tree = ttk.Treeview(master, columns=columns, show="headings", height=18)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        headers = ["ID", "Student", "Book", "Borrow Date", "Due Date", "Status"]
        for col, text in zip(columns, headers):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150 if col != "id" else 60, anchor="center")

        self.tree.tag_configure("overdue", foreground="red")

        self.load_records()

    # ================= Borrow Dialog =================
    def borrow_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Borrow Book")
        dialog.geometry("400x300")
        dialog.configure(bg="#ecf0f1")
        dialog.grab_set()

        # Fetch available books
        books = db.execute_query("SELECT book_id, title, quantity FROM books WHERE quantity > 0")

        if not books:
            messagebox.showwarning("Unavailable", "No books available for borrowing.")
            dialog.destroy()
            return

        students = db.execute_query("SELECT student_id, CONCAT(first_name, ' ', last_name) AS name FROM students")

        tk.Label(dialog, text="Select Student", bg="#ecf0f1",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=5)
        cb_student = ttk.Combobox(dialog,
                                  values=[f"{s['student_id']} - {s['name']}" for s in students],
                                  width=35)
        cb_student.pack(padx=20)

        tk.Label(dialog, text="Select Book", bg="#ecf0f1",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=10)
        cb_book = ttk.Combobox(dialog,
                               values=[f"{b['book_id']} - {b['title']}" for b in books],
                               width=35)
        cb_book.pack(padx=20)

        def save_borrow():
            if not cb_student.get() or not cb_book.get():
                messagebox.showwarning("Missing Entry", "All fields are required.")
                return

            student_id = cb_student.get().split(" - ")[0]
            book_id = cb_book.get().split(" - ")[0]

            # Check if book is reserved for someone else
            active_res = db.execute_query("""
                SELECT r.student_id
                FROM reservations r
                WHERE r.book_id=%s AND r.status='Ready'
                ORDER BY r.reservation_date ASC
                LIMIT 1
            """, (book_id,))

            if active_res:
                reserved_for = str(active_res[0]["student_id"])
                if reserved_for != student_id:
                    messagebox.showerror(
                        "Book Reserved",
                        "This book is reserved and ready for another student.\n"
                        "You cannot borrow it until the reservation expires."
                    )
                    return

            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=7)

            librarian_id = self.user_data.get("librarian_id") or self.user_data.get("id")

            # Insert borrow
            db.execute_query("""
                INSERT INTO borrow_transactions(student_id, book_id, librarian_id, borrow_date, due_date, status)
                VALUES(%s, %s, %s, %s, %s, 'Active')
            """, (student_id, book_id, librarian_id, borrow_date, due_date))

            # Reduce quantity
            db.execute_query("UPDATE books SET quantity = quantity - 1 WHERE book_id=%s", (book_id,))

            # Mark reservation as completed if used
            if active_res:
                db.execute_query("""
                    UPDATE reservations
                    SET status='Completed'
                    WHERE book_id=%s AND student_id=%s
                """, (book_id, student_id))

            messagebox.showinfo("Success", "Book Borrowed Successfully!")
            dialog.destroy()
            self.load_records()

        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", width=15,
                  command=save_borrow).pack(pady=20)

    # ================= Table Loader =================
    def load_records(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT bt.transaction_id,
                CONCAT(s.first_name, ' ', s.last_name) AS student,
                b.title AS book,
                bt.borrow_date,
                bt.due_date,
                bt.status
            FROM borrow_transactions bt
            JOIN students s ON bt.student_id = s.student_id
            JOIN books b ON bt.book_id = b.book_id
            ORDER BY bt.transaction_id DESC
        """

        data = db.execute_query(query)

        for row in data:
            status_value = row.get("status") or row.get("borrow_status") or "Active"

            # Auto-mark overdue
            if status_value == "Active" and row["due_date"] < datetime.now().date():
                status_value = "Overdue"
                db.execute_query(
                    "UPDATE borrow_transactions SET status='Overdue' WHERE transaction_id=%s",
                    (row["transaction_id"],)
                )

            tag = "overdue" if status_value == "Overdue" else ""

            self.tree.insert("", "end",
                             values=(row["transaction_id"], row["student"], row["book"],
                                     row["borrow_date"], row["due_date"], status_value),
                             tags=(tag,))

    # ================= Search =================
    def search_records(self):
        keyword = self.search_var.get().lower()
        if not keyword:
            self.load_records()
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        query = """
            SELECT bt.transaction_id,
                   CONCAT(s.first_name, ' ', s.last_name) AS student,
                   b.title AS book, bt.borrow_date, bt.due_date, bt.status
            FROM borrow_transactions bt
            JOIN students s ON bt.student_id = s.student_id
            JOIN books b ON bt.book_id = b.book_id
            WHERE s.first_name LIKE %s OR s.last_name LIKE %s OR b.title LIKE %s
        """

        key = f"%{keyword}%"
        results = db.execute_query(query, (key, key, key))

        for row in results:
            status_value = row.get("status") or "Active"
            tag = "overdue" if status_value == "Overdue" else ""

            self.tree.insert("", "end", values=(
                row["transaction_id"], row["student"], row["book"],
                row["borrow_date"], row["due_date"], status_value
            ), tags=(tag,))

    # ================= Back =================
    def go_back(self):
        self.master.destroy()
        if self.dashboard_root:
            self.dashboard_root.deiconify()
