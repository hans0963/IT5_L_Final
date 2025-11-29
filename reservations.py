import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, date
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
            FROM reservation r
            JOIN book b ON r.book_id = b.book_id
            JOIN student s ON r.student_id = s.student_id
            ORDER BY r.reservation_id DESC
        """

        rows = db.execute_query(query)

        now = datetime.now()

        for r in rows:
            tag = ""

            if r["expires_at"] and datetime.strptime(str(r["expires_at"]), "%Y-%m-%d %H:%M:%S") < now:
                tag = "expired"
                if r["status"] == "Active":
                    db.execute_query("UPDATE reservation SET status='Cancelled' WHERE reservation_id=%s",
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
        dialog.title("New Reservation")
        dialog.geometry("400x300")
        dialog.configure(bg="#ecf0f1")
        dialog.grab_set()

        students = db.execute_query("SELECT student_id, CONCAT(first_name, ' ', last_name) AS name FROM student")
        student_cb = ttk.Combobox(dialog, values=[f"{s['student_id']} - {s['name']}" for s in students])
        student_cb.pack(pady=10)

        books = db.execute_query("SELECT book_id, title FROM book WHERE quantity > 0")
        book_cb = ttk.Combobox(dialog, values=[f"{b['book_id']} - {b['title']}" for b in books])
        book_cb.pack(pady=10)

        def save():
            if not student_cb.get() or not book_cb.get():
                return messagebox.showwarning("Missing", "Select student and book.")

            student_id = student_cb.get().split(" - ")[0]
            book_id = book_cb.get().split(" - ")[0]

            now = datetime.now()
            expires = now + timedelta(hours=12)

            db.execute_query("""
                INSERT INTO reservation(book_id, student_id, reservation_date, ready_timestamp, expires_at, status)
                VALUES (%s, %s, %s, %s, %s, 'Active')
            """, (book_id, student_id, now.date(), now, expires))

            messagebox.showinfo("Success", "Reservation created.")
            dialog.destroy()
            self.load_reservations()

        tk.Button(dialog, text="Save", bg="#27ae60", fg="white",
                  width=15, command=save).pack(pady=20)

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

        db.execute_query("UPDATE reservation SET status='Ready' WHERE reservation_id=%s", (res_id,))
        self.load_reservations()

    def cancel_reservation(self):
        res_id = self.get_selected()
        if not res_id:
            return

        if messagebox.askyesno("Confirm", "Cancel this reservation?"):
            db.execute_query("UPDATE reservation SET status='Cancelled' WHERE reservation_id=%s", (res_id,))
            self.load_reservations()

    def fulfill_reservation(self):
        res_id = self.get_selected()
        if not res_id:
            return

        # Placeholder: connect to Borrow
        messagebox.showinfo("TODO", "Borrow conversion will be linked here.")
        db.execute_query("UPDATE reservation SET status='Fulfilled' WHERE reservation_id=%s", (res_id,))
        self.load_reservations()

