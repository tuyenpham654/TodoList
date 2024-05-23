from tkinter import *
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
  
    for x in resultlg:
        
        litbox.insert(END,x)
    
#login
txtUserName = StringVar()
txtPW = StringVar()
root.minsize(height=200, width=300)
root1.minsize(height=600, width=600)

Label(root, text="Tên đăng nhập").grid(row=0,column=0)
Entry(root,textvariable=txtUserName).grid(row=0,column=1)

Label(root, text="Mật khẩu").grid(row=1,column=0)
Entry(root,textvariable=txtPW).grid(row=1,column=1)


Button(root, text="Đăng Nhập",command=login).grid(row=2,column=0)
Button(root, text="Thoát",command=root.quit).grid(row=2,column=1)

#show data trong list
litbox = Listbox(root1, width=80,height=20)
litbox.grid(column=0,row=0)


root.mainloop()
