import os
# Game Settings
TITLE = "Slime Escape"
WIDTH = 800
HEIGHT = 400
FPS = 60

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.10
PLAYER_GRAV = 0.8
PLAYER_JUMP = 17
FONT_NAME = "arial"

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, 200, 40),
                 (300, HEIGHT - 40, 200, 40),
                 (600, HEIGHT - 40, 200, 40),
                 ]
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Highscore


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")