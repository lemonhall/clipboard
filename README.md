## 局域网共享剪贴板的项目

<img width="749" alt="image" src="https://user-images.githubusercontent.com/637919/180456428-881e23a1-3946-43aa-b6b2-28ad524a6266.png">
<img width="179" alt="image" src="https://user-images.githubusercontent.com/637919/180456466-fc082baa-64af-48ee-ba9a-38707e9be66e.png">


* /server 有服务器端的代码
* /ubuntu 有22.04下测试下来跑的很好的代码
* /windows win 11条件下测试，win-win跑得起来的代码，对其他系统，会多空行，需要解决
* /macos 没有依赖tk的独立程序，跑得也很好，后期可以考虑其实三端都统一到tk这边来
* /macos2 重构后的Mac版程序，可以在windows和ubutun下再测试一下，如果ok，就可以把三端的程序统一了，比预想的要简单，tk使用了线程，很稳定了


## 二进制文件：2022/07/24
* [mac版本的包](https://github.com/lemonhall/clipboard/raw/main/macos2/dist.zip)
* [ubuntu版本的包](https://github.com/lemonhall/clipboard/raw/main/ubuntu/dist.zip)
* [windows版本的包](https://github.com/lemonhall/clipboard/raw/main/windows/dist.zip)


## Todos:

- [:heavy_check_mark:] 实现基础的服务端
- [:heavy_check_mark:] 实现mac端
- [:heavy_check_mark:] 实现linux端
- [:heavy_check_mark:] 实现windows端
- [ ] 实现iOS端
- [ ] 实现Android端
- [ ] 实现linux的console端
- [ ] 打包成docker，这个其实简单
- [ ] chrome端也可以加入
- [ ] 服务端和客户端增加mDNS的能力
- [:heavy_check_mark:] 三端打包出独立的可执行文件
- [ ] 暂时先读取配置文件来定位服务器地址吧，稍后加上界面和mDNS能力的链条
- [ ] 客户端与服务器之间轮训的改进，get方法加入304机制，这样大大减少传输
- [ ] 加入容错机制，处理各种通讯异常
- [ ] 加入测试代码
