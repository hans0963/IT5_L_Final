import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import db


class ReservationWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root

        # Fix: user_data may use librarian_id instead of id
        self.librarian_id = user_data.get("librarian_id") or user_data.get("id")

        self.root.title("Book Reservations")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()
        self.load_reservations()

    # ===== Navigation =====
    def on_close(self):
        """Return to dashboard when closing window."""
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

        # Top navigation bar
        nav = tk.Frame(main_frame, bg="#2c3e50", height=60)
        nav.pack(fill=tk.X)

        tk.Button(nav, text="← Back", bg="#34495e", fg="white",
                  command=self.go_back).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(
            nav,
            text="Reservation Management",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT, padx=20)

        # Action buttons
        content = tk.Frame(main_frame, bg="#ecf0f1", padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)

        tk.Button(
            content, text="Create Reservation", bg="#27ae60", fg="white",
            width=18, command=self.open_reservation_dialog
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            content, text="Refresh", bg="#95a5a6", fg="white",
            width=18, command=self.load_reservations
        ).pack(side=tk.LEFT, padx=5)

        # Search area
        search_frame = tk.Frame(content, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, pady=10)

        tk.Label(search_frame, text="Search:", bg="#ecf0f1").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(search_frame, text="Search", command=self.search).pack(side=tk.LEFT)

        # Table frame
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Book", "Student", "Date", "Status"),
            show="headings", height=20
        )

        headers = ["Reservation ID", "Book Title", "Student", "Reserved On", "Status"]
        for col, name in zip(self.tree["columns"], headers):
            self.tree.heading(col, text=name)

        self.tree.pack(fill=tk.BOTH, expand=True)

    # ===== Load Reservations =====
    def load_reservations(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT r.reservation_id, b.title,
                   CONCAT(s.first_name,' ',s.last_name) AS student_name,
                   r.reservation_date, r.status
            FROM reservation r
            JOIN book b ON r.book_id = b.book_id
            JOIN student s ON r.student_id = s.student_id
            ORDER BY r.reservation_id DESC
        """

        rows = db.execute_query(query)

        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r["reservation_id"], r["title"], r["student_name"],
                    r["reservation_date"], r["status"]
                ))

    def search(self):
        term = self.search_entry.get().strip()

        if not term:
            return self.load_reservations()

        query = """
            SELECT r.reservation_id, b.title,
                   CONCAT(s.first_name,' ',s.last_name) AS student_name,
                   r.reservation_date, r.status
            FROM reservation r
            JOIN book b ON r.book_id = b.book_id
            JOIN student s ON r.student_id = s.student_id
            WHERE b.title LIKE %s OR s.first_name LIKE %s OR s.last_name LIKE %s
        """

        rows = db.execute_query(query, (f"%{term}%", f"%{term}%", f"%{term}%"))

        self.tree.delete(*self.tree.get_children())

        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r["reservation_id"], r["title"], r["student_name"],
                    r["reservation_date"], r["status"]
                ))

    # ===== Reservation Dialog =====
    def open_reservation_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Reserve a Book")
        dialog.geometry("400x350")
        dialog.configure(bg="#ecf0f1")
        dialog.grab_set()

        frame = tk.Frame(dialog, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Student dropdown
        tk.Label(frame, text="Select Student:", bg="#ecf0f1").pack(anchor="w")
        student_cb = ttk.Combobox(frame, width=35)
        student_cb.pack(pady=5)

        students = db.execute_query("SELECT student_id, first_name, last_name FROM student")
        student_map = {f"{s['first_name']} {s['last_name']}": s['student_id'] for s in students}
        student_cb["values"] = list(student_map.keys())

        # Book dropdown (only reservable books)
        tk.Label(frame, text="Select Book:", bg="#ecf0f1").pack(anchor="w")
        book_cb = ttk.Combobox(frame, width=35)
        book_cb.pack(pady=5)

        available_books = db.execute_query("SELECT book_id, title FROM book")
        book_map = {b["title"]: b["book_id"] for b in available_books}
        book_cb["values"] = list(book_map.keys())

        tk.Label(frame, text=f"Reservation Date: {date.today()}", bg="#ecf0f1").pack(pady=10)

        def save_reservation():
            if not student_cb.get() or not book_cb.get():
                return messagebox.showwarning("Missing Information", "Select both student and book.")

            query = """
                INSERT INTO reservation (book_id, student_id, reservation_date, status)
                VALUES (%s, %s, %s, 'Active')
            """

            values = (
                book_map[book_cb.get()],
                student_map[student_cb.get()],
                date.today()
            )

            if db.execute_query(query, values, fetch=False):
                messagebox.showinfo("Success", "Reservation created successfully!")
                dialog.destroy()
                self.load_reservations()

        tk.Button(dialog, text="Confirm Reservation", bg="#3498db", fg="white",
                  width=20, command=save_reservation).pack(pady=20)
