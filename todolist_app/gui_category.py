import tkinter as tk
from app_logic import AppLogic

class GUICategory:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Thêm Category")
        self.root.geometry("250x250")

        self.create_widgets()

    def create_widgets(self):
        # Tạo một frame chứa tất cả các thành phần
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)


        # title label và entry
        title_frame = tk.Frame(main_frame)
        title_frame.pack()

        title_label = tk.Label(title_frame, text="Tên đăng nhập:")
        title_label.grid(row=0, column=0, sticky="w")  # Đặt sticky="w" để label nằm bên trái
        self.title_entry = tk.Entry(title_frame, width=50)
        self.title_entry.grid(row=1, column=0)

        # descrip label và entry
        descrip_frame = tk.Frame(main_frame)
        descrip_frame.pack()

        descrip_label = tk.Label(descrip_frame, text="Mật khẩu:")
        descrip_label.grid(row=0, column=0, sticky="w")  # Đặt sticky="w" để label nằm bên trái
        self.descrip_entry = tk.Entry(descrip_frame, show="*", width=50)
        self.descrip_entry.grid(row=1, column=0)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        # Nút đăng nhập
        add_button = tk.Button(button_frame, text="Thêm", command=self.add_category)
        add_button.grid(row=0, column=0, padx=5, pady=10)

        # Nút đóng
        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=0, column=1, padx=5, pady=10)


    def add_category(self):
        title = self.title_entry.get()  # Lấy title từ entry
        descrip = self.descrip_entry.get()  # Lấy descrip từ entry

        # Gọi phương thức login từ đối tượng AppLogic của chính đối tượng hiện tại
        app_logic_instance = AppLogic()

        # Gọi phương thức login từ thể hiện của lớp AppLogic
        app_logic_instance.add_category(self.db_manager, title, descrip)

        
    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()  # Hiển thị cửa sổ trước khi thực hiện các thay đổi
        # Hiển thị cửa sổ đăng nhập giữa màn hình
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()

if __name__ == "__main__":
    cate_gui = GUICategory()
    cate_gui.run()
