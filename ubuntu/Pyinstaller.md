### 教程
https://realpython.com/pyinstaller-python/

### 官网
https://pyinstaller.org/en/stable/


### 安装
pip install -U pyinstaller

### 使用
pyinstaller test_icon.py

### 选项

对我来说比较有用的两个选项就是

* pyinstaller cli.py -w
这个是针对GUI程序的

* --add-data and --add-binary

Instruct PyInstaller to insert additional data or binary files into your build.

This is useful when you want to bundle in configuration files, examples, or other non-code data. You’ll see an example of this later if you’re following along with the feed reader project.

### 报错
	Exception in thread Background:
	Traceback (most recent call last):
	  File "threading.py", line 932, in _bootstrap_inner
	  File "threading.py", line 870, in run
	  File "test_icon.py", line 201, in background_task
	  File "test_icon.py", line 166, in checker
	  File "pyclip\__init__.py", line 42, in paste
	  File "pyclip\win_clip.py", line 227, in paste
	  File "pyclip\win_clip.py", line 159, in _handle_format
	  File "pyclip\win_clip.py", line 167, in _handle_hdrop
	NotImplementedError: Currently HDROP paste is only supported for single files. It appears multiple files or directories were specified

报错位置的代码如下：

    def _handle_hdrop(self, data: Tuple[str, ]) -> bytes:
        if not isinstance(data, tuple):
            raise TypeError(f"Unexpected type for HDROP. Data must be tuple, not {type(data)}")
        if len(data) > 1:
            raise NotImplementedError("Currently HDROP paste is only supported for single files. It appears multiple files or directories were specified")
        if len(data) < 1:
            raise ValueError("Data unexpectedly empty")
        fname = data[0]
        if not os.path.isfile(fname):
            raise ValueError("Can only paste files. Did you copy a directory?")
        with open(fname, 'rb') as f:
            return f.read()

这个报错应该与框架本身无关，等于是在抱怨剪切板里有多个文件，这应该是和我刚才copy了多个文件，就是那些个txt文件到exe生成目录所导致的

### 依赖文件
生成好了以后实际上是依赖两个图片文件以及四个txt文件的，要记得提前拷贝的生成的包文件里去

### 最后的生产机build选项
pyinstaller test_icon.py --onefile -w 


### mac下的报错

	I am in def background_task(interval_sec)
	Traceback (most recent call last):
	  File "test_icon.py", line 216, in <module>
	  File "tkinter/__init__.py", line 4064, in __init__
	  File "tkinter/__init__.py", line 4009, in __init__
	_tkinter.TclError: couldn't open "./android-chrome-512x512.png": no such file or directory
	[47329] Failed to execute script 'test_icon' due to unhandled exception!
	logout

就是我copy了文件它也不管

pyinstaller test_icon.py --add-data 'android-chrome-512x512.png:.'

https://www.trickster.dev/post/compiling-python-programs-with-pyinstaller/

	import sys
	import os

	def resource_path(relative_path):
	    try:
	    # PyInstaller creates a temp folder and stores path in _MEIPASS
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.abspath(".")

	    return os.path.join(base_path, relative_path)

增加了一段兼容pyinstaller的目录树的处理子程序，需要在win下再测试一下
