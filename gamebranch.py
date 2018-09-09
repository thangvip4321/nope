import pygame
import tmx
import sys
import time
from tmx import TileMap
import random
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
from mario import Mario
condition = True
pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
black =(0,0,0)
white =(256,256,256)
mariomap = tmx.load("untitled.tmx", screen.get_size())
oblay = mariomap.layers["Triggers"]
paused = False
def spritecollide(mask1,mask2,rect1,rect2):
    a = 0
    collide = []
    if rect1.left > rect2.right or rect1.right < rect2.left or rect1.top > rect2.bottom or rect1.bottom < rect2.top:
                pass
    else:
        l = max(rect1.left,rect2.left)
        t = max(rect1.top,rect2.top)
        for x in range (min(rect1.right,rect2.right)-max(rect1.left,rect2.left)):
                for y in range (min(rect1.bottom,rect2.bottom)-max(rect1.top,rect2.top)):
                        if (mask1[l-rect1.left+x][t-rect1.top +y] == True) and (mask2[l-rect2.left+x][t-rect2.top +y] == True):
                                collide.append((l-rect1.left +x,t -rect1.top + y))
    c = bool(len(collide) != 0)
    return collide,c

def collision(x,y,xsize,ysize,obj):                       
        if len(obj) == 0:
            stop = 0
            return "no" ,x,y,stop     # apply acceleration
        else:
            for object in obj:
                dis1 = abs(x+xsize-object.left)
                dis2 = abs(x-object.right)
                dis3 =abs(y+ysize - object.top)
                dis4 = abs(y -object.bottom)
                dislist = [dis1,dis2,dis3,dis4]
                if min(dislist) ==dis1:
                    x =object.left - xsize -1
                    stop = 0
                    col = "left"
                elif min(dislist) ==dis2:
                    x = object.right + 1
                    stop = 0
                    col ="right"
                elif min(dislist) == dis3:
                    y = object.top - ysize 
                    stop = 1
                    col =" top"
                else:
                    y =object.bottom +1
                    stop =1
                    col = "bottom"
            return col,x,y,stop
def tilemap_to_screen(a,b,centerx,centery): 
        x = a+ 320 - centerx
        y = b + 240 - centery
        return x,y                              
def screen_to_tilemap(x,y,centerx,centery):
        a = x+ centerx-320
        b = y +centery -240
        return a,b
class Turtle(pygame.sprite.Sprite):
    centerx = 0
    centery = 0
    containers = {}
    def __init__(self,x,y):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self,Turtle.containers)
       self.image = pygame.image.load("images.png").convert_alpha()
       self.image = pygame.transform.scale(self.image,(51,34))
       self.rect =self.image.get_rect()
       self.gravity = 0.4
       self.velo = 0
       self.speed = 1
       self.turwidth = self.rect.width
       self.turheight = self.rect.height
       self.x,self.y = x,y
       
    def update(self):
        self.velo = self.velo+self.gravity
        self.turtlerect = pygame.Rect(self.x,self.y,self.turwidth,self.turheight)
        self.obstacles = oblay.collide(self.turtlerect,["platform","brick","boundaries"])
        pos , self.x , self.y , midair = collision(self.x,self.y,self.turwidth,self.turheight,self.obstacles)
        if midair == 0:
                pass
        else:
                self.velo = 0
        if pos == "left" or pos == "right":
                self.speed = -self.speed
        self.x = self.x+ self.speed
        self.y = self.y+ self.velo
        self.a,self.b = tilemap_to_screen(self.x,self.y,Turtle.centerx,Turtle.centery)
        self.rect =pygame.Rect(self.a,self.b,self.turwidth,self.turheight)
    def mask(self):
        mask = []
        for x in range(self.turwidth):
            mask.append([])
            for y in range (self.turheight):
                mask[x].append(bool(self.image.get_at((x,y))[3]))
        return mask

all = pygame.sprite.RenderUpdates()
turtles = pygame.sprite.Group()
marios= pygame.sprite.Group()
Turtle.containers = turtles, all
Mario.containers = marios, all
mario =Mario()
turtle = Turtle(200,100)
turtle1 = Turtle(random.randint(0,1000),random.randint(0,500))
Mario.oblay = oblay
font = pygame.font.Font(None, 36)
text = font.render("Paused", 1, (255, 0, 0))
textpos = text.get_rect(centerx=width/2,centery = height/2)
def pause():
        while mario.paused == True:
            screen.fill(black)
            screen.blit(text,textpos)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if mario.paused ==False:
                            mario.paused = True
                        if mario.paused == True:
                            main()
                            

    
# Main program here
def main():
    while condition:
        screen.fill((95, 183, 229))
        clock.tick(60)
        screen.fill((95, 183, 229))     # time and screen               
        focusx = mario.x                 #make focal point
        focusy = mario.y
        focus = mariomap.set_focus(focusx,focusy)
        center_viewpoint_x = mariomap.restricted_fx    # set focus tile            center_viewpoint_x = mariomap.restricted_fx
        center_viewpoint_y = mariomap.restricted_fy
        mariomap.draw(screen)    
        Turtle.centerx = center_viewpoint_x
        Turtle.centery = center_viewpoint_y
        Mario.centerx = center_viewpoint_x
        Mario.centery = center_viewpoint_y
        turtles.update()
        marios.update()
        pause()
        for turtle in pygame.sprite.spritecollide(mario,turtles,True):
         mario.short_jump()
        all.draw(screen)
        pygame.display.flip()               # update screen
    pygame.quit()
    quit()
main()
        
        
    
                                
