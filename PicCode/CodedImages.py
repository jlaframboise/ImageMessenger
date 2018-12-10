from PIL import Image, ImageFilter
#import webbrowser.open("C:\\Users\\jaker\\PycharmProjects\\MainProject\\TestImagePython.png")



# pixelMap[0,0]=(20,20,100)
# pixel=pixelMap[0,0]
# print(pixel)

#bitLength=img.size[0]//8

#img=Image.open("C:\\Users\\jaker\\PycharmProjects\\MainProject\\TestImg2.png")
img=Image.new("RGB",(160,160),(120,120,120))

#A function to search an image pixel by pixel and find groups of eight correct grey or not pixels, to binary, to ascii
# then to string


gloYesCol=(255,0,0)
gloNoCol=(0,0,255)
gloString='''Hello World This works!!! What a great thing aaaaaaaaabbbbbbbccdddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeffffffffffffffffffffffffggggggggggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiijjjjjjjjjjjjjjjjjjkkkkkkkkkkkkkkkklllllllllllllllllmmmmmmmmmmmmmmmmmmmnnnnnnnnnnnnnnnnnnooooooooooooooppppppppppppqqqqqqqqqqqqqqqqqqqqrrrrrrrrrrrrrrrrrrrrrrrrrrrsssssssssssssssssssssstttttttttttttttttttttttttuuuuuuuuuuuuuuuuuuuvvvvvvvvvvvvvvvvvvvvvvvvvwwwwwwwwwwwwwwwwwwwwwwwwwwwwwxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoopwoop'''

def decodePic(img,yesColor=(100,100,100),noColor=(140,140,140)):

    pixelMap=img.load()

    #yesColor=YesColor
    #noColor=NoColor

    currentByte=[]
    decodedList=[]

    for x in range(0,img.size[1]):
        for i in range(0,img.size[0]):
            pixel=pixelMap[i,x]
            if pixel==yesColor:
                currentByte.append(1)
            elif pixel==noColor:
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

def encodePic(img,string,yesColor=(100,100,100),noColor=(140,140,140)):

    #yesColor=(100,100,100)
    #noColor=(140,140,140)
    pixelMap = img.load()
    #string='abcd'
    toEncodeList=[]
    xPos=0
    yPos=0
    for i in string:
        binNum=(bin(ord(i)))
        binNum=binNum[:1]+binNum[2:]
        if len(binNum) < 8:
            binNum = '0' + str(binNum)
        toEncodeList.append(binNum)
    for x in toEncodeList:
        for y in x:
            if y=='1':
                pixelMap[xPos,yPos]=yesColor
            elif y=='0':
                pixelMap[xPos,yPos]=noColor
            if xPos<img.size[0]-1:
                xPos+=1
            elif xPos==img.size[0]-1:
                xPos=0
                yPos+=1


encodePic(img, gloString,gloYesCol,gloNoCol)
#img.show()
print(decodePic(img,gloYesCol,gloNoCol))
img.show()

img.close()

# a=(bin(ord('$')))
# a=a[:1]+a[2:]
# if len(a)<8:
#     a='0'+str(a)
#
# print(a)





#print(decodePic(img))

