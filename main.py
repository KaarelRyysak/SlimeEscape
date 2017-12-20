import pygame as pg
import random
from settings import *
from sprites import *
from math import log
import time


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.mixer.pre_init(44100, 16, 2, 5000)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.mängib = True
        self.running = True
        self.looking_right = True
        self.font_name = pg.font.match_font(FONT_NAME)
        pg.mixer.music.load(os.path.join("taustamuusika.mp3"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)

        # spawn new platforms
    def spawn_platforms(self):
        stag = Stage()
        lvl = stag.level.split('\n')[1:]
        x = 0
        y = 0
        for line in lvl:
            for char in line:
                if char == "#":
                    p = Platform(WIDTH+x*40, y*40, 40, 40)
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                #Spawns platform that, when deleted, creates another part of the level
                elif char == "R": 
                    p = Platform(WIDTH+x*40, y*40, 40, 40, True)
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                x += 1
            x = 0
            y += 1

    def spawn_background(self):
            bg = Background(self, WIDTH-0.5, 0)
            self.backgrounds.add(bg)

    def new(self):
        # start a new game
        self.music = True
        self.score = 0
        self.time = time.time()
        self.score_total = 0
        self.all_sprites = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        
        self.platform_move = 0
        self.player_move = 0
        self.bg_move = 0
        
        f = open("options.txt")
        txt = f.readline()
        f.close()
        if int(txt) == 0:
            self.hscore = 0
        elif int(txt) % 81 != 0:
            print("Ära jama mängu failidega!")
            self.playing = False
            self.running = False
        else:
            self.hscore = int(log(int(txt), 81))
        
        for bg in BG_LIST:
            backg = Background(self, bg[0], bg[1])
            self.backgrounds.add(backg)
        
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        for plat in PLATFORM_LIST:
            p = Platform(plat[0], plat[1], plat[2], plat[3])
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.spawn_platforms()
        self.spawn_background()
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
        
        #Turn sprite based on velocity
        if self.looking_right and self.player.vel.x < 0:
            self.player.look_left()
            self.looking_right = False
        elif self.looking_right == False and self.player.vel.x > 0:
            self.player.look_right()
            self.looking_right = True

        if self.player.vel.y != 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #If on on similar height
                if hits[0].rect.top + 10 < self.player.rect.center[1] < hits[0].rect.bottom -10:
                    #If to the left of platform
                    if hits[0].rect.right > self.player.rect.center[0]:
                        self.player_move -= 5
                    else:
                        self.player_move += 5
                    self.player.vel.x = -self.player.vel.x
                #If platform is below player
                elif hits[0].rect.top  > self.player.rect.top -10:
                    self.player.pos.y = hits[0].rect.top + 1
                    self.player.vel.y = 0
                else:
                    self.player.pos.y = hits[0].rect.bottom +26
                    self.player.vel.y = 0

    

                
        # if player reaches right 1/4 of screen
        if self.player.rect.right >= 2*WIDTH / 3:
            self.player_move -= max(abs(self.player.vel.x),2)
            self.platform_move -= max(abs(self.player.vel.x),2)


#Automatic screen scrolling
        if self.player.rect.right < 2*WIDTH/3:
            self.player_move -= 2
            self.platform_move -= 2
     
        
        # Highscore
        time_now = (time.time() - self.time)
        self.score_total = self.score + round(time_now * 15)
        
        # If we die
        if self.player.rect.bottom > HEIGHT:
            f = open("options.txt")
            txt = f.readline()
            f.close() 
            self.score_var = 0
            if txt == '0' or self.score_total > log(int(txt), 81):
                f = open("options.txt", "w")
                self.score_var = self.score_total
                f.write(str(81 ** self.score_total))
                f.close()

            
            self.playing = False
        
        # Moving background
        if self.player.rect.right >= 2*WIDTH/3:
            self.bg_move -= max(abs((self.player.vel.x)/(2)), 2)
        self.bg_move -= 2
        
        #Move platforms
        for plat in self.platforms:
            plat.rect.right += self.platform_move
            if plat.rect.right <= 50:
                plat.rect.top += plat.fall
                plat.fall = plat.fall + 1 * 1.1
                if plat.rect.top > 400:
                    plat.kill()
                if plat.rect.right <= 40:
                    if plat.reset:
                        self.spawn_platforms()
                        self.score += 300
                        plat.reset = False
                
        #Move backgrounds
        for bg in self.backgrounds:
            bg.rect.right += self.bg_move
            if bg.rect.right <= 0:
                bg.kill()
                self.spawn_background()
        #Move player
        self.player.pos.x += self.player_move

        self.platform_move = 0
        self.player_move = 0
        self.bg_move = 0
                


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # Jump
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            # Checks if it's a shortjump event
            if event.type == pg.USEREVENT+1:
                self.player.shortjump()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    if self.mängib:
                        pg.mixer.music.pause()
                        self.mängib = False
                    else:
                        pg.mixer.music.unpause()
                        self.mängib = True


    def draw(self):
        # Game Loop
        self.screen.fill(BLACK)
        self.backgrounds.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score_total), 40, WHITE, WIDTH/2, 15)
        self.draw_text("Highscore: " + str(self.hscore + 1), 20, WHITE, 80, 15)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        intro = True
        self.screen.fill(GREEN)
        active = pg.image.load(os.path.join(img_folder, "active.jpg")).convert()
        notactive = pg.image.load(os.path.join(img_folder, "notactive.jpg")).convert()
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        if self.mängib:
                            pg.mixer.music.pause()
                            self.mängib = False
                        else:
                            pg.mixer.music.unpause()
                            self.mängib = True
        
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            
            if 323+154 > mouse[0] > 323 and 179+47 > mouse[1] > 179:
                self.screen.blit(active, (0,0))
                if click[0] == 1:
                    intro = False
            else:
                self.screen.blit(notactive, (0, 0))
            
            pg.display.update()
            self.clock.tick(15)

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLUE)
        gameover = pg.image.load(os.path.join(img_folder, "gameover.jpg"))
        self.screen.blit(gameover, (0,0))
        if self.score_var > 0:
            self.draw_text("New highscore: " + str(self.score_total), 25, WHITE, WIDTH/2, 20)
        else:
            self.draw_text("Your score: " + str(self.score_total), 25, WHITE, WIDTH/2, 20)
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