import pygame
import pygame.gfxdraw
import random
import math
import time
import cv2
import numpy as np
from enum import Enum, auto
from queue import Queue
import socket
import threading
import pickle
import struct

#|########################################################################|#
#| ABOUT                                                                  |#
#|########################################################################|#

"""
Authors:
- Anderson Pastore Rizzi
- Edurado Eberhardt Pereira

Player information:
- PLAYER 1, SERVER, LEFT
- PLAYER 2, CLIENT, RIGHT
"""

#|########################################################################|#
#| PYGAME INITIAL SETTINGS                                                |#
#|########################################################################|#

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music/background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AirSea-Battle")
clock = pygame.time.Clock()



#|########################################################################|#
#| ENUMERATIONS                                                           |#
#|########################################################################|#

class Language(Enum):
    PT_BR = auto() # Brazilian Portuguese
    EN_US = auto() # American English
    ZH_CN = auto() # Chinese Simplified

class Screen(Enum):
    NO_PAUSE = auto()
    MAIN_MENU = auto()
    LANGUAGE_SCREEN = auto()
    CREDITS_SCREEN = auto()
    SERVER_SCREEN = auto()
    CONNECTION_SCREEN = auto()
    PORT_ERROR_PAUSE_SCREEN = auto()
    CONNECTION_TIME_OUT_PAUSE_SCREEN = auto()
    UNEXPECTED_ERROR_PAUSE_SCREEN = auto()

class UserType(Enum):
    CLIENT = auto()
    SERVER = auto()

class GamePowerUps(Enum):
    NONE = auto()
    UNLIMITED_PROJECTILES = auto()
    DOUBLE_POINTS = auto()

class GameResult(Enum):
    WON = auto()
    LOST = auto()
    TIE = auto()



#|########################################################################|#
#| DEFINITION OF COLORS                                                   |#
#|########################################################################|#

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BLUE_SKY_TOP = (0, 0, 128)
BLUE_SKY_BOTTOM = (135, 206, 235)
GREEN_GRASS_TOP = (34, 139, 34)
GREEN_GRASS_BOTTOM = (38, 173, 38)
BLUE_BUTTON_TOP = (0, 41, 100) 
BLUE_BUTTON_BOTTOM = (0, 64, 150)
BLUE_BUTTON_TOP_HOVER = (0, 41, 69)
BLUE_BUTTON_BOTTOM_HOVER = (0, 64, 108) 

DARK_GRAY_TRANSLUCENT = (50, 50, 50, 150)
DARK_GREEN_TRANSLUCENT = (19, 42, 19, 90)
LIGHT_GRAY_TRANSLUCENT = (200, 200, 200, 128)
BLACK_TRANSLUCENT = (0, 0, 0, 60)
TRANSPARENT = (0, 0, 0, 0)



#|########################################################################|#
#| DEFINITION OF FONTS                                                    |#
#|########################################################################|#

latin_font_path = 'font/NotoSans-SemiBold.ttf'
simplified_chinese_font_path = 'font/NotoSansSC-SemiBold.ttf'

SMALL_FONT_SIZE = 18
DEFAULT_FONT_SIZE = 26
MEDIUM_FONT_SIZE = 46
LARGE_FONT_SIZE = 64

latin_small_font = pygame.font.Font(latin_font_path, SMALL_FONT_SIZE)
latin_default_font = pygame.font.Font(latin_font_path, DEFAULT_FONT_SIZE)
latin_medium_font = pygame.font.Font(latin_font_path, MEDIUM_FONT_SIZE)
latin_large_font = pygame.font.Font(latin_font_path, LARGE_FONT_SIZE)

simplified_chinese_small_font = pygame.font.Font(simplified_chinese_font_path, SMALL_FONT_SIZE)
simplified_chinese_default_font = pygame.font.Font(simplified_chinese_font_path, DEFAULT_FONT_SIZE)
simplified_chinese_medium_font = pygame.font.Font(simplified_chinese_font_path, MEDIUM_FONT_SIZE)
simplified_chinese_large_font = pygame.font.Font(simplified_chinese_font_path, LARGE_FONT_SIZE)

CURRENT_SMALL_FONT = latin_small_font
CURRENT_DEFAULT_FONT = latin_default_font
CURRENT_MEDIUM_FONT = latin_medium_font
CURRENT_LARGE_FONT = latin_large_font



#|########################################################################|#
#| CONNECTION SETTINGS                                                    |#
#|########################################################################|#

CLIENT_CONNECTION_TIMEOUT = 7  # In seconds.
SERVER_CONNECTION_TIMEOUT = 15 # In seconds.



#|########################################################################|#
#| STYLE SETTINGS                                                         |#
#|########################################################################|#

MARGIN_TOP_GAME = 80  # Distance between the top of the screen and the planes.
MARGIN_BOTTOM_GAME = 20 # Distance between the bottom of the screen and the cannons.
MARGIN_TOP_SCORE = 40
MARGIN_SIDE_SCORE = 50
MARGIN_TEXTBOX_LABEL = 30 # Distance between a text box and its label.
BUTTON_HEIGHT = 50
MARGIN_BOTTOM_BUTTON = 20



#|########################################################################|#
#| GAMEPLAY SETTINGS                                                      |#
#|########################################################################|#

FPS = 30
CANNON_WIDTH = 75
CANNON_HEIGHT = 75
CANNON_Y = SCREEN_HEIGHT - CANNON_HEIGHT - MARGIN_BOTTOM_GAME
CANNON_MAX_QUANTITY_OF_AMMUNITION = 5
CANNON_ANGLES = [30, 60, 90, 120, 150] # In degrees.
AIRPLANE_WIDTH = 51
AIRPLANE_HEIGHT = 25
AIRPLANE_SPEED = 4
PROJECTILE_RADIUS = 5
PROJECTILE_SPEED = 7
MATCH_TIME = 30000 # In milliseconds (30 sec).
POWER_UP_TIME = 300 # In number of frames.
CURRENT_LANGUAGE = Language.EN_US
FADING_MUSIC = False
MUSIC_ON = True
player_2_key_list = Queue()



#|########################################################################|#
#| TEXTS                                                                  |#
#|########################################################################|#

TEXT_MAIN_MENU_CREATE_SERVER_BUTTON = ""
TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON = ""
TEXT_MAIN_MENU_QUIT_BUTTON = ""
TEXT_SERVER_MENU_CREATE_BUTTON = ""
TEXT_CONNECT_MENU_CONNECT_BUTTON = ""
TEXT_CREDITS_SCREEN_TOP = ""
TEXT_LANGUAGE_MENU_TOP = ""
TEXT_SERVER_MENU_TOP = ""
TEXT_CONNECT_MENU_TOP = ""
TEXT_SERVER_MENU_TOP = ""
TEXT_PORT = ""
TEXT_CONNECTION_TIME_OUT = ""
TEXT_WAITING_CONNECTION = ""
TEXT_CONNECTING_SERVER = ""
TEXT_UNEXPECTED_ERROR = ""
TEXT_MATCH_WON = ""
TEXT_MATCH_LOST = ""
TEXT_MATCH_TIE = ""
TEXT_PORT_ERROR = ""
TEXT_CREDITS_SCREEN_DEVELOPERS = ""
TEXT_CREDITS_SCREEN_MUSIC = ""
TEXT_CREDITS_SCREEN_IMAGES = ""



#|########################################################################|#
#| IMAGES                                                                 |#
#|########################################################################|#

