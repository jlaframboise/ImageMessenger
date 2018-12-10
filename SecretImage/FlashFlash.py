import pygame
import random

clock=pygame.time.Clock()
pygame.init()

screen=pygame.display.set_mode((1900,1000))

crashed=False

while not crashed:


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            crashed=True
    pointList=[]
    for i in range(1,random.randint(4,24)):
        pointList.append((random.randint(1,1900),random.randint(1,1000)))
    pygame.draw.polygon(screen,(random.randint(1,255),random.randint(1,255),random.randint(1,255)),pointList)
    #pygame.draw.rect(screen,(random.randint(1,255),random.randint(1,255),random.randint(1,255)), (random.randint(1,1900),random.randint(1,1000), random.randint(1,100), random.randint(1,100)))
    #pygame.draw.circle(screen,(random.randint(1,255),random.randint(1,255),random.randint(1,255)), (random.randint(1,1600),random.randint(1,1000)), random.randint(1,100))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()




