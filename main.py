import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(plat[0], plat[1], plat[2], plat[3])
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
        

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
                
        # if player reaches right 1/4 of screen
        if self.player.rect.right >= 2*WIDTH / 3:
            self.player.pos.x -= max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.right -= max(abs(self.player.vel.x),2)
                if plat.rect.right <= 0:
                        plat.kill()
                        self.score += 10
        
        # If we die
        if self.player.rect.bottom > HEIGHT:
            f = open("highscore.txt")
            if self.score > int(f.readline()):
                f = open("highscore.txt", "w")
                f.write(str(self.score))
                f.close()
            f.close()
            
            self.playing = False
            
                    
        # spawn new platforms
        while len(self.platforms) < 5:
            width = random.randrange(100, 200)
            p = Platform(WIDTH, HEIGHT-40, width, 40)
            p2 = Platform(WIDTH+300, HEIGHT-200, width, 40)
            self.platforms.add(p)
            self.all_sprites.add(p)
            self.platforms.add(p2)
            self.all_sprites.add(p2)
            
                 

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            # Checks if it's a shortjump event
            if event.type == pg.USEREVENT+1:
                self.player.shortjump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 40, WHITE, WIDTH/2, 15)
        f = open("highscore.txt")
        self.draw_text("Highscore: " + str(f.read()), 25, WHITE, 70, 15)
        f.close()
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move and space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLUE)
        self.draw_text("Game over", 48, WHITE, WIDTH/2, HEIGHT / 4)
        self.draw_text("Your score: " + str(self.score), 25, WHITE, WIDTH/2, 20
                       )
        self.draw_text("Press a key to continue playing", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()
        
    
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
        

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit() 