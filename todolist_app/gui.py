import tkinter as tk
from tkcalendar import Calendar
import datetime

from gui_login import GUILogin

class App:
    def __init__(self , db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("TodoList")
        self.root.geometry("1000x700")

        self.gui_login = None
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, height=20, bg="lightgrey")
        header_frame.pack(side=tk.TOP, fill=tk.X, anchor="e")
        
        # Header label
        header_label = tk.Label(header_frame, text="Hi: ...", font=("Arial", 9), bg="lightgrey")
        header_label.pack(side=tk.LEFT ,pady=10)

        # Đăng nhập/Đăng ký button
        login_button = tk.Button(header_frame, text="Đăng nhập/Đăng ký", command=self.show_login)
        login_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Sidebar
        sidebar_frame = tk.Frame(self.root, width=200, bg="white")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Vertical separator line for sidebar
        separator_frame = tk.Frame(self.root, width=1, bg="black")
        separator_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Calendar in Sidebar
        today = datetime.date.today()
        cal = Calendar(sidebar_frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        cal.pack(pady=20)

        # Content
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_label = tk.Label(content_frame, text="Todo List", font=("Arial", 14), bg="white")
        content_label.pack(pady=10)

        # Display days of the month
        days_frame = tk.Frame(content_frame, bg="white")
        days_frame.pack(pady=20)

        # Get current month days
        self.display_month_days(days_frame, today.year, today.month)

    def display_month_days(self, parent, year, month):
        for widget in parent.winfo_children():
            widget.destroy()

        days_in_month = self.days_in_month(year, month)
        first_day_of_month = datetime.date(year, month, 1).weekday()

        for i in range(first_day_of_month):
            tk.Label(parent, text=" ", font=("Arial", 12), bg="white", width=5).grid(row=0, column=i)

        for day in range(1, days_in_month + 1):
            tk.Label(parent, text=str(day), font=("Arial", 12), bg="white", width=5).grid(row=(first_day_of_month + day - 1) // 7, column=(first_day_of_month + day - 1) % 7)

    def days_in_month(self, year, month):
        next_month = month % 12 + 1
        next_month_year = year + (month // 12)
        return (datetime.date(next_month_year, next_month, 1) - datetime.date(year, month, 1)).days

    def run(self):
        self.root.mainloop()
    
    def new_todo(self):
        # Thêm hành động khi nhấn nút "New" trong menu
        pass

    def show_login(self):
       if self.gui_login is None:
        self.gui_login = GUILogin(self.db_manager)
        self.gui_login.run()
        pass

if __name__ == "__main__":
    app = App()
    app.run()
