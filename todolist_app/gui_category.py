import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app_logic import AppLogic

class GUICategory:
    def __init__(self, db_manager,on_close_callback):
        self.db_manager = db_manager
        self.category_id = None
        self.on_close_callback = on_close_callback
        self.root = tk.Tk()
        self.root.title("Thêm Danh Mục")
        self.root.geometry("500x500")
        self.app_logic_instance = AppLogic()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        task_title_label = tk.Label(main_frame, text="Thêm Category", font=("Arial", 20))
        task_title_label.pack(pady=10)

        name_frame = tk.Frame(main_frame)
        name_frame.pack()

        name_label = tk.Label(name_frame, text="Tên Loại:")
        name_label.grid(row=2, column=0, sticky="w")
        self.name_entry = tk.Entry(name_frame, width=50)
        self.name_entry.grid(row=3, column=0)

        categories_frame = tk.Frame(main_frame)
        categories_frame.pack()

        description_frame = tk.Frame(main_frame)
        description_frame.pack()

        description_label = tk.Label(description_frame, text="Mô tả:")
        description_label.grid(row=6, column=0, sticky="w")
        self.description_entry = tk.Entry(description_frame, width=50)
        self.description_entry.grid(row=7, column=0)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        self.add_category_button = tk.Button(button_frame, text="Thêm Loại", command=self.add_category)
        self.add_category_button.grid(row=8, column=0, padx=5, pady=10)

        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=8, column=1, padx=5, pady=10)

    def add_category(self):
        name = self.name_entry.get()
        description = self.description_entry.get()

        if self.app_logic_instance.add_category(self.db_manager, name, description):
            messagebox.showinfo("Thành công", "Nhiệm vụ đã được thêm thành công")
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", "Thêm nhiệm vụ thất bại")

    def set_category_id(self, category_id):
        self.category_id = category_id
        self.is_update_mode = True
        self.add_category_button.config(text="Cập nhật Nhiệm Vụ", command=lambda: self.update_category(self.category_id))
        category_data = self.app_logic_instance.get_category_by_id(self.db_manager, category_id)
        if category_data:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, category_data[1])

            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, category_data[2])

    
    def update_category(self, category_id):
        name = self.name_entry.get()
        description = self.description_entry.get()
        
        # Tìm category_id tương ứng trong từ điển categories_dict
        
        if category_id and self.app_logic_instance.update_category(self.db_manager, category_id, name, description):
            messagebox.showinfo("Thành công", "Nhiệm vụ đã được cập nhật thành công")
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", "Cập nhật nhiệm vụ thất bại")
    
    def destroy_add_category_button(self):
        if self.category_updated:
            self.add_category_button.destroy()

    def close_window(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có muốn đóng cửa sổ này?"):
            self.root.destroy()
            if self.on_close_callback:
                self.on_close_callback()

    def on_close(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có muốn đóng cửa sổ này?"):
            self.root.destroy()
            if self.on_close_callback:
                self.on_close_callback()

    def run(self):
        self.root.update_idletasks()  # Hiển thị cửa sổ trước khi thực hiện các thay đổi
        # Hiển thị cửa sổ đăng nhập giữa màn hình
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        # self.root.mainloop()


if __name__ == "__main__":
    cate_gui = GUICategory()
    cate_gui.run()
