import pygame.camera
import pygame.image
import time
import subprocess
import os

def ok(i):
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    pygame.image.save(img, "static/images/photo"+str(i)+".bmp")
    pygame.camera.quit()
    cam.stop()
    print "running!!!"

i=0
a=[]
while True:
    ok(i)
    a.append(i)
    if len(a)>=150:
        b=a.pop(0)
        #cmd=['rm','~/Desktop/tornadoexp/static/images.photo'+str(b)+'.bmp']
        os.remove('static/images/photo'+str(b)+'.bmp')
    i+=1
    time.sleep(1)