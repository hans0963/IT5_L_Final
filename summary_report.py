import tkinter as tk
from tkinter import ttk, messagebox
from database import db


class SummaryReportWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root

        self.root.title("Summary Report")
        self.root.geometry("1000x600")
        self.root.config(bg="#ecf0f1")

        self.create_widgets()

    def create_widgets(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg="#2c3e50", height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        # Back button
        back_btn = tk.Button(
            top_bar,
            text="← Back",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
            cursor="hand2",
            width=10,
            command=self.back_to_dashboard
        )
        back_btn.pack(side=tk.LEFT, padx=20)

        # Title
        title_label = tk.Label(
            top_bar,
            text="Summary Report",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Logged in user
        user_label = tk.Label(
            top_bar,
            text=f"Logged in as: {self.user_data['first_name']} {self.user_data['last_name']}",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white"
        )
        user_label.pack(side=tk.RIGHT, padx=20)

        # Main content frame
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # White panel
        report_panel = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
        report_panel.pack(fill=tk.BOTH, expand=True)

        # Fetch data
        data = self.get_report_data()

        # Grid layout for summary metrics
        metrics = [
            ("Total Students", data["total_students"]),
            ("Total Books", data["total_books"]),
            ("Currently Borrowed", data["total_borrowed"]),
            ("Active Reservations", data["total_reservations"]),
            ("Fines Collected", f"₱ {data['fines_collected']:.2f}"),
            ("Fines Pending", f"₱ {data['fines_pending']:.2f}")
        ]

        for i, (label, value) in enumerate(metrics):
            tk.Label(report_panel, text=label, font=("Arial", 14), bg="white", anchor="w").grid(
                row=i, column=0, padx=30, pady=15, sticky="w"
            )
            tk.Label(report_panel, text=value, font=("Arial", 14, "bold"), bg="white", anchor="e").grid(
                row=i, column=1, padx=30, pady=15, sticky="e"
            )

    def get_report_data(self):
        conn = db.get_connection() if hasattr(db, "get_connection") else db.connection

        if conn is None:
            print("ERROR: Database connection failed in Summary Report")
            return {
                "total_students": 0,
                "total_books": 0,
                "total_borrowed": 0,
                "total_reservations": 0,
                "fines_collected": 0,
                "fines_pending": 0
            }

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM borrow_transactions WHERE return_date IS NULL")
            total_borrowed = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM reservations WHERE status = 'Pending'")
            total_reservations = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(fine_amount), 0) FROM fines WHERE payment_status = 'Paid'")
            fines_collected = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(fine_amount), 0) FROM fines WHERE payment_status = 'Unpaid'")
            fines_pending = cursor.fetchone()[0]

            return {
                "total_students": total_students,
                "total_books": total_books,
                "total_borrowed": total_borrowed,
                "total_reservations": total_reservations,
                "fines_collected": fines_collected,
                "fines_pending": fines_pending
            }

        except Exception as e:
            print("SUMMARY REPORT ERROR:", e)
            return {
                "total_students": 0,
                "total_books": 0,
                "total_borrowed": 0,
                "total_reservations": 0,
                "fines_collected": 0,
                "fines_pending": 0
            }

        finally:
            cursor.close()

    def back_to_dashboard(self):
        self.root.destroy()
        self.dashboard_root.deiconify()