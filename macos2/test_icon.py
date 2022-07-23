# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import pyclip
import requests
from time import sleep
from threading import Thread
#from zeroconf import ServiceBrowser, ServiceListener, Zeroconf,ServiceInfo

import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


http_server_url = ""

#这里估计需要调一会儿了，这个库看上去质量挺好，但是没有啥教程类的，得再看看
# class MyListener(ServiceListener):

#     def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         print(f"Service {name} updated")

#     def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         print(f"Service {name} removed")

#     def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         info = zc.get_service_info(type_, name)
#         print(f"Service {name} added, service info: {info}")


# zeroconf = Zeroconf()
# listener = MyListener()
# browser  = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

# (type='_http._tcp.local.', 
# name='nas16t._http._tcp.local.', 
# addresses=[b'\xc0\xa82\xe9'], 
# port=15000, weight=0, priority=0, 
# server='nas16t.local.', 
# properties={b'vendor': b'Synology', 
# b'model': b'DS220+', b'serial': b'21C0RLREXBPRP', 
# b'version_major': b'7', b'version_minor': b'1', 
# b'version_build': b'42661', b'admin_port': b'15000', 
# b'secure_admin_port': b'15001', 
# b'mac_address': b'90:09:d0:0d:e7:ed'}, 
# interface_index=None)

# myServiceInfo = ServiceInfo(type_='_http._tcp.local.',name='clipboard._http._tcp.local.',port=8000)
# zeroconf.register_service(myServiceInfo)

#import setproctitle

#setproctitle.setproctitle("clipboard")
# Create an instance of tkinter frame or window
win=Tk()

win.title("共享剪贴板程序")
# Set the size of the window
win.geometry("700x350")

# Define a function for quit the window
def quit_window(icon, item):
    #zeroconf.close()
    icon.stop()
    win.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   win.after(0,win.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
    win.withdraw()
    #win.iconify()
    image=Image.open(resource_path("favicon.ico"))
    menu=(item('退出', quit_window), item('显示主窗口', show_window))
    icon=pystray.Icon("name", image, "Share clipboard", menu)
    icon.run()



# 这三个函数是在搞定更新的
def write_to_local_post_buffter(content):
    with open(resource_path("local_clipboard_buffter.txt"),"w",encoding='utf8') as f:
        f.write(content)
        f.close

def if_diff_clipboard():
    local_clipboard_buffter = ""
    lastest_posted  = ""
    with open(resource_path('local_clipboard_buffter.txt'),encoding='utf8') as f:
        local_clipboard_buffter = f.read()
        f.close
    with open(resource_path('lastest_posted.txt'),encoding='utf8') as f:
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
        with open(resource_path("lastest_posted.txt"), 'w',encoding='utf8') as fd:
            fd.write(local_clipboard_buffter)
            fd.close
        return False

def post_to_server(content):
    print("I am in post_to_server")
    payload = {'content': content }
    print("check server url:")
    print(http_server_url)
    r = None
    #这里相当于是一个死循环，不断重试
    while r is None:
        try:
            r = requests.post(http_server_url, data=payload,timeout=(2, 3))
            print(r)
        except Exception as e:
            print(f"[!] Exception caught: {e}")
            print("网络这块，啥都别说了，就无限制重复就好了，好多种错误，你能咋整？")
            sleep(5)
    print(r.text)#这里应该是检查是否是200状态，如果是则返回True，然后下面写入local文件


def get_content_from_server():
    print("check server url:")
    print(http_server_url)
    r = None
    #这里相当于是一个死循环，不断重试
    while r is None:
        try:
            r = requests.get(http_server_url,timeout=(2, 3))
        except Exception as e:
            print(f"[!] Exception caught: {e}")
            print("网络这块，啥都别说了，就无限制重复就好了，好多种错误，你能咋整？")
            sleep(5)
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
    with open(resource_path("local_get_buffter.txt"), 'w',encoding='utf8') as fd:
        fd.write(contents)
        fd.close
    return contents

def if_diff():
    local_get_buffer = ""
    lastest_updated  = ""
    with open(resource_path('local_get_buffter.txt'),encoding='utf8') as f:
        local_get_buffer = f.read()
        f.close
    with open(resource_path('lastest_updated.txt'),encoding='utf8') as f:
        lastest_updated = f.read()
        f.close     
    if local_get_buffer == lastest_updated:
        print("远程剪贴板与本地缓存一致")
        return True
    else:
        print("远程剪贴板与本地缓存不一致！！更新缓存")
        with open(resource_path("lastest_updated.txt"),'w',encoding='utf8') as fd:
            fd.write(local_get_buffer)
            fd.close
        return False



# 这个是主逻辑，从自己的mac程序test_checker2.py里面抄出来的，以后可以包装一个类，兼容三端
def checker():
    print("本地剪切板轮训检查开始")
    #get a bytes,convert it to string
    #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
    try:
        print("====Type of paste====")
        print(type(pyclip.paste()))
        content = pyclip.paste().decode("utf-8")
        content = content.replace("\r\n","\n")
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
            Fact = remote_clip_content
            T.delete("1.0", "end")  # if you want to remove the old data
            T.insert(END,Fact)
    except Exception as e:
            print(f"[!] 剪切板解码失败: {e}")
            pyclip.copy("")
            print("那还能咋整，清空剪切板得了")

# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    n=0
    while True:
        print("I am in def background_task(interval_sec)")
        # block for the interval
        sleep(interval_sec)
        # perform the task
        checker()
        print('Background task process end!')
        print(n)
        n=n+1

#更新全局变量服务器地址
def init_server_address():
    print("初始化的时候，先把本地的剪切板更新成空字符串，避免一些错误")
    pyclip.copy("")

    tmp_server_address = ""
    with open(resource_path('http_server_url.ini'),encoding='utf8') as f:
        tmp_server_address = f.read()
        f.close
        print("config:http_server_url==========")
        print(tmp_server_address)
    return tmp_server_address

###============================================这基本上等于就是主程序部分======================================
win.protocol('WM_DELETE_WINDOW', hide_window)
#win.iconbitmap('./favicon.ico')
#拿到服务器地址的配置
http_server_url = init_server_address()

#pyperclip.copy('The text to be copied to the clipboard.')
# create and start the daemon thread
print('Starting background task...')
daemon = Thread(target=background_task, args=(1,), daemon=True, name='Background')
daemon.start()

#挺好使，这个设置图标的管用
win.iconphoto(False, PhotoImage(file=resource_path('android-chrome-512x512.png')))
#resource_path("images/bitcoin.png")

# Create text widget and specify size.
T = Text(win, height = 50, width = 152)
Fact = """共享剪贴板板内容同步中......"""
T.pack()
# Insert The Fact.
T.insert(END, Fact)

win.mainloop()
