import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import db


class ReturnWindow:
    def __init__(self, master, librarian_data=None, dashboard_root=None):
        self.master = master
        self.master.title("Return Book")
        self.master.geometry("900x450")

        self.librarian_data = librarian_data
        self.dashboard_root = dashboard_root

        tk.Label(master, text=f"Logged in as: {librarian_data['first_name']} {librarian_data['last_name']}",
                 fg="gray").pack(anchor="w", padx=10, pady=5)

        # Search bar
        search_frame = tk.Frame(master)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search: ").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_rows)

        # Table
        self.tree = ttk.Treeview(master, columns=("ID", "Student", "Book", "Borrow", "Due", "Status"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10)

        columns = ["ID", "Student", "Book", "Borrow Date", "Due Date", "Status"]
        for i, col in enumerate(columns):
            self.tree.heading(self.tree["columns"][i], text=col)

        # Return button
        tk.Button(master, text="Return Selected Book", command=self.return_book, bg="#4CAF50", fg="white").pack(pady=10)

        # Back Button
        tk.Button(master, text="Back", command=self.go_back).pack(pady=5)

        self.load_table_data()

    # ------------------------------
    # LOAD DATA INTO TABLE
    # ------------------------------
    def load_table_data(self):
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT bt.transaction_id, 
                   CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                   b.title AS book_title,
                   bt.borrow_date,
                   bt.due_date,
                   bt.status
            FROM borrow_transaction bt
            JOIN student s ON bt.student_id = s.student_id
            JOIN book b ON bt.book_id = b.book_id
            WHERE bt.status IN ('Active', 'Overdue')
        """

        data = db.execute_query(query)

        self.rows = []

        for row in data:
            overdue = (row["due_date"] < datetime.now().date())
            display_status = "Overdue" if overdue else row["status"]

            values = (
                row["transaction_id"],
                row["student_name"],
                row["book_title"],
                row["borrow_date"],
                row["due_date"],
                display_status
            )

            item_id = self.tree.insert("", "end", values=values)

            # Make overdue items red
            if overdue:
                self.tree.item(item_id, tags=("overdue",))

            self.rows.append(values)

        self.tree.tag_configure("overdue", foreground="red")

    # ------------------------------
    # SEARCH FUNCTION
    # ------------------------------
    def filter_rows(self, event=None):
        search = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        for row in self.rows:
            if any(search in str(value).lower() for value in row):
                item_id = self.tree.insert("", "end", values=row)
                if row[-1] == "Overdue":
                    self.tree.item(item_id, tags=("overdue",))

    # ------------------------------
    # RETURN BOOK
    # ------------------------------
    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a record to return.")
            return

        record = self.tree.item(selected)["values"]
        transaction_id, _, _, _, _, status = record

        # Confirm action
        if not messagebox.askyesno("Confirm Return", "Mark this book as returned?"):
            return

        update_query = """
            UPDATE borrow_transaction
            SET status = 'Returned', return_date = CURDATE()
            WHERE transaction_id = %s
        """

        # Increase book quantity
        get_book_query = "SELECT book_id FROM borrow_transaction WHERE transaction_id = %s"
        book = db.execute_query_one(get_book_query, (transaction_id,))
        if not book:
            messagebox.showerror("Error", "Book record not found.")
            return

        db.execute_query(update_query, (transaction_id,), fetch=False)
        db.execute_query("UPDATE book SET quantity = quantity + 1 WHERE book_id = %s",
                         (book['book_id'],), fetch=False)

        messagebox.showinfo("Success", "Book returned successfully!")
        self.load_table_data()

    # ------------------------------
    # BACK TO DASHBOARD
    # ------------------------------
    def go_back(self):
        self.master.destroy()
        if self.dashboard_root:
            self.dashboard_root.deiconify()
