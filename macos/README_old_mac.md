
### 新建一个环境
conda create --name clipboard_macos python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

### 激活之

conda activate clipboard_macos

### 做tray

* https://github.com/jaredks/rumps
* https://pystray.readthedocs.io/en/latest/usage.html#integrating-with-other-frameworks

做tray，倒是挺简单的，有两个选择，感觉任选一个就可以了

### 读取pasteboard

https://pypi.org/project/pasteboard/

pip install pasteboard

新建一个get.py
一切从这个开始吧

	import pasteboard

	pb = pasteboard.Pasteboard()
	content = pb.get_contents(diff=True)

	print(content)

python get.py

哦吼，每一次都会输出东西，看来这么写，diff开关，只会在运行期间，帮我们做diff

### 程序逻辑

1. 启动程序建立循环。
1. 读取剪切板，和本地文件比较，如果一致，就不做任何事情
1. 读取剪切板，....，如果不一致，则POST到远端去，等于就是sync到远端了
1. 读取远端get接口，与本地文件比较，如果一致，不做任何事情
1. 读取远端get接口，与本地另一个文件比较，如果不一致，则set本地的剪切板，sync远端的内容，同时将第1、2步提到的那个文件写成与远端一致

### 写main.py吧

### 安装rumps

pip install rumps

	import rumps
	import time


	def timez():
	    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


	@rumps.timer(5)
	def a(sender):
	    print('%r %r' % (sender, timez()))


	if __name__ == "__main__":
	    global_namespace_timer = rumps.Timer(a, 5)
	    rumps.App('myTimer').run()

这个东西很棒，直接帮我建立了一个Timer，这就很实用

### 开始联调

conda activate clipboard
uvicorn main:app --reload

server端启动起来

### 引入requests

https://requests.readthedocs.io/en/latest/user/quickstart/

	import requests

	payload = {'key1': 'value1', 'key2': 'value2'}

	r = requests.post("https://httpbin.org/post", data=payload)

### 恶心的小坑

r.text返回回来是自带双引号
    if res.startswith('"'):
        res = res[1:]
    if res.endswith('"'):
        res = res[:-1]
我只好用这种办法给它去了

### 恶心的第二个坑

还是这个r.text

我发现它会把这样的内容：
    if res.startswith('"'):
        res = res[1:]

给我编码成这样：
    if res.startswith('\"'):\n

### 解决
https://stackoverflow.com/questions/38401450/n-in-strings-not-working