GRAY_CANNON_IMAGES = [
    pygame.transform.smoothscale(pygame.image.load('img/cannon_30_deg_gray.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_60_deg_gray.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_90_deg_gray.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_120_deg_gray.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_150_deg_gray.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
]

RED_CANNON_IMAGES = [
    pygame.transform.smoothscale(pygame.image.load('img/cannon_30_deg_red.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_60_deg_red.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_90_deg_red.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_120_deg_red.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_150_deg_red.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
]

YELLOW_CANNON_IMAGES = [
    pygame.transform.smoothscale(pygame.image.load('img/cannon_30_deg_yellow.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_60_deg_yellow.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_90_deg_yellow.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_120_deg_yellow.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
    pygame.transform.smoothscale(pygame.image.load('img/cannon_150_deg_yellow.png').convert_alpha(), (CANNON_WIDTH, CANNON_HEIGHT)),
]



#|########################################################################|#
#| CLASSES                                                                |#
#|########################################################################|#

#|////////////////////////////////////////////////////////////////////////|#
# This class represents the buttons with text in the menus.
#|////////////////////////////////////////////////////////////////////////|#
class TextButton:
    def __init__(self, text, x, y, w, h, color1, color2, hover_color1, hover_color2, font=latin_default_font, border_radius=10):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color1 = color1
        self.color2 = color2
        self.hover_color1 = hover_color1
        self.hover_color2 = hover_color2
        self.border_radius = border_radius
        self.font = font
        self.hovering = False

    def draw(self, screen):
        color1, color2 = (self.hover_color1, self.hover_color2) if self.hovering else (self.color1, self.color2)

        # Creates a temporary surface with transparency.
        gradient_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Fills the surface with a gradient.
        for i in range(self.rect.height):
            ratio = i / self.rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, i), (self.rect.width, i))

        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height), border_radius=self.border_radius)
        button_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(button_surface, self.rect.topleft)

        # Draws text in the center of the button.
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


#|////////////////////////////////////////////////////////////////////////|#
# This class represents the buttons with images in the menus.
#|////////////////////////////////////////////////////////////////////////|#
class ImageButton:
    def __init__(self, x, y, w, h, background_color, background_color_hover, padding, image_path, border_radius=10):
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(original_image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.background_color = background_color
        self.background_color_hover = background_color_hover
        self.border_radius = border_radius
        self.padding = padding

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        inflated_rect = self.rect.inflate(self.padding * 2, self.padding * 2)

        if inflated_rect.collidepoint(mouse_pos):
            bg_color = self.background_color_hover
        else:
            bg_color = self.background_color

        temp_surface = pygame.Surface((inflated_rect.width, inflated_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, bg_color, temp_surface.get_rect(), border_radius=self.border_radius)
        antialiased_surface = pygame.transform.smoothscale(temp_surface, (inflated_rect.width * 2, inflated_rect.height * 2))
        antialiased_surface = pygame.transform.smoothscale(antialiased_surface, (inflated_rect.width, inflated_rect.height))
        surface.blit(antialiased_surface, inflated_rect.topleft)
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        inflated_rect = self.rect.inflate(self.padding * 2, self.padding * 2)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if inflated_rect.collidepoint(event.pos):
                return True
        return False


#|////////////////////////////////////////////////////////////////////////|#
# This class represents the menu text boxes.
#|////////////////////////////////////////////////////////////////////////|#
class TextBox:
    def __init__(self, x, y, w, h, text='', border_radius=10, font=CURRENT_DEFAULT_FONT, max_chars=None, enabled=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY_TRANSLUCENT
        self.border_color = WHITE
        self.text = text if text else ''
        self.txt_surface = font.render(self.text, True, BLACK)
        self.active = False
        self.border_radius = border_radius
        self.cursor_visible = True
        self.cursor_timer = 0 
        self.max_chars = max_chars
        self.enabled = enabled
        self.font = font

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.max_chars is None or len(self.text) < self.max_chars:
                        self.text += event.unicode
                
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        textbox_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(textbox_surface, self.color, (0, 0, self.rect.width, self.rect.height), border_radius=self.border_radius)
        screen.blit(textbox_surface, self.rect.topleft)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=self.border_radius)

        # Draws the text of the text box.
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect.topleft)

        # Draws the typing cursor.
        if self.active:
            cursor_x = text_rect.x + self.txt_surface.get_width() + 3  # 3 pixel margin
            cursor_y = self.rect.centery - self.txt_surface.get_height() // 2
            if self.cursor_visible:
                pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + self.rect.height // 2), 2)  # Cursor

    def update(self, dt):
        if not self.enabled:
            return

        # Updates the cursor timer.
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Every 500 ms, toggle visibility.
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self.active = False
    

#|////////////////////////////////////////////////////////////////////////|#
# This class represents the cannons in the game.
#|////////////////////////////////////////////////////////////////////////|#
class Cannon(pygame.sprite.Sprite):
    def __init__(self, x, side):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.angle = 90
        self.side = side
        self.max_ammo = CANNON_MAX_QUANTITY_OF_AMMUNITION
        self.current_ammo = CANNON_MAX_QUANTITY_OF_AMMUNITION
        self.current_buff = GamePowerUps.NONE
        self.buff_timer = 0

        for i, angle in enumerate(CANNON_ANGLES):
                if self.angle == 90:
                    self.image = GRAY_CANNON_IMAGES[i]

        # Defines the positioning rectangle.
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = CANNON_Y
        self.rect = self.image.get_rect(center=(self.x, CANNON_Y))

    def draw(self):
        # Changes the cannon image depending on the currently active power up.
        if self.current_buff == GamePowerUps.NONE:
            for i, angle in enumerate(CANNON_ANGLES):
                if self.angle == angle:
                    self.image = GRAY_CANNON_IMAGES[i]

        elif self.current_buff == GamePowerUps.UNLIMITED_PROJECTILES:
            for i, angle in enumerate(CANNON_ANGLES):
                if self.angle == angle:
                    self.image = YELLOW_CANNON_IMAGES[i]
            self.buff_timer -= 1

        elif self.current_buff == GamePowerUps.DOUBLE_POINTS:
            for i, angle in enumerate(CANNON_ANGLES):
                if self.angle == angle:
                    self.image = RED_CANNON_IMAGES[i]
            self.buff_timer -= 1

        if self.buff_timer <= 0:
            self.current_buff = GamePowerUps.NONE

        # Draw the cannon on the screen.
        self.rect.x = self.x
        self.rect.y = CANNON_Y
        screen.blit(self.image, self.rect)

        # Draws the ammo quantity bar.
        bar_width = CANNON_WIDTH
        bar_height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y + CANNON_HEIGHT + 8  # Positions the bar just below the cannon.
        if self.current_buff == GamePowerUps.UNLIMITED_PROJECTILES:
            ammo_percentage = 1
        else:
            ammo_percentage = self.current_ammo / self.max_ammo
        ammo_bar_width = bar_width * ammo_percentage
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, ammo_bar_width, bar_height))
    
    def to_dict(self):
        return {
            'x': int(self.x),
            'angle': int(self.angle),
            'side': self.side,
            'max_ammo': int(self.max_ammo),
            'current_ammo': int(self.current_ammo),
            'current_buff': self.current_buff
        }
    
    def update_from_dict(self, data):        
        self.x = data['x']
        self.angle = data['angle']
        self.side = data['side']
        self.max_ammo = data['max_ammo']
        self.current_ammo = data['current_ammo']
        self.current_buff = data['current_buff'] 


#|////////////////////////////////////////////////////////////////////////|#
# This class represents the planes in the game.
#|////////////////////////////////////////////////////////////////////////|#
class Airplane:
    def __init__(self, x, y, direction, buff):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.direction = direction
        self.buff = buff

    def update(self):
        self.x += self.direction * AIRPLANE_SPEED

    def draw(self):
        if self.buff == GamePowerUps.NONE:
            self.image = pygame.transform.smoothscale(pygame.image.load('img/plane_green.png').convert_alpha(), (AIRPLANE_WIDTH, AIRPLANE_HEIGHT))
        elif self.buff == GamePowerUps.UNLIMITED_PROJECTILES:
            self.image = pygame.transform.smoothscale(pygame.image.load('img/plane_yellow.png').convert_alpha(), (AIRPLANE_WIDTH, AIRPLANE_HEIGHT))
        elif self.buff == GamePowerUps.DOUBLE_POINTS:
            self.image = pygame.transform.smoothscale(pygame.image.load('img/plane_red.png').convert_alpha(), (AIRPLANE_WIDTH, AIRPLANE_HEIGHT))
        
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y

        screen.blit(self.image, self.rect)
    
    def to_dict(self):
        return {
            'x': int(self.x),
            'y': int(self.y),
            'direction': int(self.direction),
            'buff': self.buff
        }


#|////////////////////////////////////////////////////////////////////////|#
# This class represents the projectiles of a cannon.
#|////////////////////////////////////////////////////////////////////////|#
class Projectile:
    def __init__(self, x, y, angle, side):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.speed_x = PROJECTILE_SPEED * math.cos(self.angle)
        self.speed_y = -PROJECTILE_SPEED * math.sin(self.angle)
        self.side = side

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), PROJECTILE_RADIUS)



