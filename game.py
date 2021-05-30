#!/usr/bin/python3.4

# Setup Python ----------------------------------------------- #
from pygame.locals import *
import pygame
import random
import math

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
pygame.mixer.init()
pygame.init()

# set window resolution
res = (800, 600)

# open a window
window = pygame.display.set_mode(res)

# store in variables width and height of the window
width = window.get_width()
height = window.get_height()

# init title
pygame.display.set_caption('The Legend of Slugterra')

# init icon
icon = pygame.image.load("./requirements/slugicon32.png")
pygame.display.set_icon(icon)

# init fonts
font = pygame.font.Font('./requirements/Slugterra.otf', 36)
pygame.font.init()


# set light shade of the button
color_main = pygame.Color('yellow')

# set dark shade of the button
color_bkg = pygame.Color('black')

# set dark shade of the button
color_hover = (20, 20, 20)

# Load and play loop of background music:
pygame.mixer.music.load("./requirements/thunder.ogg")
pygame.mixer.music.play(-1, 22.8)
pygame.mixer.music.set_volume(0.5)

# auxiliary function to draw text used in all screens


def draw_text(text, font, color, surface, coords):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = coords
    surface.blit(textobj, textrect)


# auxiliary class for buttons


class Button(pygame.sprite.Sprite):

    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)

        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple blit them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)

        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback

    def _create_image(self, color, outline, text, rect):
        # function to create the actual surface
        # see how we can make use of Rect's virtual attributes like 'size'
        img = pygame.Surface(rect.size)
        if outline:
            # here we can make good use of Rect's functions again
            # first, fill the Surface in the outline color
            # then fill a rectangular area in the actual color
            # 'inflate' is used to 'shrink' the rect
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -4))
        else:
            img.fill(color)

        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, color_main)
            # again, see how easy it is to center stuff using Rect's attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        img.set_colorkey(color_bkg)
        img.set_alpha(150)  # make transparent!
        return img

    def update(self, events):
        # here we handle all the logic of the Button
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        # if the mouse is inside the Rect (again, see how the Rect class
        # does all the calculation for us), use the 'hov' image instead of 'org'
        self.image = self.hov if hit else self.org
        for event in events:
            # the Button checks for events itself.
            # if this Button is clicked, it runs the callback function
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)


# Main menu screen
click = False


def main_menu():

    bg_menu = pygame.image.load("./requirements/legend-slugterra-menu-800x600.png")

    sprites = pygame.sprite.Group()
    sprites.add(Button(color_bkg,
                       color_hover,
                       pygame.Rect(width/4 - 180, height - 160, 360, 80),
                       lambda b: game(),
                       'PLAY',
                       color_main))

    sprites.add(Button(color_bkg,
                       color_hover,
                       pygame.Rect(3*width/4 - 180, height - 160, 360, 80),
                       lambda b: options(),
                       'OPTIONS',
                       color_main))

    while True:

        draw_text('MAIN MENU', font, color_main, window, (20, 20))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # update all sprites
        # it doesn't matter how many Buttons we have
        sprites.update(events)

        # refresh backgroud
        window.blit(bg_menu, (0, 0))
        # draw all sprites/Buttons
        sprites.draw(window)

        pygame.display.update()
        # limit framerate to 60 FPS
        mainClock.tick(60)


