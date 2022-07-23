# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import pyclip
import requests
from time import sleep
from threading import Thread

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

def setup_checker():
# create and start the daemon thread
    print('Starting background task...')
    daemon = Thread(target=background_task, args=(2,), daemon=True, name='Background')
    daemon.start()

# Hide the window and show on the system taskbar
def hide_window():
    #win.withdraw()
    win.iconify()
    image=Image.open("favicon.ico")
    menu=(item('quit', quit_window), item('show', show_window))
    icon=pystray.Icon("name", image, "Share clipboard", menu)
    icon.run()


# 这三个函数是在搞定更新的
def write_to_local_post_buffter(content):
    with open("local_clipboard_buffter.txt","w") as f:
        f.write(content)
        f.close

def if_diff_clipboard():
    local_clipboard_buffter = ""
    lastest_posted  = ""
    with open('local_clipboard_buffter.txt') as f:
        local_clipboard_buffter = f.read()
        f.close
    with open('lastest_posted.txt') as f:
        lastest_posted = f.read()
        f.close
    print("I am in if_diff_clipboard")
    print("the local_clipboard_buffter is:=======================")
    print(local_clipboard_buffter)     
    print("the lastest_posted is:=======================")
    print(lastest_posted)
    print("end of args:=======================")   
    if local_clipboard_buffter == lastest_posted:
        print("剪贴板内容与上一次远程上传的内容一致")
        return True
    else:
        print("剪贴板内容与上一次远程上传的内容不一致")
        #写lastest_posted文件，开始post新内容到远程
        with open("lastest_posted.txt", 'w') as fd:
            fd.write(local_clipboard_buffter)
            fd.close
        return False

def post_to_server(content):
    print("I am in post_to_server")
    payload = {'content': content }
    r = requests.post("http://127.0.0.1:8000/clipboard", data=payload)
    print(r.text)#这里应该是检查是否是200状态，如果是则返回True，然后下面写入local文件


def get_content_from_server():
    r = requests.get('http://127.0.0.1:8000/clipboard')
    res = r.text
    #print(r.text)
    #去掉返回的头和尾的双引号，真是烦人的一个库
    if res.startswith('"'):
        res = res[1:]
    if res.endswith('"'):
        res = res[:-1]
    #https://stackoverflow.com/questions/38401450/n-in-strings-not-working
    #实际上你拿到的也不是一个已经encode好了的字符串说白了，所以还需要做一次unicode转义
    contents = res.encode("raw_unicode_escape")
    contents = contents.decode("unicode_escape")
    # if contents.endswith('\n'):
    #     contents = contents[:-1]
    #print(contents)
    #然后现在拿到的就是粘贴是啥，返回的还是啥了
    with open("local_get_buffter.txt", 'w') as fd:
        fd.write(contents)
        fd.close
    return contents

def if_diff():
    local_get_buffer = ""
    lastest_updated  = ""
    with open('local_get_buffter.txt') as f:
        local_get_buffer = f.read()
        f.close
    with open('lastest_updated.txt') as f:
        lastest_updated = f.read()
        f.close     
    if local_get_buffer == lastest_updated:
        print("远程剪贴板与本地缓存一致")
        return True
    else:
        print("远程剪贴板与本地缓存不一致！！更新缓存")
        with open("lastest_updated.txt", 'w') as fd:
            fd.write(local_get_buffer)
            fd.close
        return False



# 这个是主逻辑，从自己的mac程序test_checker2.py里面抄出来的，以后可以包装一个类，兼容三端
def checker():
   print("Hello World~~~")
   #get a bytes,convert it to string
   #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
   content = pyclip.paste().decode("utf-8")
   print("I am in checker begging.....3 lines, I print out pyperclip.paste()'s result")
   print(content)
   write_to_local_post_buffter(content)
   if if_diff_clipboard():
      print("剪贴板内容与上一次远程上传的内容一致")
      print("什么都不用做")
      print("tick tick local nothing changes")
   else:
      post_to_server(content)

   remote_clip_content = get_content_from_server()
   if if_diff():
      print("remote content equals local .....do nothing")
   else:
      print("更新本地剪切板")
      pyclip.copy(remote_clip_content)

   #注册下一次调用
   win.after(5000,lambda: checker())


# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    while True:
        # block for the interval
        sleep(interval_sec)
        # perform the task
        checker()
        print('Background task!')

win.protocol('WM_DELETE_WINDOW', hide_window)
#pyperclip.copy('The text to be copied to the clipboard.')
#create and start the daemon thread
print('Starting background task...')
daemon = Thread(target=background_task, args=(5,), daemon=True, name='Background')
daemon.start()

win.mainloop()