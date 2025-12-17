import tkinter as tk
from tkinter import ttk, messagebox
from database import db
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class FineManagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root

        self.root.title("Fines Management")
        self.root.geometry("1000x600")
        self.root.config(bg="#ecf0f1")

        self.build_header()
        self.build_table()
        self.build_actions()

        self.load_fines()

    # ================= HEADER =================
    def build_header(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)

        # Back Button
        tk.Button(
            header,
            text="← Back",
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.go_back
        ).pack(side=tk.LEFT, padx=10, pady=10)

        # Title
        tk.Label(
            header,
            text="Fine Management",
            fg="white",
            bg="#2c3e50",
            font=("Arial", 18, "bold")
        ).pack(side=tk.LEFT, padx=20)

        # Librarian Name (full name)
        full_name = f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}"

        tk.Label(
            header,
            text=f"Librarian: {full_name}",
            fg="white",
            bg="#2c3e50",
            font=("Arial", 12)
        ).pack(side=tk.RIGHT, padx=20)

    # ================= TABLE =================
    def build_table(self):
        table_frame = tk.Frame(self.root, bg="#ecf0f1")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("fine_id", "transaction_id", "amount", "calc_date",
                     "paid_date", "status"),
            show="headings",
            height=20
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        headers = ["Fine ID", "Transaction ID", "Amount",
                   "Calculated", "Paid", "Status"]
        for c, t in zip(self.tree["columns"], headers):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=150, anchor=tk.CENTER)

    # ================= ACTION BUTTONS =================
    def build_actions(self):
        actions = tk.Frame(self.root, bg="#ecf0f1")
        actions.pack(pady=10)

        tk.Button(actions, text="Mark as PAID", bg="#27ae60", fg="white",
                  width=15, command=self.mark_paid).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Waive Fine", bg="#e67e22", fg="white",
                  width=15, command=self.waive_fine).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Generate Receipt", bg="#2980b9", fg="white",
                  width=18, command=self.generate_receipt).pack(side=tk.LEFT, padx=5)

    # ================= LOAD FINES =================
    def load_fines(self):
        self.tree.delete(*self.tree.get_children())

        rows = db.execute_query("""
            SELECT fine_id, transaction_id, fine_amount,
                   calculated_date, paid_date, payment_status
            FROM fines
            ORDER BY fine_id DESC
        """)

        if not rows:
            return

        for r in rows:
            self.tree.insert("", tk.END, values=(
                r["fine_id"],
                r["transaction_id"],
                f"Php{r['fine_amount']}",
                r["calculated_date"],
                r["paid_date"] if r["paid_date"] else "",
                r["payment_status"]
            ))

    # ================= HELPERS =================
    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Fine", "Please select a fine.")
            return None
        return self.tree.item(sel)["values"]

    # ================= ACTIONS =================
    def mark_paid(self):
        values = self.get_selected()
        if not values:
            return
        fine_id = values[0]

        db.execute_query("""
            UPDATE fines
            SET payment_status='Paid', paid_date=CURDATE()
            WHERE fine_id=%s
        """, (fine_id,))

        messagebox.showinfo("Success", "Fine marked as PAID.")
        self.load_fines()

    def waive_fine(self):
        values = self.get_selected()
        if not values:
            return
        fine_id = values[0]

        db.execute_query("""
            UPDATE fines
            SET payment_status='Waived', paid_date=NULL
            WHERE fine_id=%s
        """, (fine_id,))

        messagebox.showinfo("Success", "Fine has been waived.")
        self.load_fines()

    # ================= PDF RECEIPT =================
    def generate_receipt(self):
        values = self.get_selected()
        if not values:
            return

        fine_id, trans_id, amount, calc_date, paid_date, status = values

        save_dir = "D:/IT5_Screenshots/Receipts"
        os.makedirs(save_dir, exist_ok=True)

        file_path = f"{save_dir}/fine_receipt_{fine_id}.pdf"

        c = canvas.Canvas(file_path)
        c.setFont("Helvetica", 12)

        y = 800
        c.drawString(50, y, "Library Management System - Fine Receipt")
        y -= 40

        c.drawString(50, y, f"Receipt Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 30

        c.drawString(50, y, f"Fine ID: {fine_id}")
        y -= 25
        c.drawString(50, y, f"Transaction ID: {trans_id}")
        y -= 25
        c.drawString(50, y, f"Fine Amount: {amount}")
        y -= 25
        c.drawString(50, y, f"Calculated Date: {calc_date}")
        y -= 25
        c.drawString(50, y, f"Paid Date: {paid_date if paid_date else 'Not Paid'}")
        y -= 25
        c.drawString(50, y, f"Status: {status}")

        y -= 40
        c.drawString(50, y, "Thank you!")
        c.save()

        messagebox.showinfo("Receipt Saved", f"PDF saved to:\n{file_path}")

    # ================= BACK BUTTON =================
    def go_back(self):
        self.root.destroy()
        self.dashboard_root.deiconify()
