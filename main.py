from Core.database import setup_database, db
from Modules.log_in import LoginWindow
import tkinter as tk

def main():
    setup_database()  # only ensures tables exist, does not reset data
    root = tk.Tk()
    app = LoginWindow(root)

    def on_closing():
        db.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    db.close()

if __name__ == "__main__":
    main()