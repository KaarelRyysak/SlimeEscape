# Sprite classes for Slime Escape
from settings import *
from random import randint
import pygame as pg
from pygame.locals import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "slime.png")).convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
            # Sets an event that will see if it's a short jump
            pg.time.set_timer(USEREVENT+1, 100)
    
    def shortjump(self):
        if not pg.key.get_pressed()[pg.K_SPACE]:
            self.vel.y = -PLAYER_JUMP*0.35
        # Removes event timer
        pg.time.set_timer(USEREVENT+1, 0)
        
        
        
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        
        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, reset=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.reset = reset



class Background(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "bg.jpg")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Stage layout selection
#It's not a sprite, but it's still related to display...
class Stage:
    def __init__(self):
        levelnum = randint(1, 5)
        if levelnum == 1:
            self.level = """
                 #                  #########################     
                 #           #                                    
                 #     #                                          
                 #                                                
                 #                                                
            #    ### ####                                         
            #          #                  #####                   
           ##                    ####R      #                     
            #                      #        #      #########      
########    ##   ###    #####      #        #        #   #        """
        elif levelnum == 2:
            self.level = """
                                 #                                
                                 #                                
                                 #                                
                                 #     #                          
                    #########    ####  #                          
                     ##          #     #                          
                     ##      #####     R   ######                 
                #  # ##              ###     ##                   
           #  # #  # ####              #     ##      #####        
######  #  #  # #  # ##    # ###########     ##        #      ####"""
        elif levelnum == 3:
            self.level = """
                   ######   #                                     
                   ######   #                                     
                   ######   #              ##                     
                   #        #              #                      
               ## ##  ###  ####           ##                      
                #     ####    #                   #######         
             ###############                         #            
                                   ###R              #            
  #######                  #####    ##               #            
     #       ##  #########   #      ##               #         ###"""
        elif levelnum == 4:
            self.level = """
                                           ##     ##     ##  ##   
                                                  ##     ##  ##   
                                           ##     ##     ##  ##   
                                            #            ##  ##   
                                            #    ###         ##   
                                          ###     ##    ###  ##   
                           ####            ##     ###    ##       
                   ####     ##       #R    ##     ##     #        
          ####      ##   ########    ##    ##     ##     ##   ### 
  ######   ##   #   ##      ##       ##    ##     ##     ###   #  """
        elif levelnum == 5:
            self.level = """
                   #   ###########################################
                   #                                              
                   #                                              
                   #                                    ##        
                   ##                                   ##        
          ##   ##  #           #                       ##         
           #   #   ##          #                       #          
        #  #   #               #          #   #####         #  ## 
   ###  #  #   #        #####  #  ####R   #     #     ###   #   # 
    #   #  #   ##  ##    ###   #    #     #     #      ###  #   # """