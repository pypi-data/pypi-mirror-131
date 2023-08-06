"""
UNDB
Thanks:https://www.cnblogs.com/featherl/p/11075038.html
"""
import tkinter
from UNKnownDB.DB import LocalDB

# 导入tkinter库


win = tkinter.Tk()  # 创建窗口
win.title('文本编辑器')  # 设置标题
win['bg'] = '#0099ff'
win.state('zoomed')
win.iconify()

entry_file = tkinter.Entry(win)  # 创建一个文本输入框，用来设置文件路径
entry_file.pack()  # 放置该输入框


def do_open():
    # 打开文件
    file_path = entry_file.get()  # 获取文本框的内容
    with open(file_path) as fr:
        # 打开文件
        content = fr.read()  # 一次性读取文件内容，对大文件不宜使用
        text.delete(0.0, tkinter.END)  # 清空文本框内容
        text.insert(tkinter.END, content)  # 在光标后插入内容


def do_save():
    # 保存文件
    content = text.get(0.0, tkinter.END)  # 获取文本框内容
    file_path = entry_file.get()  # 文件路径
    with open(file_path, 'w') as fw:
        fw.write(content)  # 写入数据到文件中


def do_interpret():
    db = LocalDB('')
    db.write()


btn_open = tkinter.Button(win, text='打开', command=do_open)  # 创建按钮用于打开文件
btn_save = tkinter.Button(win, text='保存', command=do_save)  # 创建按钮用于保存文件
btn_interpret = tkinter.Button(win, text='运行', command=do_interpret)  # 创建按钮用于运行文件

# 放置按钮
btn_open.pack()
btn_save.pack()
btn_interpret.pack()

# 创建多行文本框，用于编辑文件
text = tkinter.Text(win)
text.pack()

win.mainloop()  # 进入消息循环
