# Image Messenger

Steganography is the technique of hiding text in an image. After reading more on steganography, I built this stegenographic image messenger
to encode text into images by modifying the RGB values + or - 1 to indicate a 0 or 1. I used socket programming to connect a client and server and allow them to send images containing hidden text. The graphical user interface was made with TkInter in Python. 

With this program you can use a pre-shared library of images to hide text inside, and send them over a network. If both parties only send the modified image and keep secret the only copies of the original image, this method ensures perfect secrecy against anyone who captures the modified image. 

There is a window to select image and role (server / client), a window depending on role selected to set up the socket connection, then there is a final window in which they can communicate.

---

*** REQUIRED:
- Python 3 
- Pillow (fork of PIL library) *only one not included with python 
- TkInter 
- Socket 

*** Files:
- An image called TestImagePython.png in your current directory.
- You can name the image whatever you want, just update the filename in the GUI.
