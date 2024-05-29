import tkinter as tk
from tkcalendar import Calendar
import datetime

from app_logic import AppLogic

from gui_login import GUILogin
from gui_category import GUICategory


class App:
    
    def __init__(self , db_manager):
        
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("TodoList")
        self.root.geometry("1000x700")
        

        self.gui_login = None
        self.gui_category= None
        self.create_widgets()

    def create_widgets(self):
        app_logic_instance = AppLogic()

        # Header
        header_frame = tk.Frame(self.root, height=20, bg="lightgrey")
        header_frame.pack(side=tk.TOP, fill=tk.X, anchor="e")
        
        # Header label
        # User = app_logic_instance.get_current_user()

        # if User != None:
        #     header_label = tk.Label(header_frame, text=f"Hi: {User}", font=("Arial", 9), bg="lightgrey")
        #     header_label.pack(side=tk.LEFT, pady=10)
            
        # Đăng nhập/Đăng ký button
        login_button = tk.Button(header_frame, text="Đăng nhập/Đăng ký", command=self.show_login)
        login_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Sidebar
        sidebar_frame = tk.Frame(self.root, width=200, bg="black")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Vertical separator line for sidebar
        separator_frame = tk.Frame(self.root, width=1, bg="black")
        separator_frame.pack(side=tk.LEFT, fill=tk.Y)

        # entry in Sidebar
        today = datetime.date.today()
        
        cate_frame = tk.Frame(sidebar_frame)
        cate_frame.pack(side=tk.LEFT,anchor="n")
        
        add_lb= tk.Label(cate_frame,text="Danh Mục",width=30)
        add_lb.pack(fill="both")
        add_btn=tk.Button(cate_frame,text="Thêm category",width=30,command=self.show_category)
        add_btn.pack(fill="both")

        mincate_frame = tk.Frame(cate_frame,background="black")
        mincate_frame.pack(fill="both")
        i = 0
        catelist = app_logic_instance.show_category(self.db_manager)
        for x in catelist:
            i+=1
            ctlb= tk.Button(mincate_frame,text=x[1],width=30)
            ctlb.grid(row=i,column=0,pady=5)
            ctbtn= tk.Button(mincate_frame,text="sửa")
            ctbtn.grid(row=i,column=1,pady=5)
            ctbtn1= tk.Button(mincate_frame,text="xóa")
            ctbtn1.grid(row=i,column=2,pady=5)



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
       
    #thêm task
    def show_category(self):
        self.gui_category = GUICategory(self.db_manager)
        self.gui_category.run()
        
        
if __name__ == "__main__":
    app = App()
    app.run()
