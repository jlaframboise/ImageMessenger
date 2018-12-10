from PIL import Image, ImageFilter

import time



img=Image.open("img34.jpeg")








def decodePic(img, newImg):

    orgPixelMap=img.load()
    pixelMap=newImg.load()
    varience = 1

    currentByte=[]
    decodedList=[]

    for x in range(0,img.size[1]):
        for i in range(0,img.size[0]):
            moddedPixel=pixelMap[i,x]
            pixel=orgPixelMap[i,x]
            if moddedPixel[0]==pixel[0]+varience or moddedPixel[0]==pixel[0]+(-2*varience):
                currentByte.append(1)
            elif moddedPixel[0]==pixel[0]-varience or moddedPixel[0]==pixel[0]-(-2*varience):
                currentByte.append(0)
            if len(currentByte)==8:
                valSum=0
                for a in range(0,8):
                    if currentByte[a]==1:
                        valSum+=2**(7-a)
                decodedList.append(valSum)
                currentByte=[]
    decodedString=''.join(chr(i) for i in decodedList)

    return decodedString

def encodePic(img,string):
    global imgNew
    imgNew = img.copy()
    pixelMapNew = imgNew.load()

    toEncodeList=[]
    xPos=0
    yPos=0
    varience = 1
    for i in string:
        binNum=(bin(ord(i)))
        binNum=binNum[:1]+binNum[2:]
        if len(binNum) < 8:
            binNum = '0' + str(binNum)
        toEncodeList.append(binNum)
    for x in toEncodeList:
        for y in x:
            if y=='1':
                if pixelMapNew[xPos,yPos][0]==255:
                    varience=-2
                pixelMapNew[xPos,yPos]=(pixelMapNew[xPos,yPos][0]+varience,pixelMapNew[xPos,yPos][1],pixelMapNew[xPos,yPos][2])
                varience=1
            elif y=='0':
                if pixelMapNew[xPos,yPos][0]==0:
                    varience=-2
                pixelMapNew[xPos,yPos]=(pixelMapNew[xPos,yPos][0]-varience,pixelMapNew[xPos,yPos][1],pixelMapNew[xPos,yPos][2])
                varience = 1
            if xPos<imgNew.size[0]-1:
                xPos+=1
            elif xPos==imgNew.size[0]-1:
                xPos=0
                yPos+=1



gloString="Hello World"*2008
encodePic(img, gloString)


imgNew.save('imgCopy.bmp')
print(decodePic(img, imgNew))
img.show()
time.sleep(2)
imgNew.show()

img.close()
imgNew.close()
