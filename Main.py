from tkinter import *
import data as d

root = Tk()
root1 = Tk()
root1.withdraw()
root.title("Login")
root1.title("To Do List")



def login():

    cus=d.conn.cursor()
    
    try:
        sql = "select 1 from Account where UserName = ? and [Password]=?"
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
    




txtUserName = StringVar()

txtPW = StringVar()
root.minsize(height=200, width=300)
root1.minsize(height=600, width=600)

Label(root, text="Tên đăng nhập").grid(row=0,column=0)
Entry(root,textvariable=txtUserName).grid(row=0,column=1)

Label(root, text="Tên đăng nhập").grid(row=1,column=0)

Entry(root,textvariable=txtPW).grid(row=1,column=1)


Button(root, text="Đăng Nhập",command=login).grid(row=2,column=0)
Button(root, text="Thoát",command=root.quit).grid(row=2,column=1)



root.mainloop()
