import tkinter as tk
from tkinter import ttk, messagebox
from database import db


class FineManagementWindow:
    def __init__(self, master, user_data=None, dashboard_root=None):
        self.master = master
        self.master.title("Fine Management")
        self.master.geometry("1100x700")

        self.user_data = user_data
        self.dashboard_root = dashboard_root

        # ===== HEADER =====
        header = tk.Frame(master, bg="#2c3e50", height=50)
        header.pack(fill="x")

        tk.Button(header, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side="left", padx=10, pady=10)

        tk.Label(header, text="Fine Management", fg="white",
                 bg="#2c3e50", font=("Arial", 15, "bold")).pack(side="left", padx=20)

        tk.Label(header, text=f"Logged in as: {self.user_data['first_name']} {self.user_data['last_name']}",
                 fg="white", bg="#2c3e50").pack(side="right", padx=10)

        # ===== CONTROLS =====
        controls = tk.Frame(master, pady=10)
        controls.pack(fill="x")

        tk.Label(controls, text="Search:").pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(controls, textvariable=self.search_var, width=40).pack(side="left")

        tk.Button(controls, text="Search", bg="#3498db", fg="white",
                  command=self.search_records).pack(side="left", padx=5)

        tk.Button(controls, text="Refresh", bg="#1abc9c", fg="white",
                  command=self.load_fines).pack(side="right", padx=10)

        # ===== TABLE =====
        self.tree = ttk.Treeview(master,
                                 columns=("id", "student", "book", "amount", "payment_status", "calculated_date"),
                                 show="headings", height=18)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        headers = ["Fine ID", "Student", "Book", "Amount", "Status", "Issued On"]
        for col, text in zip(self.tree["columns"], headers):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=150 if col != "id" else 70)

        self.tree.tag_configure("unpaid", foreground="red")

        # ===== BOTTOM BUTTONS =====
        bottom = tk.Frame(master, pady=10)
        bottom.pack()

        tk.Button(bottom, text="Mark as Paid", bg="#27ae60", fg="white",
                  width=18, command=self.mark_paid).pack(side="left", padx=10)

        tk.Button(bottom, text="Waive Fine", bg="#e67e22", fg="white",
                  width=18, command=self.waive_fine).pack(side="left", padx=10)

        tk.Button(bottom, text="Delete Fine", bg="#c0392b", fg="white",
                  width=18, command=self.delete_fine).pack(side="left", padx=10)

        self.load_fines()

    # ---------------- LOAD DATA ----------------
    def load_fines(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT f.fine_id,
                   CONCAT(s.first_name,' ',s.last_name) AS student,
                   b.title AS book,
                   f.fine_amount,
                   f.payment_status,
                   f.calculated_date
            FROM fines f
            JOIN borrow_transactions bt ON f.transaction_id = bt.transaction_id
            JOIN students s ON bt.student_id = s.student_id
            JOIN books b ON bt.book_id = b.book_id
        """

        rows = db.execute_query(query)
        for r in rows:
            tag = "unpaid" if r["payment_status"] == "Unpaid" else ""
            self.tree.insert("", "end", values=(
                r["fine_id"], r["student"], r["book"],
                f"₱{r['fine_amount']:.2f}", r["payment_status"], r["calculated_date"]
            ), tags=(tag,))

    # ---------------- SEARCH ----------------
    def search_records(self):
        keyword = self.search_var.get().lower()

        if not keyword:
            self.load_fines()
            return

        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT f.fine_id,
                   CONCAT(s.first_name,' ',s.last_name) AS student,
                   b.title AS book,
                   f.fine_amount,
                   f.payment_status,
                   f.calculated_date
            FROM fines f
            JOIN borrow_transactions bt ON f.transaction_id = bt.transaction_id
            JOIN students s ON bt.student_id = s.student_id
            JOIN books b ON bt.book_id = b.book_id
            WHERE s.first_name LIKE %s OR s.last_name LIKE %s OR b.title LIKE %s
        """

        key = f"%{keyword}%"
        results = db.execute_query(query, (key, key, key))

        for r in results:
            tag = "unpaid" if r["payment_status"] == "Unpaid" else ""
            self.tree.insert("", "end", values=(
                r["fine_id"], r["student"], r["book"],
                f"₱{r['fine_amount']:.2f}", r["payment_status"], r["calculated_date"]
            ), tags=(tag,))

    # ---------------- ACTIONS ----------------
    def mark_paid(self):
        selected = self.get_selected()
        if not selected:
            return

        fine_id = selected[0]

        db.execute_query("UPDATE fines SET payment_status='Paid', paid_date=CURDATE() WHERE fine_id=%s", (fine_id,))
        messagebox.showinfo("Updated", "Fine marked as paid.")
        self.load_fines()

    def waive_fine(self):
        selected = self.get_selected()
        if not selected:
            return

        fine_id = selected[0]
        if not messagebox.askyesno("Confirm", "Are you sure you want to waive this fine?"):
            return

        db.execute_query("UPDATE fines SET payment_status='Waived' WHERE fine_id=%s", (fine_id,))
        messagebox.showinfo("Updated", "Fine has been waived.")
        self.load_fines()

    def delete_fine(self):
        selected = self.get_selected()
        if not selected:
            return

        fine_id = selected[0]
        if not messagebox.askyesno("Confirm", "Are you sure you want to permanently delete this fine?"):
            return

        db.execute_query("DELETE FROM fines WHERE fine_id=%s", (fine_id,))
        messagebox.showinfo("Deleted", "Fine removed successfully.")
        self.load_fines()

    # ---------------- HELPERS ----------------
    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a fine first.")
            return None

        return self.tree.item(selected)["values"]

    def go_back(self):
        self.master.destroy()
        if self.dashboard_root:
            self.dashboard_root.deiconify()
