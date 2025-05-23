import pygame
import sys
import pixel
import sprites

pygame.init()
pygame.font.init()

# Display variables
sw = 1280 # Fake OLED screen--each "pixel" is 10x10 px
sh = 640
screen = pygame.display.set_mode((sw, sh))
font = pygame.font.Font(size=70)
stage = "title"

# Title screen variables
title_screen = pygame.image.load("assets/title.png")
title_cover = pygame.Surface((1280, 640))
title_fade = 255

# Movement variables
keys_pressed = [False, False, False, False]

# Time variables
clock = pygame.time.Clock()
fps = 50

# DRC variables
drc_hud = pygame.image.load("assets/drc_txts/drc_1.png")
wave = 0

# Player variables
player = pixel.Character(sprites.player_cursor, False)
player.move(63, 31)
player_x = 32
player_y = 64
pixel.all_pixels = []

# Enemy variables
zombie = pixel.Character(sprites.warning_zombie)
brute = pixel.Character(sprites.error_brute)
brute.move(20, 20)

# Game wall variables
wall_top = pixel.HorizPixel(0, 0, 128)
wall_bottom = pixel.HorizPixel(0, 63, 128)
wall_left = pixel.VertPixel(0, 0, 64)
wall_right = pixel.VertPixel(127, 0, 64)

def draw_stage():
    global stage, title_fade
    if stage == "title":
        screen.blit(title_screen, (0, 0, 10, 10))
        if (pygame.time.get_ticks() % 1000 > 500):
            cover_title = pygame.Rect(490, 500, 300, 80)
            pygame.draw.rect(screen, (0, 0, 0), cover_title)
        title_cover.set_alpha(title_fade)
        title_cover.fill((0, 0, 0))
        screen.blit(title_cover, (0, 0))
        if (title_fade > 0):
            title_fade -= 2
    
    elif stage == "title_shift":
        screen.blit(title_screen, (0, 0, 10, 10))
        if (pygame.time.get_ticks() % 1000 > 500):
            cover_title = pygame.Rect(490, 500, 300, 80)
            pygame.draw.rect(screen, (0, 0, 0), cover_title)
        title_cover.set_alpha(title_fade)
        title_cover.fill((0, 0, 0))
        screen.blit(title_cover, (0, 0))
        if (title_fade < 255):
            title_fade += 3
        else:
            stage = "game"

    else:
        player.draw(screen)
        zombie.draw(screen)
        brute.draw(screen)
        wall_top.draw(screen)
        wall_bottom.draw(screen)
        wall_left.draw(screen)
        wall_right.draw(screen)
        screen.blit(drc_hud, (0, 0, 10, 10))

def event_catcher():
    global stage
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and stage == "title":
            stage = "title_shift"

        if key[pygame.K_UP]:
            keys_pressed[0] = True
        else:
            keys_pressed[0] = False
        
        if key[pygame.K_DOWN]:
            keys_pressed[1] = True
        else:
            keys_pressed[1] = False
        
        if key[pygame.K_LEFT]:
            keys_pressed[2] = True
        else:
            keys_pressed[2] = False

        if key[pygame.K_RIGHT]:
            keys_pressed[3] = True
        else:
            keys_pressed[3] = False

        if key[pygame.K_w]:
            print("UP")

        if key[pygame.K_a]:
            print("DOWN")

        if key[pygame.K_s]:
            print("LEFT")

        if key[pygame.K_d]:
            print("RIGHT")

def move_character():
    global player_x, player_y
    if keys_pressed[0] and wall_top.get_y() < 30:
        pixel.move_all(0, 1)
        player_y += 1
    if keys_pressed[1] and wall_bottom.get_y() > 36:
        pixel.move_all(0, -1)
        player_y -= 1
    if keys_pressed[2] and wall_left.get_x() < 67:
        pixel.move_all(1, 0)
        player_x -= 1
    if keys_pressed[3] and wall_right.get_x() > 73:
        pixel.move_all(-1, 0)
        player_x += 1

def move_enemies():
    if (zombie.get_center()[0] < 640):
        zombie.move(0.3, 0)
    if (zombie.get_center()[0] > 640):
        zombie.move(-0.3, 0)
    if (zombie.get_center()[1]  < 320):
        zombie.move(0, 0.3)
    if (zombie.get_center()[1]  > 320):
        zombie.move(0, -0.3)
    if (brute.get_center()[0] < 640):
        brute.move(0.1, 0)
    if (brute.get_center()[0] > 640):
        brute.move(-0.1, 0)
    if (brute.get_center()[1]  < 320):
        brute.move(0, 0.1)
    if (brute.get_center()[1]  > 320):
        brute.move(0, -0.1)

while True:
    '''Inf loop for Pygame functionality.'''
    screen.fill((0, 0, 0))
    draw_stage()
    event_catcher()
    if stage == "game":
        move_character()
        move_enemies()
    clock.tick(fps)
    pygame.display.flip()