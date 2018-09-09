import sys
import pygame
import tmx

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class MarioGame():

    width = 640
    height = 480

    def __init__(self):
        self.pygame = pygame

    def init(self):
        self.pygame.init()
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = self.pygame.time.Clock()
        self.time_step = 0
        # TODO: init sprite, tile,...
        self.tilemap = tmx.load("untitled.tmx", self.screen.get_size())

    def run(self):
        # main game loop
        while True:
            # hold frame rate at 60 fps
            dt = self.clock.tick(60)
            self.time_step += 1
            # enumerate event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # sprite handle event
                self.handle(event)

            self.update(dt / 1000.)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill((95, 183, 229)) # sky color
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Hello World !", 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)
        # TODO: sprite tilemap
        self.tilemap.set_focus(0, 480)
        self.tilemap.draw(screen)
        self.pygame.display.flip()

    def update(self, dt):
        #self.mariosprite.update()
        pass

    def handle(self, event):
        #self.my_mario.handle(event)
        pass
class Mario(pygame.sprite.Sprite):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 19
    PADDING = 1
    img_file = "small_mario.png"
    STAND = 0
    RUNNING = [0, 1]
    JUMP = 3
    index = STAND
    loaded_sprites = {}
    ANIMATION_INTERVAL = 5

    def __init__(self):
        super(Mario, self).__init__()
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.pos = self.rect
        self.v_state = "resting"
        self.h_state = "standing"
        self.facing = "right"

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def update(self, dt, game):
        new = self.rect
        game.tilemap.set_focus(new.x, new.y)

        # change sprite
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            if self.v_state == "jumping":
                self.image = self.set_sprite(self.JUMP)
            else:
                if self.h_state == "running":
                    self.index = (self.index + 1) % len(self.RUNNING)
                    self.image = self.set_sprite(self.index)
                elif self.h_state == "standing":
                    self.image = self.set_sprite(self.STAND)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image, True, False)

    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]
if __name__ == '__main__':
    g = MarioGame()
    g.init()
    g.run()
