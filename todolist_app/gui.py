import subprocess
import os
import tkinter as tk
from tkcalendar import Calendar
from app_logic import AppLogic
from gui_task import GUITask
from gui_category import GUICategory
from gui_user import GUIUser, ChangePassword
from app_logic import Auth
import datetime
import tkinter.messagebox as messagebox

class App:
    def __init__(self , db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("TodoList")
        self.root.state("zoomed")

        self.app_logic_instance = AppLogic()

        self.gui_login = None
        self.gui_task = None
        self.gui_user = None
        self.gui_category=None
        self.header_label = None
        self.create_widgets()
        self.current_user_name()

    def complete_task(self, parent, id):
        if self.app_logic_instance.completed_task(self.db_manager, id):
            # Hiển thị thông báo khi nhiệm vụ được hoàn thành thành công
            messagebox.showinfo("Thông báo", "Nhiệm vụ đã được đánh dấu là hoàn thành.")
        else:
            # Hiển thị thông báo khi xảy ra lỗi trong quá trình đánh dấu hoàn thành nhiệm vụ
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi đánh dấu hoàn thành nhiệm vụ.")

    def update_task(self, parent, id):
        if self.gui_task is None:
            self.gui_task = GUITask(self.db_manager)
            self.gui_task.set_task_id(id)
            self.gui_task.run()


    def delete_task(self, parent, id):
        confirm = messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn xoá nhiệm vụ này?")
        if confirm:
            if self.app_logic_instance.destroy_task(self.db_manager, id):
                # Hiển thị thông báo khi nhiệm vụ được xóa thành công
                messagebox.showinfo("Thông báo", "Nhiệm vụ đã được xóa thành công.")
            else:
                # Hiển thị thông báo khi xảy ra lỗi trong quá trình xóa nhiệm vụ
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi xóa nhiệm vụ.")

    def create_widgets(self):
        header_frame = tk.Frame(self.root, height=20, bg="lightgrey")
        header_frame.pack(side=tk.TOP, fill=tk.X, anchor="e")

        self.header_label = tk.Label(header_frame, text="Hi:", font=("Arial", 9), bg="lightgrey")
        self.header_label.pack(side=tk.LEFT, pady=10)

        option_button = tk.Menubutton(header_frame, text="Tuỳ chọn", relief="raised")
        option_button.pack(side=tk.RIGHT, padx=10, pady=5)
        user = Auth.get_current_user()
        option_menu = tk.Menu(option_button, tearoff=False)
        option_button.configure(menu=option_menu)
        option_menu.add_command(label="Thay đổi mật khẩu", compound=tk.LEFT, command=lambda id=user[0]: self.show_change_pass_gui(id))
        option_menu.add_command(label="Cập nhật thông tin", compound=tk.LEFT, command=lambda id=user[0]: self.show_user_gui(id))
        option_menu.add_command(label="Đăng xuất", compound=tk.LEFT, command=self.logout)
        option_menu.add_command(label="Thoát", compound=tk.LEFT, command=self.exit)

        task_button = tk.Menubutton(header_frame, text="Nhiệm vụ", relief="raised")
        task_button.pack(side=tk.RIGHT, padx=10, pady=5)
        task_menu = tk.Menu(task_button, tearoff=False)
        task_button.configure(menu=task_menu)
        task_menu.add_command(label="Thêm nhiệm vụ", compound=tk.LEFT, command=self.show_task_gui)
        task_menu.add_command(label="Làm mới nhiệm vụ", compound=tk.LEFT, command=self.refresh_tasks)

        category_button = tk.Menubutton(header_frame, text="Danh mục", relief="raised")
        category_button.pack(side=tk.RIGHT, padx=10, pady=5)
        category_menu = tk.Menu(category_button, tearoff=False)
        category_button.configure(menu=category_menu)
        category_menu.add_command(label="Thêm danh mục", compound=tk.LEFT, command=self.show_category_gui)
        category_menu.add_command(label="Làm mới danh mục", compound=tk.LEFT, command=self.refresh_tasks)


        self.sidebar_frame = tk.Frame(self.root, width=200, bg="white")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        separator_frame = tk.Frame(self.root, width=1, bg="black")
        separator_frame.pack(side=tk.LEFT, fill=tk.Y)

        today = datetime.date.today()
        # Widgets trong phần Sidebar
        doing_label = tk.Label(self.sidebar_frame, text="Category", font=("Arial", 14), bg="white")
        doing_label.pack(padx=10, pady=10, anchor="nw")
        user_tasks = self.app_logic_instance.get_user_tasks(self.db_manager)
        for task in user_tasks:
            task_frame = tk.Frame(self.sidebar_frame, width=300, height=150, padx=10, pady=10, borderwidth=1, relief="solid")
            task_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

            task_title = task[3]  # Assuming the second field is the task title
            task_description = task[4]  # Assuming the third field is the task description

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 16), width=10)
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 12), width=10, height=5)
            description_label.pack()

            # Tạo một Frame để chứa các button và sử dụng grid để căn giữa và đồng bộ width
            button_frame = tk.Frame(task_frame)
            button_frame.pack(side=tk.BOTTOM, padx=5, pady=5, anchor="w")

            complete_button = tk.Button(button_frame, text="Hoàn thành", command=lambda id=task[0]: self.complete_task(task_frame, id), foreground="green", width=10)
            complete_button.grid(row=0, column=0, padx=5, pady=5)

            update_button = tk.Button(button_frame, text="Cập nhật", command=lambda id=task[0]: self.update_task(task_frame, id), foreground="black", width=10)
            update_button.grid(row=1, column=0, padx=5, pady=5)

            delete_button = tk.Button(button_frame, text="Xoá", command=lambda id=task[0]: self.delete_task(task_frame, id), foreground="red", width=10)
            delete_button.grid(row=2, column=0, padx=5, pady=5)

        # cal = Calendar(sidebar_frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        # cal.pack(pady=20)

        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_label = tk.Label(self.content_frame, text="Todo List", font=("Arial", 14), bg="white")
        content_label.pack(pady=10)

        add_task_button = tk.Button(self.content_frame, text="+ Thêm nhiệm vụ", command=self.show_task_gui)
        add_task_button.place(relx=1.0, rely=0.0, anchor="ne", x=-70, y=10)

        refresh_button = tk.Button(self.content_frame, text="Làm mới", command=self.refresh_tasks)
        refresh_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10) 

        self.content_frame_top = tk.Frame(self.content_frame, bg="white")
        self.content_frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.content_frame_bottom = tk.Frame(self.content_frame, bg="white")
        self.content_frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Widgets trong phần trên (Đang làm)
        doing_label = tk.Label(self.content_frame_top, text="Đang làm", font=("Arial", 14), bg="white")
        doing_label.pack(padx=10, pady=10, anchor="nw")
        user_tasks = self.app_logic_instance.get_user_tasks(self.db_manager)
        for task in user_tasks:
            task_frame = tk.Frame(self.content_frame_top, width=300, height=150, padx=10, pady=10, borderwidth=1, relief="solid")
            task_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

            task_title = task[3]  # Assuming the second field is the task title
            task_description = task[4]  # Assuming the third field is the task description

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 16), width=10)
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 12), width=10, height=5)
            description_label.pack()

            # Tạo một Frame để chứa các button và sử dụng grid để căn giữa và đồng bộ width
            button_frame = tk.Frame(task_frame)
            button_frame.pack(side=tk.BOTTOM, padx=5, pady=5, anchor="w")

            complete_button = tk.Button(button_frame, text="Hoàn thành", command=lambda id=task[0]: self.complete_task(task_frame, id), foreground="green", width=10)
            complete_button.grid(row=0, column=0, padx=5, pady=5)

            update_button = tk.Button(button_frame, text="Cập nhật", command=lambda id=task[0]: self.update_task(task_frame, id), foreground="black", width=10)
            update_button.grid(row=1, column=0, padx=5, pady=5)

            delete_button = tk.Button(button_frame, text="Xoá", command=lambda id=task[0]: self.delete_task(task_frame, id), foreground="red", width=10)
            delete_button.grid(row=2, column=0, padx=5, pady=5)

        # Widgets trong phần dưới (Hoàn thành)
        completed_label = tk.Label(self.content_frame_bottom, text="Khác", font=("Arial", 14), bg="white")
        completed_label.pack(padx=10, pady=10, anchor="nw")
        user_tasks = self.app_logic_instance.get_user_tasks_other(self.db_manager)
        for task in user_tasks:
            task_frame = tk.Frame(self.content_frame_bottom, width=300, height=150, padx=10, pady=10, borderwidth=1, relief="solid")
            task_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")
            task_title = task[3] 
            task_description = task[4]
            task_status = task[9]

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 16), width=10)
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 12), width=10, height=5)
            description_label.pack()

            status_text = ""
            status_color = ""
            if task_status == 2:
                status_text = "Hoàn thành"
                status_color = "green"
            elif task_status == 0:
                status_text = "Đã hủy"
                status_color = "red"

            status_label = tk.Label(task_frame, text=status_text, font=("Arial", 12), foreground=status_color)
            status_label.pack()
    
    def refresh_tasks(self):
    # Xóa nhiệm vụ hiện có trên giao diện
        for widget in self.content_frame_top.winfo_children():
            widget.destroy()

        for widget in self.content_frame_bottom.winfo_children():
            widget.destroy()

        self.show_current_tasks()
        self.show_other_tasks()

    def show_current_tasks(self):
        doing_label = tk.Label(self.content_frame_top, text="Đang làm", font=("Arial", 14), bg="white")
        doing_label.pack(padx=10, pady=10, anchor="nw")
        user_tasks = self.app_logic_instance.get_user_tasks(self.db_manager)
        for task in user_tasks:
            task_frame = tk.Frame(self.content_frame_top, width=300, height=150, padx=10, pady=10, borderwidth=1, relief="solid")
            task_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

            task_title = task[3]  # Assuming the second field is the task title
            task_description = task[4]  # Assuming the third field is the task description

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 16), width=10)
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 12), width=10, height=5)
            description_label.pack()

             # Tạo một Frame để chứa các button và sử dụng grid để căn giữa và đồng bộ width
            button_frame = tk.Frame(task_frame)
            button_frame.pack(side=tk.BOTTOM, padx=5, pady=5, anchor="w")

            complete_button = tk.Button(button_frame, text="Hoàn thành", command=lambda id=task[0]: self.complete_task(task_frame, id), foreground="green", width=10)
            complete_button.grid(row=0, column=0, padx=5, pady=5)

            update_button = tk.Button(button_frame, text="Cập nhật", command=lambda id=task[0]: self.update_task(task_frame, id), foreground="black", width=10)
            update_button.grid(row=1, column=0, padx=5, pady=5)

            delete_button = tk.Button(button_frame, text="Xoá", command=lambda id=task[0]: self.delete_task(task_frame, id), foreground="red", width=10)
            delete_button.grid(row=2, column=0, padx=5, pady=5)

    def show_other_tasks(self):
        completed_label = tk.Label(self.content_frame_bottom, text="Khác", font=("Arial", 14), bg="white")
        completed_label.pack(padx=10, pady=10, anchor="nw")
        user_tasks = self.app_logic_instance.get_user_tasks_other(self.db_manager)
        for task in user_tasks:
            task_frame = tk.Frame(self.content_frame_bottom, width=300, height=150, padx=10, pady=10, borderwidth=1, relief="solid")
            task_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")
            task_title = task[3] 
            task_description = task[4]
            task_status = task[9]

            title_label = tk.Label(task_frame, text=task_title, font=("Arial", 16), width=10)
            title_label.pack()

            description_label = tk.Label(task_frame, text=task_description, font=("Arial", 12), width=10, height=5)
            description_label.pack()

            status_text = ""
            status_color = ""
            if task_status == 2:
                status_text = "Hoàn thành"
                status_color = "green"
            elif task_status == 0:
                status_text = "Đã hủy"
                status_color = "red"

            status_label = tk.Label(task_frame, text=status_text, font=("Arial", 12), foreground=status_color)
            status_label.pack()

    def run(self):
        self.root.mainloop()

    def exit(self):
        confirm = messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn thoát ứng dụng?")
        if confirm:
            self.root.destroy()

    def logout(self):
        self.root.destroy()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        main_py_path = os.path.join(script_dir, "main.py")
        if os.path.exists(main_py_path):
            subprocess.call(["python", main_py_path])
        else:
            print("Không tìm thấy tập lệnh main.py")

    def show_task_gui(self):
        if self.gui_task is None:
            self.gui_task = GUITask(self.db_manager)
            self.gui_task.run()

    def show_category_gui(self):
        if self.gui_category is None:
            self.gui_category = GUICategory(self.db_manager)
            self.gui_category.run()

    def show_user_gui(self, id):
        if self.gui_user is None:
            self.gui_user = GUIUser(self.db_manager)
            self.gui_user.set_user_id(id)
            self.gui_user.run()

    def show_change_pass_gui(self, id):
        if self.gui_user is None:
            self.gui_change_pass = ChangePassword(self.db_manager)
            self.gui_change_pass.set_user_id(id)
            self.gui_change_pass.run()

    def current_user_name(self):
        user_name = self.app_logic_instance.get_user_name()
        if self.header_label is not None:
            self.header_label.config(text=f"Hi: {user_name}")


if __name__ == "__main__":
    app = App()
    app.run()
