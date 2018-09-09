import pygame
import sys
import tmx
class Mario(pygame.sprite.Sprite):
    objects =[]
    oblay = []
    condition = True 
    containers = {}
    centerx = 0
    centery = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,Mario.containers)
        stand = pygame.image.load("stand.png").convert_alpha()
        self.mariow = stand.get_width()
        self.marioh = stand.get_height()
        run = pygame.image.load("run0.png").convert_alpha()
        jump = pygame.image.load("jump.png").convert_alpha()
        run = pygame.transform.scale(run,(self.mariow,self.marioh))
        run1 = pygame.transform.flip(run,True,False)
        stand1 = pygame.transform.flip(stand,True,False)
        jump = pygame.transform.scale(jump,(self.mariow,self.marioh))
        self.state = [stand,run,stand1,run1,jump]
        self.rect = stand.get_rect()
        self.a  = 0
        self.b = 0
        self.g = 0.4
        self.x = 0
        self.y = 0
        self.interval = 0
        self.move = 0
        self.velo = 0
        self.i = 0
        self.tilerect = pygame.Rect(self.x,self.y,self.mariow,self.marioh)
        self.itvspeed = 0
        self.paused = 0
    def action(self):
        self.image = self.state[self.i]
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
    def tilemap_to_screen(q,w,center1,center2): 
        long = q+ 320 - center1
        la = w + 240 - center2
        return long,la                              
    def pause(self):
        while self.paused == True:
            screen.fill(black)
            screen.blit(text,textpos)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = False


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                condition = False                       
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.itvspeed = 2
                    self.move = 5
                if event.key == pygame.K_LEFT:
                    self.itvspeed = -2
                    self.move = -5
                if event.key == pygame.K_UP:
                    self.i = 4
                    self.velo = -9
                if event.key == pygame.K_p:
                    self.paused = True
                    Mario.pause(self)
            if event.type == pygame.KEYUP:
                self.move = 0
                self.itvspeed = 0
                self.interval = 0

        if self.interval == 32 or self.interval ==-32:
            self.interval = 0
        self.interval +=self.itvspeed
        if self.interval >16:
            self.i = 1
        elif self.interval >0:
            self.i = 0
        elif self.interval > -16:
            self.i = 2
        else: self.i = 3                    #objects1 here Eg: brick
       
        self.x = self.x + self.move                                   #Eg: velo =  prevelo + 0.4                                      # x,y + velo + move
        self.y = self.y + self.velo
        self.tilerect.left = self.x
        self.tilerect.top = self.y              #object2 here Eg: 0
        Mario.objects = Mario.oblay.collide(self.tilerect,["pipe","brick","platform","boundaries"])
        self.pos,self.x,self.y,onland= Mario.collision(self.x ,self.y ,self.mariow ,self.marioh , Mario.objects) #x ,y collision direction with  collided objects           #Eg: top, xtop, onland = 1
        self.velo += self.g
        if onland == 1:
            self.velo = 0
        print(self.velo)
        self.a, self.b = Mario.tilemap_to_screen(self.x,self.y,Mario.centerx,Mario.centery)
        self.rect = pygame.Rect(self.a,self.b,self.mariow,self.marioh)
        Mario.action(self)
        print("v: ",self.velo)
    def mask(self):
        mask = []
        for x in range(self.mariow):
            mask.append([])
            for y in range (self.marioh):
                mask[x].append(bool(self.image.get_at((x,y))[3]))
        return mask
    def short_jump(self):
        self.velo = -5
        
        
