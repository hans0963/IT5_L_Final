import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import db

class ReservationWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root

        self.librarian_id = user_data.get("librarian_id") or user_data.get("id")

        self.root.title("Book Reservations")
        self.root.geometry("1000x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()
        self.load_reservations()

    # ---------------- Navigation ----------------
    def on_close(self):
        self.go_back()

    def go_back(self):
        self.root.destroy()
        self.dashboard_root.deiconify()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- UI Layout ----------------
    def build_ui(self):
        self.clear()

        main = tk.Frame(self.root, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main, bg="#2c3e50")
        header.pack(fill=tk.X)

        tk.Button(header, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(header, text="Reservation Management",
                 fg="white", bg="#2c3e50", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        tk.Label(header, text=f"Librarian: {self.user_data['first_name']} {self.user_data['last_name']}",
                 fg="white", bg="#2c3e50").pack(side=tk.RIGHT, padx=10)

        # Controls
        control = tk.Frame(main, bg="#ecf0f1")
        control.pack(fill=tk.X, pady=10)

        tk.Button(control, text="➕ Create Reservation", bg="#27ae60", fg="white",
                  width=18, command=self.create_reservation_dialog).pack(side=tk.LEFT, padx=5)

        tk.Button(control, text="🔄 Refresh", bg="#3498db", fg="white",
                  width=12, command=self.load_reservations).pack(side=tk.LEFT, padx=5)

        # Search
        tk.Label(control, text="Search:", bg="#ecf0f1").pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(control, textvariable=self.search_var, width=40).pack(side=tk.LEFT)
        tk.Button(control, text="Search", bg="#7f8c8d", fg="white",
                  command=self.search).pack(side=tk.LEFT, padx=5)

        # Table
        self.tree = ttk.Treeview(main, columns=("id", "book", "student", "date", "expires", "status"),
                                 show="headings", height=20)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=15)

        headers = ["ID", "Book", "Student", "Reserved On", "Expires", "Status"]
        for c, text in zip(self.tree["columns"], headers):
            self.tree.heading(c, text=text)
            self.tree.column(c, anchor=tk.CENTER, width=160)

        self.tree.tag_configure("expired", background="#ffcccc")
        self.tree.tag_configure("ready", background="#fdfd96")

        # Action buttons
        actions = tk.Frame(main, bg="#ecf0f1")
        actions.pack(pady=5)

        tk.Button(actions, text="Mark as READY", bg="#f39c12", fg="white",
                  command=self.mark_ready).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="CONFIRM Borrow", bg="#2980b9", fg="white",
                  command=self.fulfill_reservation).pack(side=tk.LEFT, padx=5)

        tk.Button(actions, text="Cancel Reservation", bg="#e74c3c", fg="white",
                  command=self.cancel_reservation).pack(side=tk.LEFT, padx=5)

    # ---------------- Load Reservations ----------------
    def load_reservations(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT reservation_id, b.title,
                   CONCAT(s.first_name,' ',s.last_name) AS student,
                   reservation_date, expires_at, r.status
            FROM reservations r
            JOIN books b ON r.book_id = b.book_id
            JOIN students s ON r.student_id = s.student_id
            ORDER BY r.reservation_id DESC
        """

        rows = db.execute_query(query)
        now = datetime.now()

        for r in rows:
            tag = ""

            # Auto mark expired
            if r["expires_at"] and datetime.strptime(str(r["expires_at"]), "%Y-%m-%d %H:%M:%S") < now:
                tag = "expired"
                if r["status"] == "Active":
                    db.execute_query("UPDATE reservations SET status='Cancelled' WHERE reservation_id=%s",
                                     (r["reservation_id"],))
                    r["status"] = "Cancelled"

            if r["status"] == "Ready":
                tag = "ready"

            self.tree.insert("", tk.END, tags=(tag,),
                             values=(r["reservation_id"], r["title"], r["student"],
                                     r["reservation_date"], r["expires_at"], r["status"]))

    # ---------------- Search ----------------
    def search(self):
        term = self.search_var.get().strip().lower()
        if not term:
            return self.load_reservations()

        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if term in str(values).lower():
                data.append(values)

        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=row)

    # ---------------- Create Reservation ----------------
    def create_reservation_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Reservation")
        dialog.geometry("400x300")
        dialog.configure(bg="#ecf0f1")
        dialog.grab_set()

        container = tk.Frame(dialog, bg="#ecf0f1")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ---- STUDENT ----
        tk.Label(container, text="Select Student:", bg="#ecf0f1",
                font=("Arial", 11, "bold")).pack(anchor="w", pady=(0,5))

        students = db.execute_query(
            "SELECT student_id, CONCAT(first_name, ' ', last_name) AS name FROM students"
        )
        self.student_cb = ttk.Combobox(
            container,
            values=[f"{s['student_id']} - {s['name']}" for s in students],
            width=40,
            state="readonly"
        )
        self.student_cb.pack(pady=(0,10))

        # ---- BOOK ----
        tk.Label(container, text="Select Book:", bg="#ecf0f1",
                font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,5))

        books = db.execute_query(
            "SELECT book_id, title FROM books WHERE quantity > 0"
        )
        self.book_cb = ttk.Combobox(
            container,
            values=[f"{b['book_id']} - {b['title']}" for b in books],
            width=40,
            state="readonly"
        )
        self.book_cb.pack(pady=(0,10))

        # ---- BUTTON ----
        tk.Button(
            container,
            text="Save Reservation",
            bg="#27ae60",
            fg="white",
            width=20,
            height=1,
            font=("Arial", 11, "bold"),
            command=lambda: self.save_reservation(dialog)
        ).pack(pady=20)

    def save_reservation(self, dialog):
        if not self.student_cb.get() or not self.book_cb.get():
            return messagebox.showwarning("Missing Data", "Please select both student and book.")

        student_id = self.student_cb.get().split(" - ")[0]
        book_id = self.book_cb.get().split(" - ")[0]

        success = db.execute_query("""
            INSERT INTO reservations
            (book_id, student_id, reservation_date, status, expires_at)
            VALUES
            (%s, %s, NOW(), 'Active', DATE_ADD(NOW(), INTERVAL 7 DAY))
        """, (book_id, student_id), fetch=False)

        if success:
            messagebox.showinfo("Success", "Reservation created successfully!")
            dialog.destroy()
            self.load_reservations()
        else:
            messagebox.showerror("Error", "Failed to create reservation.")


    # ---------------- Status Actions ----------------
    def get_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a reservation.")
            return None
        return self.tree.item(selection)["values"][0]

    def mark_ready(self):
        res_id = self.get_selected()
        if not res_id:
            return
        db.execute_query("UPDATE reservations SET status='Ready' WHERE reservation_id=%s", (res_id,))
        self.load_reservations()

    def cancel_reservation(self):
        res_id = self.get_selected()
        if not res_id:
            return

        if messagebox.askyesno("Confirm", "Cancel this reservation?"):
            db.execute_query("UPDATE reservations SET status='Cancelled' WHERE reservation_id=%s", (res_id,))
            self.load_reservations()

    def fulfill_reservation(self):
        res_id = self.get_selected()
        if not res_id:
            return

        reservation = db.execute_query(
            "SELECT student_id, book_id FROM reservations WHERE reservation_id=%s", (res_id,)
        )
        if not reservation:
            messagebox.showerror("Error", "Reservation not found.")
            return

        student_id = reservation[0]["student_id"]
        book_id = reservation[0]["book_id"]

        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=7)
        librarian_id = self.librarian_id

        db.execute_query("""
            INSERT INTO borrow_transactions(student_id, book_id, librarian_id, borrow_date, due_date, status)
            VALUES(%s, %s, %s, %s, %s, 'Active')
        """, (student_id, book_id, librarian_id, borrow_date, due_date))

        db.execute_query("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
        db.execute_query("UPDATE reservations SET status='Fulfilled' WHERE reservation_id=%s", (res_id,))

        messagebox.showinfo("Success", "Book borrowed and reservation fulfilled!")
        self.load_reservations()
