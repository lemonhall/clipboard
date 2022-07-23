

### 新建一个环境
conda create --name clipboard_windows python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

### 激活环境
conda activate clipboard_windows

### 安装依赖
pip install pystray


### 启动server端
pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart

uvicorn main:app --reload

### 就用tk就完事儿了

	# Import the required libraries
	from tkinter import *
	from pystray import MenuItem as item
	import pystray
	from PIL import Image, ImageTk

	# Create an instance of tkinter frame or window
	win=Tk()

	win.title("共享剪贴板程序")
	# Set the size of the window
	win.geometry("700x350")

	# Define a function for quit the window
	def quit_window(icon, item):
	   icon.stop()
	   win.destroy()

	# Define a function to show the window again
	def show_window(icon, item):
	   icon.stop()
	   win.after(0,win.deiconify())

	# Hide the window and show on the system taskbar
	def hide_window():
	   #win.withdraw()
	   win.iconify()
	   # image=Image.open("favicon.ico")
	   # menu=(item('退出', quit_window), item('显示主窗体', show_window))
	   # icon=pystray.Icon("name", image, "共享剪贴板", menu)
	   # win.after(1000,lambda: ss())
	   # icon.run()

	def ss():
	    print("Hello World~~~")
	    win.after(1000,lambda: ss())

	win.protocol('WM_DELETE_WINDOW', hide_window)
	win.after(1000,lambda: ss())
	win.mainloop()


### 从mac端开始copy代码
pip install requests

https://github.com/terryyin/clipboard

import pyperclip

* 写内容到剪贴板
pyperclip.copy('The text to be copied to the clipboard.')

* 读内容到内存
text = clipboard.paste()  # text will have the content of clipboard

阿西吧，真是麻烦
