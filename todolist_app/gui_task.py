import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from app_logic import AppLogic



class GUITask:
    def __init__(self, db_manager, on_close_callback, refresh_callback):
        self.db_manager = db_manager
        self.task_id = None
        self.root = tk.Tk()
        self.root.title("Thêm Nhiệm Vụ")
        self.root.geometry("500x500")
        self.app_logic_instance = AppLogic()
        self.categories_dict = {}
        self.current_month = datetime.today().month
        self.use_due_date = tk.BooleanVar(value=False)  
        self.create_widgets()
        self.on_close_callback = on_close_callback
        self.refresh_callback = refresh_callback
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        
    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", pady=50)

        task_title_label = tk.Label(main_frame, text="Thêm Nhiệm Vụ", font=("Arial", 20))
        task_title_label.pack(pady=10)

        title_frame = tk.Frame(main_frame)
        title_frame.pack()

        title_label = tk.Label(title_frame, text="Tiêu Đề:")
        title_label.grid(row=2, column=0, sticky="w")
        self.title_entry = tk.Entry(title_frame, width=50)
        self.title_entry.grid(row=3, column=0)

        categories_frame = tk.Frame(main_frame)
        categories_frame.pack()

        category_label = tk.Label(categories_frame, text="Danh mục:")
        category_label.grid(row=4, column=0, sticky="w")

        categories = self.app_logic_instance.list_categories(self.db_manager)
        self.categories_dict = {category[0]: category[1] for category in categories}
        categories_values = ['Không'] + list(self.categories_dict.values())

        self.category_combobox = ttk.Combobox(categories_frame, values=categories_values, state="readonly")
        self.category_combobox.current(0)
        self.category_combobox.grid(row=5, column=0)

        description_frame = tk.Frame(main_frame)
        description_frame.pack()

        description_label = tk.Label(description_frame, text="Mô Tả:")
        description_label.grid(row=6, column=0, sticky="w")
        self.description_entry = tk.Entry(description_frame, width=50)
        self.description_entry.grid(row=7, column=0)

        start_date_frame = tk.Frame(main_frame)
        start_date_frame.pack()

        start_date_label = tk.Label(start_date_frame, text="Ngày bắt đầu:")
        start_date_label.grid(row=8, column=0, sticky="w")
        self.start_date_entry = DateEntry(start_date_frame, width=50, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.grid(row=9, column=0)
        self.start_date_entry.config(selectmode='day', date_pattern='dd/MM/yyyy', width=14) 
        self.start_date_entry.set_date(datetime.now())

        repeat_frame = tk.Frame(main_frame)
        repeat_frame.pack()

        repeat_label = tk.Label(repeat_frame, text="Lặp Lại:")
        repeat_label.grid(row=10, column=0, sticky="w")
        
        self.repeat_combobox = ttk.Combobox(repeat_frame, values=["Không", "Hàng Ngày", "Hàng Tuần", "Hàng Tháng"], state="readonly")
        self.repeat_combobox.current(0)
        self.repeat_combobox.grid(row=11, column=0, pady=5)

        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        self.add_task_button = tk.Button(button_frame, text="Thêm Nhiệm Vụ", command=self.add_task)
        self.add_task_button.grid(row=12, column=0, padx=5, pady=10)

        close_button = tk.Button(button_frame, text="Đóng", command=self.close_window)
        close_button.grid(row=12, column=1, padx=5, pady=10)
    
    def toggle_date_entry(self):
        if self.use_due_date.get():
            self.due_date_entry.config(state="normal")
        else:
            self.due_date_entry.config(state="disabled")

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        selected_category = self.category_combobox.get()
        repeat = self.repeat_combobox.get()

        # Tìm category_id tương ứng trong từ điển categories_dict
        category_id = None
        for key, value in self.categories_dict.items():
            if value == selected_category:
                category_id = key
                break

        start_date_str = self.start_date_entry.get_date().strftime('%d/%m/%Y')

        repeat_mapping = {
            "Không": "none",
            "Hàng Ngày": "daily",
            "Hàng Tuần": "weekly",
            "Hàng Tháng": "monthly"
        }
        repeat_value = repeat_mapping.get(repeat, "none")

        if self.app_logic_instance.add_task(self.db_manager, title, category_id, description, start_date_str, repeat_value):
            messagebox.showinfo("Thành công", "Nhiệm vụ đã được thêm thành công")
            self.on_close()
        else:
            messagebox.showerror("Lỗi", "Thêm nhiệm vụ thất bại")
            
            self.refresh_callback(self.current_month)

    def set_task_id(self, task_id):
        self.task_id = task_id
        self.is_update_mode = True
        self.add_task_button.config(text="Cập nhật Nhiệm Vụ", command=lambda: self.update_task(self.task_id))
        task_data = self.app_logic_instance.get_task_by_id(self.db_manager, task_id)
        if task_data:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, task_data[3])

            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, task_data[4])
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.set_date(task_data[5])
            category_id = task_data[2]
            category_name = self.categories_dict.get(category_id)
            if category_name:
                self.category_combobox.set(category_name)
            repeat_id = task_data[7]
            repeat_mapping = {
                "none":"Không" ,
                "daily":"Hàng Ngày",
                "weekly":"Hàng Tuần",
                "monthly":"Hàng Tháng"
            }
            repeat_value = repeat_mapping.get(repeat_id)
            if repeat_value:
                self.repeat_combobox.set(repeat_value)
    
    def update_task(self, task_id):
        title = self.title_entry.get()
        description = self.description_entry.get()
        start_date = self.start_date_entry.get_date().strftime('%d/%m/%Y')
        selected_category = self.category_combobox.get()
        selected_repeat = self.repeat_combobox.get()

        category_id = None
        for key, value in self.categories_dict.items():
            if value == selected_category:
                category_id = key
                break

        repeat_mapping = {
            "Không": "none",
            "Hàng Ngày": "daily",
            "Hàng Tuần": "weekly",
            "Hàng Tháng": "monthly"
        }
        repeat_id = repeat_mapping.get(selected_repeat)
        
        
        if task_id and self.app_logic_instance.update_task(self.db_manager, task_id, title, category_id, description, start_date, repeat_id):
            messagebox.showinfo("Thành công", "Nhiệm vụ đã được cập nhật thành công")
            self.on_close()
        else:
            messagebox.showerror("Lỗi", "Cập nhật nhiệm vụ thất bại")
            self.refresh_callback() 

    
    def destroy_add_task_button(self):
        if self.task_updated:
            self.add_task_button.destroy()
        self.refresh_callback()

    def close_window(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có muốn đóng cửa sổ này?"):
            self.root.destroy()
            if self.on_close_callback:
                self.on_close_callback()

    def on_close(self):
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
    # Khởi tạo db_manager phù hợp của bạn ở đây
    db_manager = None  # Thay bằng khởi tạo thực sự của db_manager
    task_gui = GUITask(db_manager)
    task_gui.run()
