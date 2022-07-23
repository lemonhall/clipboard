
### 新建一个环境
conda create --name clipboard_macos2 python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

### 激活之
conda activate clipboard_macos2

### 安装依赖
pip install requests
pip install pyclip

### 兼容性
注意：本代码已经可以成功在windows下安全运行了

### 待解决
似乎应该看一下关于图像的处理，这个是有点恶心的，图像这东西暂时不打算支持

### 制作可执行文件？

https://realpython.com/pyinstaller-python/

看了，是支持三个平台的，这就好了

### 增加mDNS支持？

pip install zeroconf

### windows下的一个兼容性问题
pip install pyclip
pyclip==225才可以在windows下正常运行，也是非常奇怪的

### 文件的编码格式问题
	with open("clipboard.txt","w",encoding='utf8') as f:
		f.write(content)
		f.close
最后统一用了utf-8，这下windows下不再报错

### windows特有的回车问题
   #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
   content = pyclip.paste().decode("utf-8")
   content = content.replace("\r\n","\n")
 在入口读取剪切板的地方，把\r这种可恶的东西干掉了
