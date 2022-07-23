from typing import Union
from fastapi import FastAPI, Form
import os

app = FastAPI()

@app.get("/clipboard")
def get_clipboard():
	content = ""
	with open('clipboard.txt',encoding='utf8') as f:
		content = f.read()
		f.close
	print("from get_clipboard method():")
	print(content)
	return content

@app.post("/clipboard")
async def set_clipboard(content: str = Form()):
	print("server rev a post request")
	with open("clipboard.txt","w",encoding='utf8') as f:
		f.write(content)
		f.close
	return content
