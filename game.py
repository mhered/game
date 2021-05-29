import pygame
import random
import math

# Credits

# Inspired by this tutorial from edureka:
# https://www.youtube.com/watch?v=KFP9qXiHQ0o

# Background vector created by upklyak:
# https://www.freepik.com/vectors/background

# Slugterra font designed by HackFonts:
# https://www.dafontfree.io/slugterra-font/

# Images from Slugterra Fandom Wiki:
# https://slugterra.fandom.com/wiki/SlugTerra_Wiki

# initialization
pygame.init()

# window
window = pygame.display.set_mode((800, 600))

# title
pygame.display.set_caption('The Legend of Slugterra')

# icon
icon = pygame.image.load("./requirements/slugicon32.png")
pygame.display.set_icon(icon)

# background
bg = pygame.image.load("./requirements/bkg800-600.jpg")

# slugterra goodie
# load image
slug_goodie = pygame.image.load("./requirements/slug_goodie.png")
# initial position
slug_goodie_X = 400
slug_goodie_Y = 500
slug_goodie_vble_pos = 0


def display_slug_goodie(x, y):
    window.blit(slug_goodie, (x, y))


# slugterra baddies
# load image
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
    slug_baddie_vble_pos_y.append(80)


def display_slug_baddie(x, y, i):
    window.blit(slug_baddie[i], (x, y))


# laser
# load image
laser = pygame.image.load("./requirements/laser.png")
laser_X = 0
laser_Y = 480
laser_vble_pos_y = 8
# initial state
l_state = False


def fire_laser(x, y):
    window.blit(laser, (x, y))


# Collision


def collision_detection(slug_baddie_X, slug_baddie_Y, laser_X, laser_Y, threshold):
    dist = math.sqrt(math.pow(slug_baddie_X - laser_X, 2) + math.pow(slug_baddie_Y - laser_Y, 2))
    if dist < threshold:
        return True
    else:
        return False


# Scoring system
score = 0
font = pygame.font.Font('./requirements/Slugterra.otf', 48)
pygame.font.init()
X = 10
Y = 10

# Game Over
over_font = pygame.font.Font('./requirements/Slugterra.otf', 80)


def game_over():
    over = over_font.render("GAME OVER", True, (255, 255, 0))
    window.blit(over, (200, 220))


def display_score(X, Y):
    s = font.render("SCORE: " + str(score), True, (255, 255, 0))
    window.blit(s, (X, Y))


# main loop
running = True
while running:
    # window.fill((255, 0, 45))
    # refresh backgroud
    window.blit(bg, (0, 0))

    # event loop
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            running = False
        if even.type == pygame.KEYDOWN:
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
            laser_Y = 480
            l_state = False
            score += 10
            slug_baddie_X[i] = random.randint(0, 700)
            slug_baddie_Y[i] = random.randint(0, 200)

        display_slug_baddie(slug_baddie_X[i], slug_baddie_Y[i], i)

    display_score(X, Y)

    # last action in loop update display
    pygame.display.update()

# after loop quit
pygame.quit()