#|########################################################################|#
#| GENERAL FUNCTIONS                                                      |#
#|########################################################################|#

#|////////////////////////////////////////////////////////////////////////|#
# This function draws the sky with gradient (with linear interpolation).
#|////////////////////////////////////////////////////////////////////////|#
def draw_sky():
    for y in range(SCREEN_HEIGHT):
        r = BLUE_SKY_TOP[0] + (BLUE_SKY_BOTTOM[0] - BLUE_SKY_TOP[0]) * y // SCREEN_HEIGHT
        g = BLUE_SKY_TOP[1] + (BLUE_SKY_BOTTOM[1] - BLUE_SKY_TOP[1]) * y // SCREEN_HEIGHT
        b = BLUE_SKY_TOP[2] + (BLUE_SKY_BOTTOM[2] - BLUE_SKY_TOP[2]) * y // SCREEN_HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


#|////////////////////////////////////////////////////////////////////////|#
# This function draws grass with gradient (with linear interpolation).
#|////////////////////////////////////////////////////////////////////////|#
def draw_grass():
    grass_height = 100
    for y in range(SCREEN_HEIGHT - grass_height, SCREEN_HEIGHT):
        r = GREEN_GRASS_TOP[0] + (GREEN_GRASS_BOTTOM[0] - GREEN_GRASS_TOP[0]) * (y - (SCREEN_HEIGHT - grass_height)) // grass_height
        g = GREEN_GRASS_TOP[1] + (GREEN_GRASS_BOTTOM[1] - GREEN_GRASS_TOP[1]) * (y - (SCREEN_HEIGHT - grass_height)) // grass_height
        b = GREEN_GRASS_TOP[2] + (GREEN_GRASS_BOTTOM[2] - GREEN_GRASS_TOP[2]) * (y - (SCREEN_HEIGHT - grass_height)) // grass_height
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


#|////////////////////////////////////////////////////////////////////////|#
# This function gets the user's IP address.
#|////////////////////////////////////////////////////////////////////////|#
def get_ip_address(interface=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connects to Google's DNS server.
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return ""


#|////////////////////////////////////////////////////////////////////////|#
# This function calculates the X coordinate to center objects based on the 
# screen width, the width of each object, and a given spacing.
#|////////////////////////////////////////////////////////////////////////|#
def get_centered_x(num_objects, object_width, spacing):
    total_width = num_objects * object_width + (num_objects - 1) * spacing
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    positions_x = []
    for i in range(num_objects):
        positions_x.append(start_x + i * (object_width + spacing))
    
    return positions_x


#|////////////////////////////////////////////////////////////////////////|#
# This function draws centered text and leaves the background blurred.
#|////////////////////////////////////////////////////////////////////////|#
def draw_centered_text_with_blur(screen, text, font, blur_radius=15):
    screen_snapshot = pygame.surfarray.array3d(screen)
    screen_snapshot = np.transpose(screen_snapshot, (1, 0, 2))
    blurred_snapshot = cv2.GaussianBlur(screen_snapshot, (blur_radius, blur_radius), 0)
    blurred_surface = pygame.surfarray.make_surface(np.transpose(blurred_snapshot, (1, 0, 2)))
    screen.blit(blurred_surface, (0, 0))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 180))
    screen.blit(overlay, (0, 0))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


#|////////////////////////////////////////////////////////////////////////|#
# This function draws the players' scores.
#|////////////////////////////////////////////////////////////////////////|#
def draw_scores(p1_score, p2_score, font):
    left_text = font.render(str(p1_score), True, WHITE)
    right_text = font.render(str(p2_score), True, WHITE)
    screen.blit(left_text, (MARGIN_SIDE_SCORE, MARGIN_TOP_SCORE))
    right_text_rect = right_text.get_rect()
    right_text_rect.right = SCREEN_WIDTH - MARGIN_SIDE_SCORE
    right_text_rect.top = MARGIN_TOP_SCORE
    screen.blit(right_text, right_text_rect)


#|////////////////////////////////////////////////////////////////////////|#
# This function draws the remaining time of the match in the top center.
#|////////////////////////////////////////////////////////////////////////|#
def draw_remaining_time(screen, time_remaining_ms, font):
    seconds = time_remaining_ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    time_string = f"{minutes:02}:{seconds:02}"  # MM:SS format
    text_surface = font.render(time_string, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, MARGIN_TOP_SCORE))
    text_rect.top = MARGIN_TOP_SCORE
    screen.blit(text_surface, text_rect)


#|////////////////////////////////////////////////////////////////////////|#
# This function creates a new group of planes.
#|////////////////////////////////////////////////////////////////////////|#
def create_airplanes(direction):
    num_airplanes = random.randint(3, 5)

    if direction == 1:
        updated_direction = -1
        start_x = 0
    else:
        updated_direction = 1
        start_x = SCREEN_WIDTH - AIRPLANE_WIDTH

    airplanes = []
    squadron_y = random.randint(0,20)

    for i in range(num_airplanes):
        buffed = random.randint(0,100)
        if buffed > 70:
            buff = random.randint(0,1)
            if buff == 0:
                buff = GamePowerUps.UNLIMITED_PROJECTILES
            else:
                buff = GamePowerUps.DOUBLE_POINTS
        else:
            buff = GamePowerUps.NONE
        airplanes.append(Airplane(start_x + (direction * random.randint(0,50)), MARGIN_TOP_GAME + squadron_y + i * (AIRPLANE_HEIGHT + 20), direction, buff))
    return airplanes, updated_direction


#|////////////////////////////////////////////////////////////////////////|#
# This function receives data from a client connected to the server.
#|////////////////////////////////////////////////////////////////////////|#
def receive_data_from_network(network_socket):
    network_socket.settimeout(CLIENT_CONNECTION_TIMEOUT)
    while True:
        try:
            # Receives the length of the data.
            data_len_bytes = network_socket.recv(4)

            # Connection closed by server.
            if not data_len_bytes:
                break

            # Convert bytes to integer.
            data_len = struct.unpack('>I', data_len_bytes)[0]  

            # Receives data with known length.
            data = b''
            while len(data) < data_len:
                more_data = network_socket.recv(data_len - len(data))

                # Connection closed by the server while receiving data.
                if not more_data:
                    break
                data += more_data

            # Deserialize the data and put it in the queue that will be read by the game server.
            if data:
                fila_recebida = pickle.loads(data)
                for item in fila_recebida:
                    player_2_key_list.put(item)
    
        except socket.timeout:
            continue

        except Exception as e:
            break


#|////////////////////////////////////////////////////////////////////////|#
# This function gradually reduces the music volume to zero until it pauses.
#|////////////////////////////////////////////////////////////////////////|#
def fade_out_music(duration):
    global FADING_MUSIC
    FADING_MUSIC = True
    current_volume = pygame.mixer.music.get_volume()
    steps = 50
    step_duration = duration / steps
    
    for i in range(steps):
        current_volume -= 1.0 / steps
        pygame.mixer.music.set_volume(max(0, current_volume))
        time.sleep(step_duration) 

    pygame.mixer.music.pause()
    FADING_MUSIC = False


#|////////////////////////////////////////////////////////////////////////|#
# This function gradually increases the music volume from 0 to the 
# original volume.
#|////////////////////////////////////////////////////////////////////////|#
def fade_in_music(duration):
    global FADING_MUSIC
    FADING_MUSIC = True
    pygame.mixer.music.unpause()
    current_volume = pygame.mixer.music.get_volume()
    steps = 50 
    step_duration = duration / steps

    for i in range(steps):
        current_volume += 1.0 / steps
        pygame.mixer.music.set_volume(min(1.0, current_volume))
        time.sleep(step_duration)
    
    FADING_MUSIC = False


