import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app_logic import AppLogic

class GUIUser:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_id = None
        self.root = tk.Tk()
        self.root.title("Cập Nhật Thông Tin")
        self.root.geometry("500x500")
        self.app_logic_instance = AppLogic()
        self.user_updated = False
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        user_title_label = tk.Label(main_frame, text="Cập Nhật Thông Tin Người Dùng", font=("Arial", 20))
        user_title_label.pack(pady=10)

        email_frame = tk.Frame(main_frame)
        email_frame.pack()

        email_label = tk.Label(email_frame, text="Email:")
        email_label.grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(email_frame, width=50)
        self.email_entry.grid(row=1, column=0)

        full_name_frame = tk.Frame(main_frame)
        full_name_frame.pack()

        full_name_label = tk.Label(full_name_frame, text="Họ và Tên:")
        full_name_label.grid(row=2, column=0, sticky="w")
        self.full_name_entry = tk.Entry(full_name_frame, width=50)
        self.full_name_entry.grid(row=3, column=0)

        birthday_frame = tk.Frame(main_frame)
        birthday_frame.pack()

        self.birthday_label = tk.Label(birthday_frame, text="Ngày Sinh:")
        self.birthday_label.grid(row=4, column=0, sticky="w")

        self.birthday_entry = DateEntry(birthday_frame, width=50, background='darkblue', foreground='white', borderwidth=2)
        self.birthday_entry.grid(row=5, column=0)
        self.birthday_entry.config(selectmode='day', date_pattern='dd/MM/yyyy', width=14)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        self.update_user_button = tk.Button(button_frame, text="Cập Nhật Thông Tin", command=self.update_user)
        self.update_user_button.grid(row=6, column=0, padx=5, pady=10)

        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=6, column=1, padx=5, pady=10)

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.update_user_button.config(command=self.update_user)
        user_data = self.app_logic_instance.get_user_by_id(self.db_manager, user_id)
        if user_data:
            self.email_entry.insert(0, user_data['email'])
            self.full_name_entry.insert(0, user_data['full_name'])
            if user_data['birthday']:  # Kiểm tra nếu ngày sinh không phải là None
                self.birthday_entry.set_date(user_data['birthday'])

    def update_user(self):
        email = self.email_entry.get()
        full_name = self.full_name_entry.get()
        birthday = self.birthday_entry.get_date().strftime('%Y-%m-%d')

        # Kiểm tra xem tất cả các trường thông tin đã được nhập đúng chưa
        if not full_name:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        # Thực hiện cập nhật người dùng
        if self.app_logic_instance.update_user(self.db_manager, self.user_id, email, full_name, birthday):
            messagebox.showinfo("Thành công", "Thông tin người dùng đã được cập nhật thành công.")
            self.root.destroy()  # Đóng cửa sổ sau khi cập nhật thành công
        else:
            messagebox.showerror("Lỗi", "Cập nhật thông tin người dùng thất bại.")

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()  
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()
        
class ChangePassword:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_id = None
        self.root = tk.Tk()
        self.root.title("Thay Đổi Mật Khẩu")
        self.root.geometry("500x400")
        self.app_logic_instance = AppLogic()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        title_label = tk.Label(main_frame, text="Thay Đổi Mật Khẩu", font=("Arial", 20))
        title_label.pack(pady=10)

        old_password_frame = tk.Frame(main_frame)
        old_password_frame.pack()

        old_password_label = tk.Label(old_password_frame, text="Mật Khẩu Cũ:")
        old_password_label.grid(row=0, column=0, sticky="w")
        self.old_password_entry = tk.Entry(old_password_frame, show="*", width=50)
        self.old_password_entry.grid(row=1, column=0)

        new_password_frame = tk.Frame(main_frame)
        new_password_frame.pack()

        new_password_label = tk.Label(new_password_frame, text="Mật Khẩu Mới:")
        new_password_label.grid(row=2, column=0, sticky="w")
        self.new_password_entry = tk.Entry(new_password_frame, show="*", width=50)
        self.new_password_entry.grid(row=3, column=0)

        confirm_password_frame = tk.Frame(main_frame)
        confirm_password_frame.pack()

        confirm_password_label = tk.Label(confirm_password_frame, text="Xác Nhận Mật Khẩu Mới:")
        confirm_password_label.grid(row=4, column=0, sticky="w")
        self.confirm_password_entry = tk.Entry(confirm_password_frame, show="*", width=50)
        self.confirm_password_entry.grid(row=5, column=0)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        change_password_button = tk.Button(button_frame, text="Thay Đổi Mật Khẩu", command=self.change_password)
        change_password_button.grid(row=6, column=0, padx=5, pady=10)

        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=6, column=1, padx=5, pady=10)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Kiểm tra xem mật khẩu cũ và mật khẩu mới có khớp nhau không
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp.")
            return
        # Thực hiện thay đổi mật khẩu
        if self.app_logic_instance.change_password(self.db_manager, self.user_id, old_password, new_password):
            messagebox.showinfo("Thành công", "Mật khẩu đã được thay đổi thành công.")
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", "Thay đổi mật khẩu thất bại.")

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()  
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()


if __name__ == "__main__":
    user_gui = GUIUser()
    user_gui.run()
