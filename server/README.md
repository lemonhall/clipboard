

### 新建一个环境
conda create --name clipboard python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/


### 激活之
conda activate clipboard

### 安装依赖

https://fastapi.tiangolo.com/


pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart


### 开始写代码

	from typing import Union
	from fastapi import FastAPI, Form

	app = FastAPI()

	@app.get("/clipboard")
	def get_clipboard():
	    return {"Hello": "World"}

	@app.post("/clipboard")
	async def set_clipboard(content: str = Form()):
	    return content

uvicorn main:app --host 0.0.0.0

然后访问：
http://127.0.0.1:8000/clipboard


拿到了结果了，OK


### server设计

就两个API，get和set

极简风格

### post

* curl -d "content=I set this to clipboard" -X POST http://127.0.0.1:8000/clipboard

### 运行结果
	"I set this to clipboard"(base) lemonhall@yuningdeMBP:~$ curl -d "content=I set this to clipboard" -X POST http://127.0.0.1:8000/clipboard
	"I set this to clipboard"(base) lemonhall@yuningdeMBP:~$ curl -d "content=I set this to clipboard" -X POST http://127.0.0.1:8000/clipboard
	"I set this to clipboard"(base) lemonhall@yuningdeMBP:~$


### 保存到文件？
	@app.post("/clipboard")
	async def set_clipboard(content: str = Form()):
		with open("clipboard.txt","w") as f:
			f.write(content)
			f.close
		return content

搞定，写到本地文件里了

### 修改读取的方法
@app.get("/clipboard")
def get_clipboard():
	lines = ""
	with open('clipboard.txt') as f:
		lines = f.readline()
	return lines

* 测试：
curl http://127.0.0.1:8000/clipboard

### 当前主要的依赖有哪些？
	anyio==3.6.1
	certifi @ file:///private/var/folders/sy/f16zz6x50xz3113nwtb9bvq00000gp/T/abs_83242e7e-f82d-4a71-8ef2-9d71d212d249gu_wxmeq/croots/recipe/certifi_1655968827803/work/certifi
	charset-normalizer==2.1.0
	click==8.1.3
	docopt==0.6.2
	fastapi==0.79.0
	h11==0.13.0
	httptools==0.4.0
	idna==3.3
	pipreqs==0.4.11
	pydantic==1.9.1
	python-dotenv==0.20.0
	python-multipart==0.0.5
	PyYAML==6.0
	requests==2.28.1
	six==1.16.0
	sniffio==1.2.0
	starlette==0.19.1
	typing_extensions==4.3.0
	urllib3==1.26.10
	uvicorn==0.18.2
	uvloop==0.16.0
	watchfiles==0.16.0
	websockets==10.3
	yarg==0.1.9

## 到此为止，最简单的server你就可以说已经结束了

- [ ] 实现mac端
- [ ] 实现linux端
- [ ] 实现windows端
- [ ] 实现iOS端
- [ ] 实现Android端
- [ ] 实现linux的console端
- [ ] 打包成docker，这个其实简单
- [ ] 服务端和客户端增加mDNS的能力