#|////////////////////////////////////////////////////////////////////////|#
# This function creates a Thread to start the music fade out.
#|////////////////////////////////////////////////////////////////////////|#
def start_fade_in(duration):
    threading.Thread(target=fade_in_music, args=(duration,)).start()


#|////////////////////////////////////////////////////////////////////////|#
# This function creates a Thread to start the music fade in.
#|////////////////////////////////////////////////////////////////////////|#
def start_fade_out(duration):
    threading.Thread(target=fade_out_music, args=(duration,)).start()


#|////////////////////////////////////////////////////////////////////////|#
# This function changes the game language.
#|////////////////////////////////////////////////////////////////////////|#
def change_language(new_language):
    global CURRENT_LANGUAGE
    global CURRENT_SMALL_FONT
    global CURRENT_DEFAULT_FONT
    global CURRENT_MEDIUM_FONT
    global CURRENT_LARGE_FONT

    global TEXT_MAIN_MENU_CREATE_SERVER_BUTTON
    global TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON
    global TEXT_MAIN_MENU_QUIT_BUTTON
    global TEXT_SERVER_MENU_CREATE_BUTTON
    global TEXT_CONNECT_MENU_CONNECT_BUTTON
    global TEXT_CREDITS_SCREEN_TOP
    global TEXT_LANGUAGE_MENU_TOP
    global TEXT_CONNECT_MENU_TOP
    global TEXT_SERVER_MENU_TOP
    global TEXT_PORT
    global TEXT_CONNECTION_TIME_OUT
    global TEXT_WAITING_CONNECTION
    global TEXT_CONNECTING_SERVER
    global TEXT_UNEXPECTED_ERROR
    global TEXT_MATCH_WON
    global TEXT_MATCH_LOST
    global TEXT_MATCH_TIE
    global TEXT_PORT_ERROR
    global TEXT_CREDITS_SCREEN_DEVELOPERS
    global TEXT_CREDITS_SCREEN_MUSIC
    global TEXT_CREDITS_SCREEN_IMAGES
    
    CURRENT_LANGUAGE = new_language

    if CURRENT_LANGUAGE == Language.EN_US:
        CURRENT_SMALL_FONT = latin_small_font
        CURRENT_DEFAULT_FONT = latin_default_font
        CURRENT_MEDIUM_FONT = latin_medium_font
        CURRENT_LARGE_FONT = latin_large_font

        TEXT_MAIN_MENU_CREATE_SERVER_BUTTON = "Create a server"
        TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON = "Connect to a server"
        TEXT_MAIN_MENU_QUIT_BUTTON = "Exit the game"
        TEXT_SERVER_MENU_CREATE_BUTTON = "Create"
        TEXT_CONNECT_MENU_CONNECT_BUTTON = "Connect"
        TEXT_LANGUAGE_MENU_TOP = "Select language"
        TEXT_CONNECT_MENU_TOP = "Connecting to a server"
        TEXT_SERVER_MENU_TOP = "Creating a server"
        TEXT_PORT = "PORT"
        TEXT_CONNECTION_TIME_OUT = "No connection established within timeout."
        TEXT_WAITING_CONNECTION = "Waiting for another user to connect to start the game."
        TEXT_CONNECTING_SERVER = "Please wait while the connection is established."
        TEXT_UNEXPECTED_ERROR = "An unexpected error has occurred and you will be redirected to the main menu." 
        TEXT_MATCH_WON = "Congratulations, you won!"
        TEXT_MATCH_LOST = "You lost."
        TEXT_MATCH_TIE = "The game is tied."
        TEXT_PORT_ERROR = "The port number must be between 0 and 65535."
        TEXT_CREDITS_SCREEN_TOP = "Credits"
        TEXT_CREDITS_SCREEN_DEVELOPERS = "Developers:"
        TEXT_CREDITS_SCREEN_MUSIC = "Music:"
        TEXT_CREDITS_SCREEN_IMAGES = "Images:"


    elif CURRENT_LANGUAGE == Language.PT_BR:
        CURRENT_SMALL_FONT = latin_small_font
        CURRENT_DEFAULT_FONT = latin_default_font
        CURRENT_MEDIUM_FONT = latin_medium_font
        CURRENT_LARGE_FONT = latin_large_font

        TEXT_MAIN_MENU_CREATE_SERVER_BUTTON = "Criar um servidor"
        TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON = "Conectar-se a um servidor"
        TEXT_MAIN_MENU_QUIT_BUTTON = "Sair do jogo"
        TEXT_SERVER_MENU_CREATE_BUTTON = "Criar"
        TEXT_CONNECT_MENU_CONNECT_BUTTON = "Conectar"
        TEXT_LANGUAGE_MENU_TOP = "Selecione o idioma"
        TEXT_CONNECT_MENU_TOP = "Conectando-se a um servidor"
        TEXT_SERVER_MENU_TOP = "Criando um servidor"
        TEXT_PORT = "PORTA"
        TEXT_CONNECTION_TIME_OUT = "Nenhuma conexão estabelecida dentro do tempo limite."
        TEXT_WAITING_CONNECTION = "Aguardando a conexão de outro usuário para iniciar a partida."
        TEXT_CONNECTING_SERVER = "Aguarde enquanto a conexão é estabelecida."
        TEXT_UNEXPECTED_ERROR = "Um erro inesperado aconteceu e você será redirecionado ao menu principal." 
        TEXT_MATCH_WON = "Parabéns, você venceu!"
        TEXT_MATCH_LOST = "Você perdeu."
        TEXT_MATCH_TIE = "O jogo empatou."
        TEXT_PORT_ERROR = "O número da porta deve estar entre 0 e 65535."
        TEXT_CREDITS_SCREEN_TOP = "Créditos"
        TEXT_CREDITS_SCREEN_DEVELOPERS = "Desenvolvedores:"
        TEXT_CREDITS_SCREEN_MUSIC = "Música:"
        TEXT_CREDITS_SCREEN_IMAGES = "Imagens:"


    elif CURRENT_LANGUAGE == Language.ZH_CN:
        CURRENT_SMALL_FONT = simplified_chinese_small_font
        CURRENT_DEFAULT_FONT = simplified_chinese_default_font
        CURRENT_MEDIUM_FONT = simplified_chinese_medium_font
        CURRENT_LARGE_FONT = simplified_chinese_large_font

        TEXT_MAIN_MENU_CREATE_SERVER_BUTTON = "创建服务器"
        TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON = "连接到服务器"
        TEXT_MAIN_MENU_QUIT_BUTTON = "退出游戏"
        TEXT_SERVER_MENU_CREATE_BUTTON = "创造"
        TEXT_CONNECT_MENU_CONNECT_BUTTON = "连接"
        TEXT_LANGUAGE_MENU_TOP = "选择语言"
        TEXT_CONNECT_MENU_TOP = "连接到服务器"
        TEXT_SERVER_MENU_TOP = "创建服务器"
        TEXT_PORT = "端口"
        TEXT_CONNECTION_TIME_OUT = "超时内未建立连接。"
        TEXT_WAITING_CONNECTION = "等待另一个用户连接以开始游戏。"
        TEXT_CONNECTING_SERVER = "请等待连接建立。"
        TEXT_UNEXPECTED_ERROR = "发生了意外错误，您将被重定向到主菜单。" 
        TEXT_MATCH_WON = "恭喜你，你中奖了！"
        TEXT_MATCH_LOST = "你錯了。"
        TEXT_MATCH_TIE = "比赛打平。"
        TEXT_PORT_ERROR = "端口号必须介于 0 至 65535 之间。"
        TEXT_CREDITS_SCREEN_TOP = "致谢"
        TEXT_CREDITS_SCREEN_DEVELOPERS = "开发人员："
        TEXT_CREDITS_SCREEN_MUSIC = "音乐："
        TEXT_CREDITS_SCREEN_IMAGES = "图片："



#|########################################################################|#
#| MAIN MENU FUNCTION                                                     |#
#|########################################################################|#

