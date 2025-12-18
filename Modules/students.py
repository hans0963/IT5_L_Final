"""
Student Management GUI module (SQLite-compatible)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from Core.database import db
from Core.validators import validate_student_fields


class StudentManagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root
        
        self.root.title("Student Management")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_student_management()
    
    def clear_frame(self):
        """Clear all widgets from the frame"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def on_closing(self):
        """Handle window closing"""
        self.go_back()
    
    def go_back(self):
        """Return to dashboard"""
        self.root.destroy()
        self.dashboard_root.deiconify()
    
    def show_student_management(self):
        """Display student management page"""
        self.clear_frame()

        # Main frame
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top navigation bar
        nav_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(
            nav_frame, text="← Back",
            font=('Arial', 11),
            bg='#34495e', fg='white',
            cursor='hand2',
            command=self.go_back
        )
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)

        title_label = tk.Label(
            nav_frame, text="Student Management",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50', fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20)

        user_label = tk.Label(
            nav_frame,
            text=f"Logged in: {self.user_data['first_name']} {self.user_data['last_name']}",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        user_label.pack(side=tk.RIGHT, padx=20)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#ecf0f1', padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Action row (buttons left, search right)
        action_frame = tk.Frame(content_frame, bg='#ecf0f1')
        action_frame.pack(fill=tk.X, pady=(5, 8), padx=10)

        # Buttons (LEFT)
        button_frame = tk.Frame(action_frame, bg='#ecf0f1')
        button_frame.pack(side=tk.LEFT)

        tk.Button(
            button_frame, text="Add Student",
            font=('Arial', 10, 'bold'),
            bg='#27ae60', fg='white',
            cursor='hand2', width=15,
            command=self.add_student_dialog
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="Edit Student",
            font=('Arial', 10, 'bold'),
            bg='#f39c12', fg='white',
            cursor='hand2', width=15,
            command=self.edit_student
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="Delete Student",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c', fg='white',
            cursor='hand2', width=15,
            command=self.delete_student
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="Refresh",
            font=('Arial', 10, 'bold'),
            bg='#3498db', fg='white',
            cursor='hand2', width=15,
            command=self.load_students
        ).pack(side=tk.LEFT, padx=5)

        # Search (RIGHT)
        search_frame = tk.Frame(action_frame, bg='#ecf0f1')
        search_frame.pack(side=tk.RIGHT)

        self.search_entry = ttk.Entry(search_frame, font=('Arial', 10), width=28)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            search_frame, text="Search",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            relief='flat',
            command=self.search_students
        ).pack(side=tk.LEFT)

        # Table frame (closer to buttons)
        table_frame = tk.Frame(content_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 8))

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Registration Date'),
            height=20,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=50)
        self.tree.column('First Name', anchor=tk.W, width=150)
        self.tree.column('Last Name', anchor=tk.W, width=150)
        self.tree.column('Email', anchor=tk.W, width=250)
        self.tree.column('Phone', anchor=tk.W, width=120)
        self.tree.column('Registration Date', anchor=tk.CENTER, width=130)

        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('First Name', text='First Name', anchor=tk.W)
        self.tree.heading('Last Name', text='Last Name', anchor=tk.W)
        self.tree.heading('Email', text='Email', anchor=tk.W)
        self.tree.heading('Phone', text='Phone', anchor=tk.W)
        self.tree.heading('Registration Date', text='Registration Date', anchor=tk.CENTER)

        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Status bar
        status_frame = tk.Frame(content_frame, bg='#ecf0f1')
        status_frame.pack(fill=tk.X, pady=5)

        self.status_label = tk.Label(
            status_frame, text="Ready",
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#7f8c8d',
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT)

        # Load students
        self.load_students()
    
    def load_students(self):
        """Load students from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = """
            SELECT student_id, first_name, last_name, email, phone, registration_date
            FROM students
            ORDER BY student_id
        """
        students = db.execute_query(query, fetch=True)  # ensure fetch=True

        if students:
            for idx, student in enumerate(students):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert(
                    '',
                    'end',
                    values=(
                        student['student_id'],
                        student['first_name'],
                        student['last_name'],
                        student['email'],
                        student['phone'] or 'N/A',
                        student['registration_date']
                    ),
                    tags=(tag,)
                )
            if hasattr(self, "status_label"):
                self.status_label.config(text=f"Loaded {len(students)} students")
        else:
            if hasattr(self, "status_label"):
                self.status_label.config(text="No students found in database")

    
    def search_students(self):
        """Search students by name or email"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_students()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        query = """
            SELECT student_id, first_name, last_name, email, phone, registration_date
            FROM students
            WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
            ORDER BY student_id
        """
        search_pattern = f"%{search_term}%"
        students = db.execute_query(query, (search_pattern, search_pattern, search_pattern))
        
        if students:
            for idx, student in enumerate(students):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert(
                    '',
                    tk.END,
                    values=(
                        student['student_id'],
                        student['first_name'],
                        student['last_name'],
                        student['email'],
                        student['phone'] or 'N/A',
                        student['registration_date']
                    ),
                    tags=(tag,)
                )
            self.status_label.config(text=f"Found {len(students)} students matching '{search_term}'")
        else:
            self.status_label.config(text=f"No students found matching '{search_term}'")
    
    def add_student_dialog(self):
        """Open dialog to add a new student"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.configure(bg='#ecf0f1')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#ecf0f1', padx=30, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # First Name
        tk.Label(form_frame, text="First Name:", bg='#ecf0f1', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        first_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        first_name_entry.grid(row=1, column=0, pady=(0, 10))
        
        # Last Name
        tk.Label(form_frame, text="Last Name:", bg='#ecf0f1', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        last_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        last_name_entry.grid(row=3, column=0, pady=(0, 10))
        
        # Email
        tk.Label(form_frame, text="Email:", bg='#ecf0f1', font=('Arial', 10)).grid(row=4, column=0, sticky='w', pady=5)
        email_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        email_entry.grid(row=5, column=0, pady=(0, 10))
        
        # Phone
        tk.Label(form_frame, text="Phone:", bg='#ecf0f1', font=('Arial', 10)).grid(row=6, column=0, sticky='w', pady=5)
        phone_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        phone_entry.grid(row=7, column=0, pady=(0, 20))
        
        def save_student():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            # ---- VALIDATION ----
            is_valid, error_message = validate_student_fields(first_name, last_name, email, phone)
            if not is_valid:
                messagebox.showerror("Validation Error", error_message)
                return
            
            query = """
                INSERT INTO students (first_name, last_name, email, phone, registration_date)
                VALUES (?, ?, ?, ?, ?)
            """
            values = (first_name, last_name, email, phone if phone else None, date.today().isoformat())
            
            if db.execute_query(query, values, fetch=False):
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to add student")
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.grid(row=8, column=0, pady=10)
        
        save_btn = tk.Button(btn_frame, text="Save", font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                             cursor='hand2', width=10, command=save_student)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", font=('Arial', 10), bg='#95a5a6', fg='white',
                               cursor='hand2', width=10, command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def edit_student(self):
        """ Edit selected student """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        # Get student data
        item = self.tree.item(selected[0])
        student_id, first_name, last_name, email, phone, reg_date = item["values"]
        
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Student (ID: {student_id})")
        dialog.geometry("400x390")
        dialog.resizable(False, False)
        dialog.configure(bg='#ecf0f1')

        dialog.transient(self.root)
        dialog.grab_set()

        # Form frame
        form_frame = tk.Frame(dialog, bg='#ecf0f1', padx=30, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        form_frame.grid_columnconfigure(0, weight=1)

        # Input fields
        tk.Label(form_frame, text="First Name:", bg='#ecf0f1', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        first_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        first_name_entry.insert(0, first_name)
        first_name_entry.grid(row=1, column=0, pady=(0, 10))

        tk.Label(form_frame, text="Last Name:", bg='#ecf0f1', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        last_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        last_name_entry.insert(0, last_name)
        last_name_entry.grid(row=3, column=0, pady=(0, 10))

        tk.Label(form_frame, text="Email:", bg='#ecf0f1', font=('Arial', 10)).grid(row=4, column=0, sticky='w', pady=5)
        email_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        email_entry.insert(0, email)
        email_entry.grid(row=5, column=0, pady=(0, 10))

        tk.Label(form_frame, text="Phone:", bg='#ecf0f1', font=('Arial', 10)).grid(row=6, column=0, sticky='w', pady=5)
        phone_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        if phone != "N/A":
            phone_entry.insert(0, phone)
        phone_entry.grid(row=7, column=0, pady=(0, 20))

        def update_student():
            updated_first = first_name_entry.get().strip()
            updated_last = last_name_entry.get().strip()
            updated_email = email_entry.get().strip()
            updated_phone = phone_entry.get().strip()

            if not all([updated_first, updated_last, updated_email]):
                messagebox.showwarning("Input Error", "Please fill in all required fields")
                return

            # Update record
            query = """
                UPDATE students
                SET first_name = ?, last_name = ?, email = ?, phone = ?
                WHERE student_id = ?
            """
            values = (updated_first, updated_last, updated_email, updated_phone if updated_phone else None, student_id)

            if db.execute_query(query, values, fetch=False):
                messagebox.showinfo("Success", "Student updated successfully!")
                dialog.destroy()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to update student")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.grid(row=8, column=0, pady=20, sticky="w")

        save_btn = tk.Button(btn_frame, text="Update", font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                             cursor='hand2', width=10, command=update_student)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(btn_frame, text="Cancel", font=('Arial', 10), bg='#95a5a6', fg='white',
                               cursor='hand2', width=10, command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def delete_student(self):
        """Delete selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
            
        # Get student data
        item = self.tree.item(selected[0])
        student_id = item['values'][0]
        student_name = f"{item['values'][1]} {item['values'][2]}"
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete student '{student_name}'?\n\nThis action cannot be undone."
        )
        
        if confirm:
            query = "DELETE FROM students WHERE student_id = ?"
            if db.execute_query(query, (student_id,), fetch=False):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to delete student")