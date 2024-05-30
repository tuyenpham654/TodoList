import tkinter as tk
import re
from app_logic import Auth
from gui import App
from app_logic import AppLogic

from tkinter import messagebox
from tkcalendar import DateEntry

class GUILogin:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Đăng nhập")
        self.root.geometry("500x300")

        self.create_widgets()

    def create_widgets(self):
        # Tạo một frame chứa tất cả các thành phần
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        login_title_label = tk.Label(main_frame, text="Đăng Nhập", font=("Arial", 20))
        login_title_label.pack(pady=10)

        username_frame = tk.Frame(main_frame)
        username_frame.pack()
        username_label = tk.Label(username_frame, text="Tên đăng nhập:")
        username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(username_frame, width=50)
        self.username_entry.grid(row=1, column=0)

        password_frame = tk.Frame(main_frame)
        password_frame.pack()
        password_label = tk.Label(password_frame, text="Mật khẩu:")
        password_label.grid(row=0, column=0, sticky="w")
        self.password_entry = tk.Entry(password_frame, show="*", width=50)
        self.password_entry.grid(row=1, column=0)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()
        login_button = tk.Button(button_frame, text="Đăng nhập", command=self.login)
        login_button.grid(row=0, column=0, padx=5, pady=10)
        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=0, column=1, padx=5, pady=10)

        register_label = tk.Label(main_frame, text="Bạn chưa có tài khoản? Đăng ký ngay", fg="blue", cursor="hand2")
        register_label.pack()
        register_label.bind("<Button-1>", self.show_register)  # Gán sự kiện click cho label đăng ký

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        auth = Auth()
        login_success = auth.login(self.db_manager, username, password)

        if login_success:
            self.root.destroy()
            app = App(self.db_manager)
            app.run()
        else:
            messagebox.showinfo("Lỗi", "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu.")
            
    def show_register(self, event):
        # Hiển thị GUI đăng ký khi click vào label "Đăng ký"
        register_gui = GUIRegister(self.db_manager)
        register_gui.run()

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()  # Hiển thị cửa sổ trước khi thực hiện các thay đổi
        # Hiển thị cửa sổ đăng nhập giữa màn hình
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()

class GUIRegister:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Đăng ký")
        self.root.geometry("500x500")
        self.app_logic_instance = AppLogic()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        register_title_label = tk.Label(main_frame, text="Đăng Ký", font=("Arial", 20))
        register_title_label.pack(pady=10)

        full_name_frame = tk.Frame(main_frame)
        full_name_frame.pack()

        full_name_label = tk.Label(full_name_frame, text="Họ tên:")
        full_name_label.grid(row=0, column=0, sticky="w")
        self.full_name_entry = tk.Entry(full_name_frame, width=50)
        self.full_name_entry.grid(row=1, column=0)

        email_frame = tk.Frame(main_frame)
        email_frame.pack()

        email_label = tk.Label(email_frame, text="Email:")
        email_label.grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(email_frame, width=50)
        self.email_entry.grid(row=3, column=0)

        birthday_frame = tk.Frame(main_frame)
        birthday_frame.pack()

        self.birthday_label = tk.Label(birthday_frame, text="Ngày Sinh:")
        self.birthday_label.grid(row=4, column=0, sticky="w")

        self.birthday_entry = DateEntry(birthday_frame, width=50, background='darkblue', foreground='white', borderwidth=2)
        self.birthday_entry.grid(row=5, column=0)
        self.birthday_entry.config(selectmode='day', date_pattern='dd/MM/yyyy', width=14)

        username_frame = tk.Frame(main_frame)
        username_frame.pack()

        username_label = tk.Label(username_frame, text="Tên đăng nhập:")
        username_label.grid(row=8, column=0, sticky="w")
        self.username_entry = tk.Entry(username_frame, width=50)
        self.username_entry.grid(row=9, column=0)

        password_frame = tk.Frame(main_frame)
        password_frame.pack()

        password_label = tk.Label(password_frame, text="Mật khẩu:")
        password_label.grid(row=10, column=0, sticky="w")
        self.password_entry = tk.Entry(password_frame, show="*", width=50)
        self.password_entry.grid(row=11, column=0)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        register_button = tk.Button(button_frame, text="Đăng ký", command=self.register)
        register_button.grid(row=12, column=0, padx=5, pady=10)

        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=12, column=1, padx=5, pady=10)

    def register(self):
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        birthday = self.birthday_entry.get_date().strftime('%Y-%m-%d')
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.is_valid_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ.")
            return

        success, message = self.app_logic_instance.register(self.db_manager, username, password, email, full_name, birthday )

        if success:
            messagebox.showinfo("Thành công", message)
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", message)
    
    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()  
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()

if __name__ == "__main__":
    login_gui = GUILogin()
    login_gui.run()