def main_menu():
    # Sets the initial language to English (US).
    global CURRENT_LANGUAGE
    change_language(Language.EN_US)

    # Define control variables.
    current_screen = Screen.MAIN_MENU
    current_pause_screen = Screen.NO_PAUSE
    pause_remaining_time = 0 # In frames.
    global FADING_MUSIC
    global MUSIC_ON

    MUSIC_ON = True

    # Creating text boxes.
    ip_text_box_for_server_creation = TextBox(get_centered_x(1, 250, 0)[0], 220, 250, 50, get_ip_address(), border_radius = 7, enabled = True)
    ip_text_box_for_server_connection = TextBox(get_centered_x(1, 250, 0)[0], 220, 250, 50, border_radius = 7, max_chars = 15)
    port_text_box = TextBox(get_centered_x(1, 250, 0)[0], 320, 250, 50, border_radius = 7, max_chars = 5)

    # Declaration of buttons.
    create_button = None
    connect_button = None
    quit_button = None
    create_server_button = None
    connect_button_submit = None
    
    back_button = ImageButton(
        10, 
        10, 
        50, 
        50, 
        TRANSPARENT, 
        BLACK_TRANSLUCENT, 
        -2, 
        'img/arrow_back.png', 
        border_radius = 7
    )


    # Creation of the lower buttons.
    size_bottom_buttons = 46
    x_bottom_buttons = get_centered_x(3, size_bottom_buttons, 25)

    language_button = ImageButton(
        x_bottom_buttons[0], 
        528, 
        size_bottom_buttons, 
        size_bottom_buttons, 
        DARK_GREEN_TRANSLUCENT, 
        DARK_GRAY_TRANSLUCENT, 
        3, 
        'img/language_icon.png', 
        border_radius = 7
    )

    music_button = ImageButton(
        x_bottom_buttons[1], 
        528, 
        size_bottom_buttons,
        size_bottom_buttons,
        DARK_GREEN_TRANSLUCENT, 
        DARK_GRAY_TRANSLUCENT, 
        3, 
        'img/music_on_icon.png', 
        border_radius = 7
    )

    credits_button = ImageButton(
        x_bottom_buttons[2], 
        528, 
        size_bottom_buttons, 
        size_bottom_buttons, 
        DARK_GREEN_TRANSLUCENT, 
        DARK_GRAY_TRANSLUCENT, 
        3, 
        'img/credits_icon.png', 
        border_radius = 7
    )
    

    # Creation of language selection buttons.
    en_us_button = TextButton(
        "English (US)",
        get_centered_x(1, 350, 0)[0],
        200,
        350,
        BUTTON_HEIGHT,
        BLUE_BUTTON_TOP,
        BLUE_BUTTON_BOTTOM,
        BLUE_BUTTON_TOP_HOVER,
        BLUE_BUTTON_BOTTOM_HOVER,
        font = latin_default_font,
        border_radius=7
    )

    pt_br_button = TextButton(
        "Português (BR)",
        get_centered_x(1, 350, 0)[0],
        en_us_button.rect.top + en_us_button.rect.h + MARGIN_BOTTOM_BUTTON,
        350,
        BUTTON_HEIGHT,
        BLUE_BUTTON_TOP,
        BLUE_BUTTON_BOTTOM,
        BLUE_BUTTON_TOP_HOVER,
        BLUE_BUTTON_BOTTOM_HOVER,
        font = latin_default_font,
        border_radius=7
    )

    zh_cn_button = TextButton(
        "简体中文",
        get_centered_x(1, 350, 0)[0],
        pt_br_button.rect.top + pt_br_button.rect.h + MARGIN_BOTTOM_BUTTON,
        350,
        BUTTON_HEIGHT,
        BLUE_BUTTON_TOP,
        BLUE_BUTTON_BOTTOM,
        BLUE_BUTTON_TOP_HOVER,
        BLUE_BUTTON_BOTTOM_HOVER,
        font = simplified_chinese_default_font,
        border_radius = 7
    )


    # Main menu execution loop.
    running = True
    while running:
        dt = clock.tick(FPS)
        
        # Draw the background.
        draw_sky()
        draw_grass()
        
        # Displays the main menu home screen.
        if current_screen == Screen.MAIN_MENU:
            title_surface = latin_large_font.render("AirSea-Battle", True, WHITE)
            screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 80))

            create_button = TextButton(
                TEXT_MAIN_MENU_CREATE_SERVER_BUTTON, 
                get_centered_x(1, 350, 0)[0], 
                200, 
                350, 
                BUTTON_HEIGHT, 
                BLUE_BUTTON_TOP, BLUE_BUTTON_BOTTOM, 
                BLUE_BUTTON_TOP_HOVER, 
                BLUE_BUTTON_BOTTOM_HOVER, 
                font = CURRENT_DEFAULT_FONT,
                border_radius = 7
            )

            connect_button = TextButton(
                TEXT_MAIN_MENU_CONNECT_SERVER_BUTTON, 
                get_centered_x(1, 350, 0)[0], 
                create_button.rect.top + create_button.rect.h + MARGIN_BOTTOM_BUTTON,
                350, 
                BUTTON_HEIGHT, 
                BLUE_BUTTON_TOP, 
                BLUE_BUTTON_BOTTOM, 
                BLUE_BUTTON_TOP_HOVER, 
                BLUE_BUTTON_BOTTOM_HOVER, 
                font = CURRENT_DEFAULT_FONT,
                border_radius = 7
            )

            quit_button = TextButton(
                TEXT_MAIN_MENU_QUIT_BUTTON, 
                get_centered_x(1, 350, 0)[0], 
                connect_button.rect.top + connect_button.rect.h + MARGIN_BOTTOM_BUTTON, 
                350, 
                BUTTON_HEIGHT, 
                BLUE_BUTTON_TOP, 
                BLUE_BUTTON_BOTTOM, 
                BLUE_BUTTON_TOP_HOVER, 
                BLUE_BUTTON_BOTTOM_HOVER, 
                font = CURRENT_DEFAULT_FONT,
                border_radius = 7
            )    

            create_button.draw(screen)
            connect_button.draw(screen)
            quit_button.draw(screen)
            language_button.draw(screen)
            credits_button.draw(screen)
            music_button.draw(screen)


        # Displays the language change screen.
        elif current_screen == Screen.LANGUAGE_SCREEN:
            text_surface = latin_small_font.render("AIRSEA-BATTLE", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 80))

            text_surface = CURRENT_MEDIUM_FONT.render(TEXT_LANGUAGE_MENU_TOP, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))

            en_us_button.draw(screen)
            pt_br_button.draw(screen)
            zh_cn_button.draw(screen)
            back_button.draw(screen)
        
        
        # Displays the credits screen.
        elif current_screen == Screen.CREDITS_SCREEN:
            text_surface = latin_small_font.render("AIRSEA-BATTLE", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 80))

            text_surface = CURRENT_MEDIUM_FONT.render(TEXT_CREDITS_SCREEN_TOP, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))

            text_surface = CURRENT_SMALL_FONT.render(TEXT_CREDITS_SCREEN_DEVELOPERS, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 190))

            text_surface = latin_default_font.render("Anderson Pastore Rizzi", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 215))

            text_surface = latin_default_font.render("Edurado Eberhardt Pereira", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 245))

            text_surface = CURRENT_SMALL_FONT.render(TEXT_CREDITS_SCREEN_MUSIC, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 300))

            text_surface = latin_default_font.render("\"Price of Freedom\" by Zakhar Valaha from Pixabay", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 320))

            text_surface = CURRENT_SMALL_FONT.render(TEXT_CREDITS_SCREEN_IMAGES, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 375))

            text_surface = latin_default_font.render("Sound icons by Konstantin Filatov from SVG Repo", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 395))

            text_surface = latin_default_font.render("Language icon by Noah Jacobus from SVG Repo", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 425))

            text_surface = latin_default_font.render("Credits icon by krystonschwarze from SVG Repo", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 455))

            back_button.draw(screen)
        

        # Displays the create server screen.
        elif current_screen == Screen.SERVER_SCREEN:
            create_server_button = TextButton(
                TEXT_SERVER_MENU_CREATE_BUTTON, 
                get_centered_x(1, 250, 0)[0], 
                400, 
                250, 
                50, 
                BLUE_BUTTON_TOP, 
                BLUE_BUTTON_BOTTOM, 
                BLUE_BUTTON_TOP_HOVER, 
                BLUE_BUTTON_BOTTOM_HOVER, 
                font = CURRENT_DEFAULT_FONT,
                border_radius = 7
            )

            text_surface = latin_small_font.render("AIRSEA-BATTLE", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 80))
            
            text_surface = CURRENT_MEDIUM_FONT.render(TEXT_SERVER_MENU_TOP, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))
            
            text_surface = latin_small_font.render("IP (localhost)", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, ip_text_box_for_server_creation.rect.top - MARGIN_TEXTBOX_LABEL))

            text_surface = CURRENT_SMALL_FONT.render(TEXT_PORT, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, port_text_box.rect.top - MARGIN_TEXTBOX_LABEL))

            back_button.draw(screen)
            ip_text_box_for_server_creation.draw(screen)
            port_text_box.draw(screen)
            create_server_button.draw(screen)
        

        # Displays the screen for connecting to a server.
        elif current_screen == Screen.CONNECTION_SCREEN:
            connect_button_submit = TextButton(
                TEXT_CONNECT_MENU_CONNECT_BUTTON, 
                get_centered_x(1, 250, 0)[0], 
                400, 
                250, 
                50, 
                BLUE_BUTTON_TOP, 
                BLUE_BUTTON_BOTTOM, 
                BLUE_BUTTON_TOP_HOVER, 
                BLUE_BUTTON_BOTTOM_HOVER, 
                font = CURRENT_DEFAULT_FONT,
                border_radius = 7
            )

            text_surface = latin_small_font.render("AIRSEA-BATTLE", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 80))
            
            text_surface = CURRENT_MEDIUM_FONT.render(TEXT_CONNECT_MENU_TOP, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))
            
            text_surface = latin_small_font.render("IP", True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, ip_text_box_for_server_connection.rect.top - MARGIN_TEXTBOX_LABEL))
            
            text_surface = CURRENT_SMALL_FONT.render(TEXT_PORT, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, port_text_box.rect.top - MARGIN_TEXTBOX_LABEL))

            back_button.draw(screen)
            ip_text_box_for_server_connection.draw(screen)
            port_text_box.draw(screen)
            connect_button_submit.draw(screen)
        

        # Displays the pause screens.
        if current_pause_screen == Screen.PORT_ERROR_PAUSE_SCREEN:
            draw_centered_text_with_blur(screen, TEXT_PORT_ERROR, CURRENT_DEFAULT_FONT, blur_radius=29)
            pause_remaining_time -= 1
            if pause_remaining_time <= 0:
                current_pause_screen = Screen.NO_PAUSE
        
        elif current_pause_screen == Screen.CONNECTION_TIME_OUT_PAUSE_SCREEN:
            draw_centered_text_with_blur(screen, TEXT_CONNECTION_TIME_OUT, CURRENT_DEFAULT_FONT, blur_radius=29)
            pause_remaining_time -= 1
            if pause_remaining_time <= 0:
                current_pause_screen = Screen.NO_PAUSE
        
        elif current_pause_screen == Screen.UNEXPECTED_ERROR_PAUSE_SCREEN:
            draw_centered_text_with_blur(screen, TEXT_UNEXPECTED_ERROR, CURRENT_SMALL_FONT, blur_radius=29)
            pause_remaining_time -= 1
            if pause_remaining_time <= 0:
                current_pause_screen = Screen.NO_PAUSE


        # Checks and responds to events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Checks if any key was pressed.
            elif event.type == pygame.KEYDOWN:
                # If the M key was pressed, it changes the music state.
                if event.key == pygame.K_m:
                    if not FADING_MUSIC and MUSIC_ON == True:
                        original_image = pygame.image.load('img/music_off_icon.png').convert_alpha()
                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                        start_fade_out(1)
                        MUSIC_ON = False
                    elif not FADING_MUSIC and MUSIC_ON == False:
                        original_image = pygame.image.load('img/music_on_icon.png').convert_alpha()
                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                        start_fade_in(1)
                        MUSIC_ON = True
                
                # If the ESC key was pressed, it returns to the previous menu.
                elif event.key == pygame.K_ESCAPE and current_screen != Screen.MAIN_MENU:
                    current_screen = Screen.MAIN_MENU


            # Interactions in the main menu.
            if current_pause_screen == Screen.NO_PAUSE and current_screen == Screen.MAIN_MENU:
                if create_button.handle_event(event):
                    current_screen = Screen.SERVER_SCREEN
                elif connect_button.handle_event(event):
                    current_screen = Screen.CONNECTION_SCREEN
                elif language_button.handle_event(event):
                    current_screen = Screen.LANGUAGE_SCREEN
                elif music_button.handle_event(event) and not FADING_MUSIC and MUSIC_ON == True:
                    original_image = pygame.image.load('img/music_off_icon.png').convert_alpha()
                    music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                    start_fade_out(1)
                    MUSIC_ON = False
                elif music_button.handle_event(event) and not FADING_MUSIC and MUSIC_ON == False:
                    original_image = pygame.image.load('img/music_on_icon.png').convert_alpha()
                    music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                    start_fade_in(1)
                    MUSIC_ON = True
                elif credits_button.handle_event(event):
                    current_screen = Screen.CREDITS_SCREEN
                elif quit_button.handle_event(event):
                    running = False


            # Interactions in the change language menu.
            elif current_pause_screen == Screen.NO_PAUSE and current_screen == Screen.LANGUAGE_SCREEN:
                if back_button.handle_event(event):
                    current_screen = Screen.MAIN_MENU
                elif en_us_button.handle_event(event):
                    change_language(Language.EN_US)
                    current_screen = Screen.MAIN_MENU
                elif pt_br_button.handle_event(event):
                    change_language(Language.PT_BR)
                    current_screen = Screen.MAIN_MENU
                elif zh_cn_button.handle_event(event):
                    change_language(Language.ZH_CN)
                    current_screen = Screen.MAIN_MENU
                
            
            # Interactions in the credits screen.
            elif current_pause_screen == Screen.NO_PAUSE and current_screen == Screen.CREDITS_SCREEN:
                if back_button.handle_event(event):
                    current_screen = Screen.MAIN_MENU

                    
            # Interactions in the server creation menu.
            elif current_pause_screen == Screen.NO_PAUSE and current_screen == Screen.SERVER_SCREEN:
                ip_text_box_for_server_creation.handle_event(event)
                port_text_box.handle_event(event)
                port_text_box.update(dt)

                if back_button.handle_event(event):
                    current_screen = Screen.MAIN_MENU
                if create_server_button != None and create_server_button.handle_event(event):
                    screen_snapshot = pygame.display.get_surface().copy()
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    try:
                        ip = ip_text_box_for_server_creation.text.strip()
                        port = int(port_text_box.text.strip())

                        if port < 0 or port > 65535:
                            current_pause_screen = Screen.PORT_ERROR_PAUSE_SCREEN
                            pause_remaining_time = 2 * FPS
                        else:
                            server_socket.bind((ip, port))
                            server_socket.listen(1)
                            server_socket.settimeout(0)
                            draw_centered_text_with_blur(screen, TEXT_WAITING_CONNECTION, CURRENT_DEFAULT_FONT, blur_radius=29)
                            
                            start_time = time.time()

                            # Accepts the connection in a non-blocking manner.
                            while True:
                                current_time = time.time()

                                if current_time - start_time >= SERVER_CONNECTION_TIMEOUT:
                                    screen.blit(screen_snapshot, (0, 0))
                                    pygame.display.flip()
                                    current_pause_screen = Screen.CONNECTION_TIME_OUT_PAUSE_SCREEN
                                    pause_remaining_time = 2 * FPS
                                    break

                                try:
                                    conn_player_2, _ = server_socket.accept()
                                    screen.blit(screen_snapshot, (0, 0))
                                    pygame.display.flip()

                                    thread_server_game = threading.Thread(target=receive_data_from_network, args=(conn_player_2,))
                                    thread_server_game.start()

                                    game_server(conn_player_2)

                                    # Adjusts the music icon if the music state has changed during gameplay.
                                    if MUSIC_ON == True:
                                        original_image = pygame.image.load('img/music_on_icon.png').convert_alpha()
                                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                                    elif MUSIC_ON == False:
                                        original_image = pygame.image.load('img/music_off_icon.png').convert_alpha()
                                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                                    break
                                    
                                except socket.error:
                                    pygame.event.pump()
                                    continue
                      
                    except Exception as e:
                        current_pause_screen = Screen.UNEXPECTED_ERROR_PAUSE_SCREEN
                        pause_remaining_time = 2 * FPS
                    
                    finally:
                        server_socket.close()
                        if current_pause_screen == Screen.NO_PAUSE:
                            current_screen = Screen.MAIN_MENU


            # Interactions in the server connection menu.
            elif current_pause_screen == Screen.NO_PAUSE and current_screen == Screen.CONNECTION_SCREEN:
                ip_text_box_for_server_connection.handle_event(event)
                port_text_box.handle_event(event)
                port_text_box.update(dt)

                if back_button.handle_event(event):
                    current_screen = Screen.MAIN_MENU
                if connect_button_submit != None and connect_button_submit.handle_event(event):
                    screen_snapshot = pygame.display.get_surface().copy()
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    try:
                        ip = ip_text_box_for_server_creation.text.strip()
                        port = int(port_text_box.text.strip())

                        if port < 0 or port > 65535:
                            current_pause_screen = Screen.PORT_ERROR_PAUSE_SCREEN
                            pause_remaining_time = 2 * FPS
                        else:
                            draw_centered_text_with_blur(screen, TEXT_CONNECTING_SERVER, CURRENT_DEFAULT_FONT, blur_radius=29)
                            client_socket.settimeout(0.2)

                            start_time = time.time()

                            # Makes the connection in a non-blocking manner.
                            while True:
                                current_time = time.time()

                                if current_time - start_time >= CLIENT_CONNECTION_TIMEOUT:
                                    screen.blit(screen_snapshot, (0, 0))
                                    pygame.display.flip()
                                    current_pause_screen = Screen.CONNECTION_TIME_OUT_PAUSE_SCREEN
                                    pause_remaining_time = 2 * FPS
                                    break

                                try:
                                    client_socket.connect((ip_text_box_for_server_connection.text, int(port_text_box.text)))
                                    screen.blit(screen_snapshot, (0, 0))
                                    pygame.display.flip()
                                    
                                    game_client(client_socket)

                                    # Adjusts the music icon if the music state has changed during gameplay.
                                    if MUSIC_ON == True:
                                        original_image = pygame.image.load('img/music_on_icon.png').convert_alpha()
                                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                                    elif MUSIC_ON == False:
                                        original_image = pygame.image.load('img/music_off_icon.png').convert_alpha()
                                        music_button.image = pygame.transform.smoothscale(original_image, (size_bottom_buttons, size_bottom_buttons))
                                    break
                                    
                                except socket.error:
                                    pygame.event.pump()
                                    continue

                    except Exception as e:
                        current_pause_screen = Screen.UNEXPECTED_ERROR_PAUSE_SCREEN
                        pause_remaining_time = 2 * FPS

                    finally:
                        client_socket.close()
                        if current_pause_screen == Screen.NO_PAUSE:
                            current_screen = Screen.MAIN_MENU
        
        pygame.display.flip()
    pygame.quit()



