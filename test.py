from tkinter import *
import data as d
from tkinter import ttk

win = Tk()

# Tạo LabelFrame cho form login
lf = LabelFrame(win, text='Login')
lf.grid(row=0, column=0, padx=70, pady=35)

# Thêm các widget vào LabelFrame
l1 = Label(lf, text="Tên đăng nhập")
l1.grid(row=0, column=0)
e1 = Entry(lf)
e1.grid(row=0, column=1)

Label(lf, text="Mật khẩu").grid(row=1, column=0)
Entry(lf).grid(row=1, column=1)

Button(lf, text="Đăng Nhập").grid(row=2, column=0)
Button(lf, text="Thoát", command=win.quit).grid(row=2, column=1)


# Tạo frame chính và đặt nó vào grid
main_frame = Frame(win)
main_frame.grid(row=1, column=0, sticky="nsew")

# Cấu hình grid cho frame chính để nó chiếm toàn bộ diện tích cửa sổ
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)

# Tạo canvas và scrollbar
my_canvas = Canvas(main_frame)
my_canvas.grid(row=0, column=0, sticky="nsew")
my_sb = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_sb.grid(row=0, column=1, sticky="ns")

# Cấu hình grid cho my_sb và my_canvas để chúng tự động thay đổi kích thước
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=0)  # Cho phép my_sb có chiều rộng cố định

# Cấu hình canvas và scrollbar để hoạt động cùng nhau
my_canvas.configure(yscrollcommand=my_sb.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Tạo frame con để chứa các widget
lf1 = Frame(my_canvas)
my_canvas.create_window((0, 0), window=lf1, anchor="nw")

i = 1

# Lấy dữ liệu từ cơ sở dữ liệu
cus1 = d.conn.cursor()
sql = "select * from view_task"
cus1.execute(sql)
resultlg = cus1.fetchall()

# Hiển thị dữ liệu vào các label
for x in resultlg:
    i += 1
    Label(lf1, text=x[0]).grid(column=0, row=i, padx=10, pady=10)
    Label(lf1, text=x[1]).grid(column=1, row=i, padx=10, pady=10)
    Label(lf1, text=x[2]).grid(column=2, row=i, padx=10, pady=10)
    Label(lf1, text=x[3]).grid(column=3, row=i, padx=10, pady=10)
    Label(lf1, text=x[4]).grid(column=4, row=i, padx=10, pady=10)
    Checkbutton(lf1).grid(column=5, row=i)
    Button(lf1).grid(column=6, row=i)

# Thêm các button bổ sung
for x in range(100):
    Button(lf1, text=x).grid(column=0, row=i+x+1, padx=10, pady=10)



win.mainloop()