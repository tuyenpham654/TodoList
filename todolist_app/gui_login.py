import tkinter as tk
from app_logic import AppLogic

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

         # Tạo tiêu đề
        login_title_label = tk.Label(main_frame, text="Đăng Nhập", font=("Arial", 20))
        login_title_label.pack(pady=10)


        # Username label và entry
        username_frame = tk.Frame(main_frame)
        username_frame.pack()

        username_label = tk.Label(username_frame, text="Tên đăng nhập:")
        username_label.grid(row=0, column=0, sticky="w")  # Đặt sticky="w" để label nằm bên trái
        self.username_entry = tk.Entry(username_frame, width=50)
        self.username_entry.grid(row=1, column=0)

        # Password label và entry
        password_frame = tk.Frame(main_frame)
        password_frame.pack()

        password_label = tk.Label(password_frame, text="Mật khẩu:")
        password_label.grid(row=0, column=0, sticky="w")  # Đặt sticky="w" để label nằm bên trái
        self.password_entry = tk.Entry(password_frame, show="*", width=50)
        self.password_entry.grid(row=1, column=0)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        # Nút đăng nhập
        login_button = tk.Button(button_frame, text="Đăng nhập", command=self.login)
        login_button.grid(row=0, column=0, padx=5, pady=10)

        # Nút đóng
        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=0, column=1, padx=5, pady=10)

        # Dòng "Bạn chưa có tài khoản. Đăng ký ngay"
        register_label = tk.Label(main_frame, text="Bạn chưa có tài khoản? Đăng ký ngay", fg="blue", cursor="hand2")
        register_label.pack()
        register_label.bind("<Button-1>", self.show_register)  # Gán sự kiện click cho label đăng ký

    def login(self):
        username = self.username_entry.get()  # Lấy username từ entry
        password = self.password_entry.get()  # Lấy password từ entry

        # Gọi phương thức login từ đối tượng AppLogic của chính đối tượng hiện tại
        app_logic_instance = AppLogic()

        # Gọi phương thức login từ thể hiện của lớp AppLogic
        app_logic_instance.login(self.db_manager, username, password)


    def show_register(self, event):
        # Hiển thị GUI đăng ký khi click vào label "Đăng ký"
        register_gui = GUIRegister()
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
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đăng ký")
        self.root.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):
        # Tạo một frame chứa tất cả các thành phần
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        # Tạo tiêu đề
        register_title_label = tk.Label(main_frame, text="Đăng Ký", font=("Arial", 20))
        register_title_label.pack(pady=10)

        # Họ tên label và entry
        full_name_frame = tk.Frame(main_frame)
        full_name_frame.pack()

        full_name_label = tk.Label(full_name_frame, text="Họ tên:")
        full_name_label.grid(row=0, column=0, sticky="w")
        self.full_name_entry = tk.Entry(full_name_frame, width=50)
        self.full_name_entry.grid(row=1, column=0)

        # Email label và entry
        email_frame = tk.Frame(main_frame)
        email_frame.pack()

        email_label = tk.Label(email_frame, text="Email:")
        email_label.grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(email_frame, width=50)
        self.email_entry.grid(row=3, column=0)

        # Ngày sinh label và entry
        dob_frame = tk.Frame(main_frame)
        dob_frame.pack()

        dob_label = tk.Label(dob_frame, text="Ngày sinh:")
        dob_label.grid(row=4, column=0, sticky="w")
        self.dob_entry = tk.Entry(dob_frame, width=50)
        self.dob_entry.grid(row=5, column=0)

        # Địa chỉ label và entry
        address_frame = tk.Frame(main_frame)
        address_frame.pack()

        address_label = tk.Label(address_frame, text="Địa chỉ:")
        address_label.grid(row=6, column=0, sticky="w")
        self.address_entry = tk.Entry(address_frame, width=50)
        self.address_entry.grid(row=7, column=0)

        # Username label và entry
        username_frame = tk.Frame(main_frame)
        username_frame.pack()

        username_label = tk.Label(username_frame, text="Tên đăng nhập:")
        username_label.grid(row=8, column=0, sticky="w")
        self.username_entry = tk.Entry(username_frame, width=50)
        self.username_entry.grid(row=9, column=0)

        # Password label và entry
        password_frame = tk.Frame(main_frame)
        password_frame.pack()

        password_label = tk.Label(password_frame, text="Mật khẩu:")
        password_label.grid(row=10, column=0, sticky="w")
        self.password_entry = tk.Entry(password_frame, show="*", width=50)
        self.password_entry.grid(row=11, column=0)

       # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        # Nút đăng ký
        register_button = tk.Button(button_frame, text="Đăng ký", command=self.register)
        register_button.grid(row=12, column=0, padx=5, pady=10)

        # Nút đóng
        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=12, column=1, padx=5, pady=10)

    def register(self):
        # Lấy thông tin từ các entry widgets
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Thực hiện xử lý đăng ký
        # Ví dụ: Kiểm tra thông tin và lưu vào cơ sở dữ liệu
        print("Thông tin đăng ký:")
        print("Họ tên:", full_name)
        print("Email:", email)
        print("Ngày sinh:", dob)
        print("Địa chỉ:", address)
        print("Tên đăng nhập:", username)
        print("Mật khẩu:", password)

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    login_gui = GUILogin()
    login_gui.run()