#|########################################################################|#
#| GAME IN SERVER VERSION                                                 |#
#|########################################################################|#

def game_server(network_socket):
    global FADING_MUSIC
    global MUSIC_ON

    local_clock = pygame.time.Clock()

    left_cannon = Cannon(0, 'left') 
    right_cannon = Cannon(SCREEN_WIDTH - CANNON_WIDTH, 'right')
    p1_score = 0 # Cannon on the left (server).
    p2_score = 0 # Cannon on the right (client).

    current_cannon = left_cannon

    projectiles = []
    airplanes_direction = 1
    airplanes, airplanes_direction = create_airplanes(airplanes_direction)
    
    angle_index = 2  # Starts with 90 degrees.
    current_remaining_time = MATCH_TIME

    # Game execution loop.
    while current_remaining_time > 0:
        dt = local_clock.tick(FPS)

        # Draw the background and timer.
        draw_sky()
        draw_grass()
        draw_remaining_time(screen, current_remaining_time, latin_default_font)

        # Decrements the remaining time.
        current_remaining_time -= dt

        # Find the left cannon angle index.
        for i, angle in enumerate(CANNON_ANGLES):
            if left_cannon.angle == angle:
                angle_index = i
                break

        # Game event check.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_remaining_time = 0
            
            elif event.type == pygame.KEYDOWN:
                # If the K_DOWN or K_UP key is pressed, it changes the firing angle of the cannon.
                if event.key == pygame.K_DOWN:
                    if angle_index > 0:
                        angle_index -= 1
                        current_cannon.angle = CANNON_ANGLES[angle_index]
                if event.key == pygame.K_UP:
                    if angle_index < len(CANNON_ANGLES) - 1:
                        angle_index += 1
                        current_cannon.angle = CANNON_ANGLES[angle_index]
                
                # If the SPACE key is pressed, fires a projectile.
                elif event.key == pygame.K_SPACE:
                    if current_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES and current_cannon.current_ammo > 0:
                        current_cannon.current_ammo -= 1
                        projectiles.append(Projectile(current_cannon.x + CANNON_WIDTH // 2, CANNON_Y + CANNON_HEIGHT // 2, current_cannon.angle, current_cannon.side))
                    elif current_cannon.current_buff == GamePowerUps.UNLIMITED_PROJECTILES:
                        projectiles.append(Projectile(current_cannon.x + CANNON_WIDTH // 2, CANNON_Y + CANNON_HEIGHT // 2, current_cannon.angle, current_cannon.side))
                
                # If the M key was pressed, it changes the music state.
                elif event.key == pygame.K_m:
                    if not FADING_MUSIC and MUSIC_ON == True:
                        start_fade_out(1)
                        MUSIC_ON = False
                    elif not FADING_MUSIC and MUSIC_ON == False:
                        start_fade_in(1)
                        MUSIC_ON = True

        keys = pygame.key.get_pressed()
        
        # Moves the left cannon.
        if keys[pygame.K_LEFT] and current_cannon.x > 0:
            current_cannon.x -= 5
        if keys[pygame.K_RIGHT] and current_cannon.x < SCREEN_WIDTH // 2 - CANNON_WIDTH:
            current_cannon.x += 5

        # Find the right cannon angle index.
        for i, angle in enumerate(CANNON_ANGLES):
            if right_cannon.angle == angle:
                angle_index = i
                break

        # Processes the other player's keys.
        while not player_2_key_list.empty():
            new_key = player_2_key_list.get() 
            if new_key == 'k_left' and right_cannon.x > SCREEN_WIDTH // 2:
                right_cannon.x -= 5
            elif new_key == 'k_right' and right_cannon.x < SCREEN_WIDTH - CANNON_WIDTH:
                right_cannon.x += 5
            elif new_key == 'k_down' and angle_index > 0:
                angle_index -= 1
                right_cannon.angle = CANNON_ANGLES[angle_index]
            elif new_key == 'k_up' and angle_index < len(CANNON_ANGLES) - 1:
                angle_index += 1
                right_cannon.angle = CANNON_ANGLES[angle_index]
            elif new_key == 'k_space':
                if right_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES and right_cannon.current_ammo > 0:
                    right_cannon.current_ammo-=1
                    projectiles.append(Projectile(right_cannon.x + CANNON_WIDTH // 2, CANNON_Y + CANNON_HEIGHT // 2, right_cannon.angle, right_cannon.side))
                elif right_cannon.current_buff == GamePowerUps.UNLIMITED_PROJECTILES:
                    projectiles.append(Projectile(right_cannon.x + CANNON_WIDTH // 2, CANNON_Y + CANNON_HEIGHT // 2, right_cannon.angle, right_cannon.side))
            
        # Projectiles update.
        for projectile in projectiles[:]:
            projectile.update()

            if projectile.y < 0 or projectile.x < 0 or projectile.x > SCREEN_WIDTH:
                if projectile.side == 'left' and left_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES:
                    left_cannon.current_ammo += 1
                elif projectile.side == 'right' and right_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES:
                    right_cannon.current_ammo += 1
                
                projectiles.remove(projectile)

            for airplane in airplanes[:]:
                if airplane.x < projectile.x < airplane.x + AIRPLANE_WIDTH and airplane.y < projectile.y < airplane.y + AIRPLANE_HEIGHT:
                    if projectile.side == 'left':
                        if left_cannon.current_buff == GamePowerUps.DOUBLE_POINTS:
                            p1_score += 2
                        else:
                            p1_score += 1
                        
                        if left_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES:
                            left_cannon.current_ammo += 1
                        if left_cannon.current_buff == GamePowerUps.NONE and airplane.buff != GamePowerUps.NONE:
                            left_cannon.current_buff = airplane.buff
                            left_cannon.buff_timer = POWER_UP_TIME
                            if airplane.buff == GamePowerUps.UNLIMITED_PROJECTILES:
                                left_cannon.current_ammo = left_cannon.max_ammo
                        
                    elif projectile.side == 'right':
                        if right_cannon.current_buff == GamePowerUps.DOUBLE_POINTS:
                            p2_score += 2
                        else:
                            p2_score += 1

                        if right_cannon.current_buff != GamePowerUps.UNLIMITED_PROJECTILES:
                            right_cannon.current_ammo += 1
                        if right_cannon.current_buff == GamePowerUps.NONE and airplane.buff != GamePowerUps.NONE:
                            right_cannon.current_buff = airplane.buff
                            right_cannon.buff_timer = POWER_UP_TIME
                            if airplane.buff == GamePowerUps.UNLIMITED_PROJECTILES:
                                right_cannon.current_ammo = right_cannon.max_ammo

                    airplanes.remove(airplane)
                    projectiles.remove(projectile)
        
        # Airplanes update.
        if not airplanes:
            airplanes, airplanes_direction = create_airplanes(airplanes_direction)

        for airplane in airplanes[:]:
            airplane.update()
            if airplane.x < -AIRPLANE_WIDTH or airplane.x > SCREEN_WIDTH + AIRPLANE_WIDTH:
                airplanes.remove(airplane)

        # Draw the airplanes.
        for airplane in airplanes:
            airplane.draw()

        # Draw the projectiles.
        for projectile in projectiles:
            projectile.draw()

        # Draw the cannons.
        left_cannon.draw()
        right_cannon.draw()

        # Draw the score.
        draw_scores(p1_score, p2_score, latin_default_font)

        # Sends the game state to the other player.
        airplanes_list = []
        for airplane in airplanes[:]:
            airplanes_list.append(airplane.to_dict())
        send_data = pickle.dumps([projectiles, airplanes_list, left_cannon.to_dict(), right_cannon.to_dict(), current_remaining_time, p1_score, p2_score])        
        sent_data_len = struct.pack('>I', len(send_data))  # Note: '>I' indicates a 4-byte big-endian integer.
        network_socket.sendall(sent_data_len)
        network_socket.sendall(send_data)

        # Refresh the screen.
        pygame.display.flip()

    # Returns the match state.
    if p1_score > p2_score:
        draw_centered_text_with_blur(screen, TEXT_MATCH_WON, CURRENT_MEDIUM_FONT, blur_radius=29)
    elif p2_score > p1_score:
        draw_centered_text_with_blur(screen, TEXT_MATCH_LOST, CURRENT_MEDIUM_FONT, blur_radius=29)
    elif p1_score == p2_score:
       draw_centered_text_with_blur(screen, TEXT_MATCH_TIE, CURRENT_MEDIUM_FONT, blur_radius=29)
    else:
        draw_centered_text_with_blur(screen, TEXT_UNEXPECTED_ERROR, CURRENT_SMALL_FONT, blur_radius=29)

    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= 3:
            break
        pygame.event.pump()



#|########################################################################|#
#| GAME IN CLIENT VERSION                                                 |#
#|########################################################################|#

def game_client(client_socket):
    global FADING_MUSIC
    global MUSIC_ON

    left_cannon = Cannon(0, 'left') 
    right_cannon = Cannon(SCREEN_WIDTH - CANNON_WIDTH, 'right')
    p1_score = 0 # Cannon on the left (server).
    p2_score = 0 # Cannon on the right (client).

    projectiles = []
    airplanes = []
    
    current_remaining_time = MATCH_TIME

    running = True

    while running:
        clock.tick(FPS)

        # Draw the background and timer.
        draw_sky()
        draw_grass()
        draw_remaining_time(screen, current_remaining_time, latin_default_font)

        # Game event check.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_2_key_list.put('k_down')
                elif event.key == pygame.K_UP:
                    player_2_key_list.put('k_up')
                elif event.key == pygame.K_SPACE:
                    player_2_key_list.put('k_space')
                
                # If the M key was pressed, it changes the music state.
                elif event.key == pygame.K_m:
                    if not FADING_MUSIC and MUSIC_ON == True:
                        start_fade_out(1)
                        MUSIC_ON = False
                    elif not FADING_MUSIC and MUSIC_ON == False:
                        start_fade_in(1)
                        MUSIC_ON = True
                    
        keys = pygame.key.get_pressed()

        # Right cannon movement key capture.
        if keys[pygame.K_LEFT] and right_cannon.x > SCREEN_WIDTH // 2:
            player_2_key_list.put('k_left')
            right_cannon.x -= 5
        if keys[pygame.K_RIGHT] and right_cannon.x < SCREEN_WIDTH - CANNON_WIDTH:
            player_2_key_list.put('k_right')
            right_cannon.x += 5
        
        if not player_2_key_list.empty():
            data = pickle.dumps(list(player_2_key_list.queue))
            data_len = struct.pack('>I', len(data))
            client_socket.sendall(data_len)
            client_socket.sendall(data)

            while not player_2_key_list.empty():
                player_2_key_list.get()

        # Receives the length of the data.
        data_len_bytes = client_socket.recv(4)

        # Checks if the connection was closed by the server.
        if not data_len_bytes:
            break
        received_data_len = struct.unpack('>I', data_len_bytes)[0]

        # Receives data with known length.
        received_data = b''
        while len(received_data) < received_data_len:
            more_data = client_socket.recv(received_data_len - len(received_data))
            # Checks if the connection is closed by the server while receiving data.
            if not more_data:
                break
            received_data += more_data

        # Deserialize and put the data in the queue that will be read by the server.
        if received_data:
            game_data = pickle.loads(received_data)
            projectiles = game_data[0]
            airplanes_list = game_data[1]
            left_cannon.update_from_dict(game_data[2]) 
            right_cannon.update_from_dict(game_data[3])
            current_remaining_time = int(game_data[4])
            if (current_remaining_time <= 0):
                break
            p1_score = int(game_data[5])
            p2_score = int(game_data[6])

            airplanes.clear()
            for airplane_dict in airplanes_list[:]:
                new_airplane = Airplane(airplane_dict['x'], airplane_dict['y'], airplane_dict['direction'], airplane_dict['buff'])
                airplanes.append(new_airplane)

        # Draw the airplanes.
        for airplane in airplanes:
            airplane.draw()

        # Draw the projectiles.
        for projectile in projectiles:
            projectile.draw()

        # Draw the cannons.
        left_cannon.draw()
        right_cannon.draw()

        # Draw the score.
        draw_scores(p1_score, p2_score, latin_default_font)

        # Refresh the screen.
        pygame.display.flip()

    # Returns the match state.
    if p2_score > p1_score:
        draw_centered_text_with_blur(screen, TEXT_MATCH_WON, CURRENT_MEDIUM_FONT, blur_radius=29)
    elif p1_score > p2_score:
        draw_centered_text_with_blur(screen, TEXT_MATCH_LOST, CURRENT_MEDIUM_FONT, blur_radius=29)
    elif p1_score == p2_score:
       draw_centered_text_with_blur(screen, TEXT_MATCH_TIE, CURRENT_MEDIUM_FONT, blur_radius=29)
    else:
        draw_centered_text_with_blur(screen, TEXT_UNEXPECTED_ERROR, CURRENT_SMALL_FONT, blur_radius=29)

    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= 3:
            break
        pygame.event.pump()



#|########################################################################|#
#| MAIN FUNCTION                                                          |#
#|########################################################################|#

if __name__ == "__main__":
    main_menu()
