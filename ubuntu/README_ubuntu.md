### 新建一个环境
conda create --name clipboard_ubuntu python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

### 看来conda的版本还是太老了，重装一个2022.05的版本的
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/?C=M&O=D

### activete env
conda activate clipboard_ubuntu

###
pip install pystray

### 安装拷贝粘贴的兼容库

changing

https://pypi.org/project/pyclip/

### install system package
Linux
Linux on X11 requires xclip to work. Install with your package manager, e.g. sudo apt install xclip Linux on Wayland requires wl-clipboard to work. Install with your package manager, e.g. sudo apt install wl-clipboard

* sudo apt install wl-clipboard

### copy windows programe to linux will be fine

pip install requests

主程序竟然完全可以与windows公用，可移植性非常得好，多亏了tk啊，我得再看看tk这边，肯定能优化的非常好