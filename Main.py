from tkinter import *
from tkinter import ttk
import data as d

root = Tk()
root1 = Tk()
root1.withdraw()
root.title("Login")
root1.title("To Do List")



def login():
    global txtUserName_value
    cus = d.conn.cursor()
    txtUserName_value = txtUserName.get()
    try:
        sql = "select 1 from users where username = ? and [password]=?"
        cus.execute(sql,(txtUserName.get(),txtPW.get()))
        resultlg = cus.fetchall()
    except:
        resultlg = ()
    
    a=len(resultlg)
    if a == 1:
        if root1.state() == "withdrawn":
            root.withdraw()
            root1.deiconify()
        else:
            root1.withdraw()
            root.deiconify()
    show(txtUserName_value)

def show(usn):
    
    cus=d.conn.cursor()
    try:
        sql = "select * from view_task where username = ?"
        cus.execute(sql,(usn,))
        resultlg = cus.fetchall()
    except:
        resultlg = ()
    i=1
    Button(root1,text="ma").grid(column=0,row=i)
    Button(root1,text="title").grid(column=1,row=i)
    Button(root1,text="description").grid(column=2,row=i)
    Button(root1,text="due Date").grid(column=3,row=i)
    Button(root1,text="create at").grid(column=4,row=i)
    for x in resultlg:
        i += 1
        Label(root1, text=x[0]).grid(column=0, row=i, padx=10, pady=10)
        Label(root1, text=x[1]).grid(column=1, row=i, padx=10, pady=10)
        Label(root1, text=x[2]).grid(column=2, row=i, padx=10, pady=10)
        Label(root1, text=x[3]).grid(column=3, row=i, padx=10, pady=10)
        Label(root1, text=x[4]).grid(column=4, row=i, padx=10, pady=10)
        Checkbutton(root1).grid(column=5, row=i)
        Button(root1).grid(column=6, row=i)
    
    
#login
txtUserName = StringVar()
txtPW = StringVar()
root.minsize(height=200, width=300)
root1.minsize(height=600, width=600)

lf = LabelFrame(root,text='Login')
lf.grid(row=0,column=0, padx=70,pady=35)


l1=Label(lf, text="Tên đăng nhập")
l1.grid(row=0,column=0)
e1=Entry(lf,textvariable=txtUserName)
e1.grid(row=0,column=1)

Label(lf, text="Mật khẩu").grid(row=1,column=0)
Entry(lf,textvariable=txtPW).grid(row=1,column=1)


Button(lf, text="Đăng Nhập",command=login).grid(row=2,column=0)
Button(lf, text="Thoát",command=root.quit).grid(row=2,column=1)

lf2 =LabelFrame(root,text="thêm tasks mới")
lf2.grid(row=1,column=0)
e1=Entry(lf2)
e1.grid(column=0,row=0)
e1=Button(lf2,text="+")
e1.grid(column=1,row=0)




# Tạo frame chính và đặt nó vào grid
main_frame = Frame(root)
main_frame.grid(row=2, column=0, sticky="nsew")

# Cấu hình grid cho frame chính để nó chiếm toàn bộ diện tích cửa sổ
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

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
root.mainloop()
