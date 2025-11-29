import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import db


class ReturnWindow:
    def __init__(self, master, librarian_data=None, dashboard_root=None):
        self.master = master
        self.master.title("Return Books")
        self.master.geometry("1100x550")
        self.master.config(bg="#ecf0f1")

        self.librarian_data = librarian_data
        self.dashboard_root = dashboard_root

        # ======== Header ========
        header = tk.Frame(master, bg="#2c3e50", height=50)
        header.pack(fill="x")

        tk.Button(header, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side="left", padx=10, pady=10)

        tk.Label(header, text="Return Books", fg="white",
                 bg="#2c3e50", font=("Arial", 15, "bold")).pack(side="left", padx=20)

        tk.Label(header, text=f"Logged in as: {librarian_data['first_name']} {librarian_data['last_name']}",
                 fg="white", bg="#2c3e50", font=("Arial", 10)).pack(side="right", padx=10)

        # ======== Controls (Refresh + Search) ========
        control_frame = tk.Frame(master, bg="#ecf0f1")
        control_frame.pack(fill="x", pady=10)

        tk.Button(control_frame, text="Refresh", width=12, bg="#1abc9c", fg="white",
                  command=self.load_table).pack(side="left", padx=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(control_frame, textvariable=self.search_var, width=35)
        self.search_entry.pack(side="right", padx=5)
        tk.Button(control_frame, text="Search", width=10, bg="#3498db", fg="white",
                  command=self.filter_table).pack(side="right", padx=5)

        # ======== Table ========
        self.tree = ttk.Treeview(
            master,
            columns=("id", "student", "book", "borrow", "due", "status"),
            show="headings",
            height=18
        )
        self.tree.pack(fill="both", expand=True, padx=10)

        column_labels = ["ID", "Student", "Book", "Borrow Date", "Due Date", "Status"]
        widths = [60, 200, 250, 120, 120, 100]

        for col, label, width in zip(self.tree["columns"], column_labels, widths):
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")

        self.tree.tag_configure("overdue", foreground="red")

        # ======== Buttons (Return + Lost) ========
        bottom_frame = tk.Frame(master, bg="#ecf0f1")
        bottom_frame.pack(fill="x", pady=15)

        tk.Button(bottom_frame, text="Return Selected Book", bg="#27ae60", fg="white",
                  width=20, command=self.return_book).pack(side="left", padx=20)

        tk.Button(bottom_frame, text="Mark as Lost", bg="#e74c3c", fg="white",
                  width=20, command=self.mark_lost).pack(side="right", padx=20)

        self.load_table()

    # ------------ Load Borrowed Books ------------
    def load_table(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT bt.transaction_id, 
                   CONCAT(s.first_name, ' ', s.last_name) AS student,
                   b.title, bt.borrow_date, bt.due_date, 
                   COALESCE(bt.status,'Active') AS status
            FROM borrow_transaction bt
            JOIN student s ON bt.student_id = s.student_id
            JOIN book b ON bt.book_id = b.book_id
            WHERE LOWER(COALESCE(bt.status,'active')) IN ('active','overdue')
            ORDER BY bt.transaction_id DESC
        """

        data = db.execute_query(query)

        self.rows = []

        for row in data:
            overdue = row["due_date"] < datetime.now().date()

            # Auto-update overdue status
            if overdue and row["status"].lower() == "active":
                db.execute_query(
                    "UPDATE borrow_transaction SET status='Overdue' WHERE transaction_id=%s",
                    (row["transaction_id"],)
                )
                row["status"] = "Overdue"

            tag = "overdue" if row["status"].lower() == "overdue" else ""

            formatted_row = (
                row["transaction_id"], row["student"], row["title"],
                row["borrow_date"], row["due_date"], row["status"]
            )

            self.tree.insert("", "end", values=formatted_row, tags=(tag,))
            self.rows.append(formatted_row)

    # ------------ Search ------------
    def filter_table(self):
        term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        for row in self.rows:
            if term in str(row).lower():
                tag = "overdue" if str(row[-1]).lower() == "overdue" else ""
                self.tree.insert("", "end", values=row, tags=(tag,))

    # ------------ Return Book ------------
    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Select a record first.")

        transaction_id, _, _, _, due_date, status = self.tree.item(selected)["values"]

        # --- Create fine if overdue ---
        if status == "Overdue":
            days_late = (datetime.now().date() - datetime.strptime(str(due_date), "%Y-%m-%d").date()).days
            fine_amount = days_late * 5   # <-- rate per day

            db.execute_query("""
                INSERT INTO fine(transaction_id, fine_amount, calculated_date, payment_status)
                VALUES(%s, %s, CURDATE(), 'Unpaid')
            """, (transaction_id, fine_amount))

        # --- Update transaction to returned ---
        db.execute_query("""
            UPDATE borrow_transaction 
            SET status='Returned', return_date=CURDATE()
            WHERE transaction_id=%s
        """, (transaction_id,))

        # --- Return the book stock ---
        book = db.execute_query_one("""
            SELECT book_id FROM borrow_transaction WHERE transaction_id=%s
        """, (transaction_id,))

        db.execute_query("UPDATE book SET quantity = quantity + 1 WHERE book_id = %s", (book["book_id"],))

        self.load_table()
        messagebox.showinfo("Success", "Book successfully returned.")

    # ------------ Mark Lost ------------
    def mark_lost(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Please select a record.")

        transaction_id = self.tree.item(selected)["values"][0]

        if not messagebox.askyesno("Confirm", "Mark this book as lost?"):
            return

        db.execute_query(
            "INSERT INTO fine(transaction_id, amount, status) VALUES(%s,%s,'Unpaid')",
            (transaction_id, 300)
        )

        db.execute_query("UPDATE borrow_transaction SET status='Lost' WHERE transaction_id=%s",
                         (transaction_id,))

        self.load_table()
        messagebox.showinfo("Recorded", "Book marked as lost.")

    def go_back(self):
        self.master.destroy()
        if self.dashboard_root:
            self.dashboard_root.deiconify()
