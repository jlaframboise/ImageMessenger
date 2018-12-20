# ImageMessenger

This program ia a graphical program to take user input, encrypt the text into a picture, save it and send it over
a socket connection where it will be decrypted by the other computer by comparing it to the same base image.
The plaintext will then be displayed on the other user's GUI.

There is a window to select image and role, then two different windows depending on role selected to set up connection,
then there is a final window in which they can communicate.

***REQUIRED:
    -Python 3
    -Pillow (fork of PIL library) *only one not included with python
    -TkInter
    -Socket
    **Files:
        An image called TestImagePython.png in your current directory.
        - You can name the image whatever you want, just update the filename in the GUI.\n
