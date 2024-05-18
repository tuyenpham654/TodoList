from tkinter import *


def login():
    pw=txtPW.get()
    us=txtUserName.get()
    Label(root,text=txtUserName.get()).grid(row=3,column=1)
    Label(root,text=txtPW.get()).grid(row=3,column=2)


root = Tk()

txtUserName = StringVar()

txtPW = StringVar()
root.minsize(height=500, width=500)

Label(root, text="Tên đăng nhập").grid(row=0,column=0)
Entry(root,textvariable=txtUserName).grid(row=0,column=1)

Label(root, text="Tên đăng nhập").grid(row=1,column=0)

Entry(root,textvariable=txtPW).grid(row=1,column=1)


Button(root, text="Đăng Nhập",command=login).grid(row=2,column=1)
Button(root, text="Thoát",command=root.quit).grid(row=2,column=2)



root.mainloop()