def game():

    # init sound effects:
    laser_sound = pygame.mixer.Sound('./requirements/laser_sound2.wav')
    laser_sound.set_volume(0.05)
    kill_sound = pygame.mixer.Sound('./requirements/kill_sound.wav')
    kill_sound.set_volume(0.2)

    # load game background image
    bg = pygame.image.load("./requirements/bkg800-600.jpg")

    # init slugterra goodie
    # load image
    slug_goodie = pygame.image.load("./requirements/slug_goodie.png")
    # initial position
    slug_goodie_X = 400
    slug_goodie_Y = 500
    slug_goodie_vble_pos = 0

    def display_slug_goodie(x, y):
        window.blit(slug_goodie, (x, y))

    # init list of slugterra baddies
    slug_baddie = []
    slug_baddie_X = []
    slug_baddie_Y = []
    slug_baddie_vble_pos_x = []
    slug_baddie_vble_pos_y = []

    number_baddies = 5
    for i in range(number_baddies):
        # load image
        slug_baddie.append(pygame.image.load("./requirements/slug_baddie.png"))
        # initial position
        slug_baddie_X.append(random.randint(0, 700))
        slug_baddie_Y.append(random.randint(0, 150))
        slug_baddie_vble_pos_x.append(.5)
        slug_baddie_vble_pos_y.append(50)

    def display_slug_baddie(x, y, i):
        window.blit(slug_baddie[i], (x, y))

    # init laser
    # load image
    laser = pygame.image.load("./requirements/laser.png")
    laser_X = 0
    laser_Y = 480
    laser_vble_pos_y = 8
    # initial state
    l_state = False

    def fire_laser(x, y):
        window.blit(laser, (x, y))
        pygame.mixer.find_channel(True).play(laser_sound)

    # collision

    def collision_detection(slug_baddie_X, slug_baddie_Y, laser_X, laser_Y, threshold):
        dist = math.sqrt(math.pow(slug_baddie_X - laser_X, 2) +
                         math.pow(slug_baddie_Y - laser_Y, 2))
        if dist < threshold:
            return True
        else:
            return False

    # init scoring system
    score = 0

    # Game Over
    over_font = pygame.font.Font('./requirements/Slugterra.otf', 80)

    def game_over():
        over = over_font.render("GAME OVER", True, (255, 255, 0))
        window.blit(over, (200, 220))

    """def display_score(X, Y):
        s = font.render("SCORE: " + str(score), True, (255, 255, 0))
        window.blit(s, (X, Y))"""

    # main loop
    running = True

    while running:
        # refresh backgroud
        window.blit(bg, (0, 0))

        # event loop
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_ESCAPE:
                    running = False
                if even.key == pygame.K_RIGHT:
                    slug_goodie_vble_pos += 1
                if even.key == pygame.K_LEFT:
                    slug_goodie_vble_pos -= 1
                if even.key == pygame.K_SPACE and l_state is False:
                    laser_X = slug_goodie_X
                    l_state = True

            if even.type == pygame.KEYUP:
                if even.key == pygame.K_RIGHT or even.key == pygame.K_LEFT:
                    slug_goodie_vble_pos = 0

        # slug_goodie logic
        slug_goodie_X += slug_goodie_vble_pos
        if slug_goodie_X <= 0:
            slug_goodie_X = 0
        if slug_goodie_X >= 700:
            slug_goodie_X = 700

        display_slug_goodie(slug_goodie_X, slug_goodie_Y)

        # laser logic
        if l_state:
            laser_Y -= laser_vble_pos_y
            fire_laser(laser_X+15, laser_Y+15)

        if laser_Y <= 0:
            laser_Y = 480
            l_state = False

        # slug_baddie logic
        for i in range(number_baddies):

            # game over logic
            if slug_baddie_Y[i] > 600 or collision_detection(
                    slug_baddie_X[i], slug_baddie_Y[i],
                    slug_goodie_X, slug_goodie_Y, 50):
                for j in range(number_baddies):
                    slug_baddie_Y[j] = 2000
                game_over()
                break

            slug_baddie_X[i] += slug_baddie_vble_pos_x[i]

            if slug_baddie_X[i] <= 0:
                slug_baddie_vble_pos_x[i] = .3
                slug_baddie_Y[i] += slug_baddie_vble_pos_y[i]

            if slug_baddie_X[i] >= 700:
                slug_baddie_vble_pos_x[i] = -.3
                slug_baddie_Y[i] += slug_baddie_vble_pos_y[i]
            if collision_detection(slug_baddie_X[i], slug_baddie_Y[i],
                                   laser_X, laser_Y, 20):
                # initialize laser
                l_state = False
                pygame.mixer.find_channel(True).play(kill_sound)
                score += 10
                slug_baddie_X[i] = random.randint(0, 700)
                slug_baddie_Y[i] = random.randint(0, 200)

            display_slug_baddie(slug_baddie_X[i], slug_baddie_Y[i], i)

        draw_text("SCORE: " + str(score), font, color_main, window, (20, 20))

        # last action in loop update display
        pygame.display.update()
        # mainClock.tick(60)


def options():
    running = True
    while running:
        window.fill((0, 0, 0))

        draw_text('OPTIONS', font, color_main, window, (20, 20))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()
