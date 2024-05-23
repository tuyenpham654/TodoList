
# # Tạo hai cửa sổ
# root1 = tk.Tk()
# root2 = tk.Tk()

# # Ẩn cửa sổ root2 ban đầu
# root2.withdraw()
# # Hàm callback khi bấm vào nút
# def toggle_windows():
#     if root2.state() == "withdrawn":
#         root1.withdraw()
#         root2.deiconify()
#     else:
#         root2.withdraw()
#         root1.deiconify()

# # Tạo nút bấm trong root1
# button = tk.Button(root1, text="Chuyển đổi cửa sổ", command=toggle_windows)
# button.pack()
# # Hiển thị root1
# root1.mainloop()