import pyclip
# Linux
# Linux on X11 requires xclip to work. 
# Install with your package manager, e.g. 
# sudo apt install xclip 

# Linux on Wayland requires wl-clipboard to work. 
# Install with your package manager, e.g. 
# sudo apt install wl-clipboard

pyclip.copy("hello clipboard") # copy data to the clipboard