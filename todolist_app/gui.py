import tkinter as tk
from tkcalendar import Calendar
from app_logic import AppLogic
import datetime

class App:
    def __init__(self , db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("TodoList")
        self.root.geometry("1000x700")

        self.app_logic_instance = AppLogic()

        self.gui_login = None
        self.header_label = None
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, height=20, bg="lightgrey")
        header_frame.pack(side=tk.TOP, fill=tk.X, anchor="e")

        self.header_label = tk.Label(header_frame, text="Hi:", font=("Arial", 9), bg="lightgrey")
        self.header_label.pack(side=tk.LEFT, pady=10)

        login_button = tk.Button(header_frame, text="Đăng nhập/Đăng ký", command=self.show_login)
        login_button.pack(side=tk.RIGHT, padx=10, pady=5)

        sidebar_frame = tk.Frame(self.root, width=200, bg="white")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        separator_frame = tk.Frame(self.root, width=1, bg="black")
        separator_frame.pack(side=tk.LEFT, fill=tk.Y)

        today = datetime.date.today()
        cal = Calendar(sidebar_frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        cal.pack(pady=20)

        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_label = tk.Label(content_frame, text="Todo List", font=("Arial", 14), bg="white")
        content_label.pack(pady=10)

        user_tasks = self.app_logic_instance.get_user_tasks(self.db_manager)

        for task in user_tasks:
            task_frame = tk.Frame(content_frame, bg="lightblue", width=150, height=150, padx=10, pady=10)
            task_frame.pack(side=tk.LEFT, padx=10, pady=10)

            task_title = task[1]  # Assuming the second field is the task title
            task_description = task[2]  # Assuming the third field is the task description

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 12), bg="white")
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 10), bg="white")
            description_label.pack()

    def run(self):
        self.root.mainloop()
    
    def new_todo(self):
        # Thêm hành động khi nhấn nút "New" trong menu
        pass

    def show_login(self):
    #    if self.gui_login is None:
    #     self.gui_login = GUILogin(self.db_manager)
    #     self.gui_login.run()

        pass
    
    def current_user_name(self):
        user_name = self.app_logic_instance.get_user_name()
        if self.header_label is not None:
            self.header_label.config(text=f"Hi: {user_name}")


if __name__ == "__main__":
    app = App()
    app.run()
