import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import db


class FineManagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root

        self.root.title("Fine Management")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()
        self.load_fines()

    # ===== Navigation =====
    def on_close(self):
        self.go_back()

    def go_back(self):
        self.root.destroy()
        self.dashboard_root.deiconify()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ===== UI Layout =====
    def build_ui(self):
        self.clear()

        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)

        nav = tk.Frame(main_frame, bg="#2c3e50", height=60)
        nav.pack(fill=tk.X)

        tk.Button(nav, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(nav, text="Fine Management",
                 bg="#2c3e50", fg="white", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        content = tk.Frame(main_frame, bg="#ecf0f1", padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)

        tk.Button(content, text="Refresh", bg="#95a5a6", fg="white",
                  width=15, command=self.load_fines).pack(side=tk.LEFT, padx=5)

        # Table
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Student", "Book", "Amount", "Status", "Calc Date", "Paid Date"),
            show="headings", height=20
        )

        headers = ["Fine ID", "Student", "Book Title", "Amount",
                   "Payment Status", "Date Charged", "Date Paid"]

        for col, name in zip(self.tree["columns"], headers):
            self.tree.heading(col, text=name)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Action buttons area
        action_frame = tk.Frame(content, bg="#ecf0f1")
        action_frame.pack(fill=tk.X, pady=10)

        tk.Button(action_frame, text="Mark as Paid", bg="#27ae60", fg="white",
                  width=18, command=self.pay_fine).pack(side=tk.LEFT, padx=5)

        tk.Button(action_frame, text="Waive Fine", bg="#e74c3c", fg="white",
                  width=18, command=self.waive_fine).pack(side=tk.LEFT, padx=5)

    # ===== Load fines =====
    def load_fines(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT f.fine_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                   b.title, f.fine_amount, f.payment_status, f.calculated_date, f.paid_date
            FROM fine f
            JOIN borrow_transaction t ON f.transaction_id = t.transaction_id
            JOIN student s ON t.student_id = s.student_id
            JOIN book b ON t.book_id = b.book_id
            ORDER BY f.fine_id DESC
        """

        rows = db.execute_query(query)

        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=(
                    row["fine_id"],
                    row["student_name"],
                    row["title"],
                    f"₱{row['fine_amount']:.2f}",
                    row["payment_status"],
                    row["calculated_date"],
                    row["paid_date"] if row["paid_date"] else "—"
                ))

    # ===== Payment Action =====
    def pay_fine(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Select a fine record first.")

        fine_id = self.tree.item(selected[0])["values"][0]

        if messagebox.askyesno("Confirm Payment", "Mark this fine as PAID?"):
            today = date.today()
            query = """
                UPDATE fine
                SET payment_status='Paid', paid_date=%s
                WHERE fine_id=%s
            """

            if db.execute_query(query, (today, fine_id), fetch=False):
                messagebox.showinfo("Success", "Fine marked as PAID.")
                self.load_fines()

    # ===== Waive Action =====
    def waive_fine(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("No Selection", "Select a fine first.")

        fine_id = self.tree.item(selected[0])["values"][0]

        if messagebox.askyesno("Confirm", "Waive this fine? This cannot be undone."):
            query = """
                UPDATE fine
                SET payment_status='Waived', paid_date=NULL
                WHERE fine_id=%s
            """

            if db.execute_query(query, (fine_id,), fetch=False):
                messagebox.showinfo("Success", "Fine successfully waived.")
                self.load_fines()
