import pygame
import tmx
import sys
import time
from tmx import TileMap

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
condition = True
pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
black =(0,0,0)
white =(256,256,256)

mariomap = tmx.load("untitled.tmx", screen.get_size())
stand = pygame.image.load("stand.png").convert_alpha()
run = pygame.image.load("run0.png").convert_alpha()
run1 = pygame.image.load("run1.png").convert_alpha()
jump = pygame.image.load("jump.png").convert_alpha()
mario_x =run.get_width()
mario_y =run.get_height()
stand =pygame.transform.scale(stand ,(run.get_width(),run.get_height()))
jump =pygame.transform.scale(jump ,(run.get_width(),run.get_height()))
run1 = pygame.transform.scale(run1,(run.get_width(),run.get_height()))
a = 100
b=100
b_change =0
g = 0.5
s =0
oblay = mariomap.layers["Triggers"]
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
                    x =object.left - xsize 
                    stop = 0
                    col = "left"
                elif min(dislist) ==dis2:
                    x = object.right 
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

class Turtle(pygame.sprite.Sprite):
    containers = {}
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self,Turtle.containers)
       self.image = pygame.image.load("images.png")
       self.image = pygame.transform.scale(self.image,(51,34))
       self.rect =self.image.get_rect()
       self.rect.topleft = 0,100
       self.move = 1
       self.gravity = 0.5
       self.velo = 0
       
    def walk(self):
        self.velo = self.velo+self.gravity
        obstacles = oblay.collide(self.rect,["platforms","pipe"])
        pos , left , top , midair = collision(self.rect.left,self.rect.top,self.rect.width,self.rect.height,obstacles)
        if midair ==0: pass
        else: self.velo = 0
        self.rect =self.rect.move(3,self.velo)
def action(i,x,y):   # mario's action
    if i == 0:
        screen.blit(stand,(x,y))
    if i == 1:
        screen.blit(stand,(x,y))
        pygame.display.update()         
        screen.blit(run,(x,y))
    if i ==2 :
       screen.blit(jump,(x,y))      #running?
       
v=0
a_change = 0 # gravity
turtles = pygame.sprite.Group()
all = pygame.sprite.RenderUpdates()
Turtle.containers = turtles,all
print(Turtle.containers)
turtle = Turtle()
print(turtles)

while condition:
    screen.fill((95, 183, 229))
    clock.tick(60)
    screen.fill((95, 183, 229))     # time and screen               
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Hello World !", 1, (255, 0, 0))
        textpos = text.get_rect(centerx=width/2)
        screen.blit(text, textpos)
    focusx = a                  #make focal point
    focusy = b
    focus = mariomap.set_focus(focusx,focusy)    # set focus tile
    center_viewpoint_x = mariomap.restricted_fx
    center_viewpoint_y = mariomap.restricted_fy
    mariomap.draw(screen)
    xtile  =  center_viewpoint_x + a -320
    ytile =  center_viewpoint_y + b -240
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condtion = False
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                v=1
                a_change = 5
            if event.key == pygame.K_LEFT:          # make mario move
                v =1
                a_change = -5
            if event.key ==pygame.K_UP:
                b_change = -9
        if event.type == pygame.KEYUP:
                if b <440:
                    v =2
                else:
                    v =0
                a_change = 0
    b_change =b_change+g            # apply velocity
    xtile =xtile+ a_change                 # make the move
    ytile= ytile+b_change            
    playerrect =pygame.Rect(xtile,ytile,mario_x,mario_y)
    objects = oblay.collide(playerrect,["brick","platform","pipe","boundaries"])
    pos,xtile,ytile,midair =collision(xtile,ytile,mario_x,mario_y,objects)
    if midair ==0:
        pass
    else:
        b_change = 0
    print(b_change)
    a = xtile +320- center_viewpoint_x
    b =ytile +240 -center_viewpoint_y
    action(v,a,b)                   # show mario
    pygame.display.flip()               # update screen
pygame.quit()
quit()
