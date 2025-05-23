import pygame
import sys
import random
import pixel
import sprites
import serial

pygame.init()
pygame.font.init()

# Open serial comms with Arduino controller... unless we don't have one. Then just do keyboard.
try:
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/cu.usbmodem4827E2FD7CA02'
    ser.timeout = 0.01
    ser.open()
    button_press = 0
    last_press = 0
    arduino_mode = True
except:
    arduino_mode = False

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

# Game over screen variables
go_screen = pygame.image.load("assets/game_over.png")
go_screen2 = pygame.image.load("assets/game_over_2.png")
go_cover = pygame.Surface((1280, 640))
go_fade = 255

# Win screen variables
win_screen = pygame.image.load("assets/win.png")
win_screen2 = pygame.image.load("assets/win.png")
win_cover = pygame.Surface((1280, 640))
win_fade = 255

# Movement variables
keys_pressed = [False, False, False, False]

# Time variables
clock = pygame.time.Clock()
fps = 60

# DRC variables
drc_hud = pygame.image.load("assets/drc_txts/drc_1.png")
wave = 0

# Player variables
player = pixel.Character(sprites.player_cursor, False)
player.move(63, 31)
player_x = 32
player_y = 64
pixel.all_pixels = [] # player should not be subject to pixel movement rules

# Combat variables
gun_cd = 0
gcd_length = 100 # cooldown between shots, in millis
if arduino_mode: # can't control gun direction, so make it autofire but slower
    gcd_length = 250
kills = 0

# Enemy variables
zombie_cd = 0
zcd_length = 5000
brute_cd = 0
bcd_length = 11000

# Game background variables
wall_top = pixel.HorizPixel(0, 0, 128)
wall_bottom = pixel.HorizPixel(0, 63, 128)
wall_left = pixel.VertPixel(0, 0, 64)
wall_right = pixel.VertPixel(127, 0, 64)
vias = []
for i in range(8):
    top = pixel.HorizPixel(4+i*16, 6, 8)
    bot = pixel.HorizPixel(4+i*16, 15, 8)
    left = pixel.VertPixel(3+i*16, 7, 8)
    right = pixel.VertPixel(12+i*16, 7, 8)
    #spawn_point = [7+i*16, 10] # CENTERED SPAWN
    #print(spawn_point)
    spawn_point = [3+i*16, 6] # TLEFT SPAWN
    vias.append(top)
    vias.append(bot)
    vias.append(left)
    vias.append(right)
    pixel.spawns.append(spawn_point)

def read_ard():
    '''Gets message from Arduino.'''
    global button_press, last_press
    try:
        button_press = ord(ser.read(1))
        if button_press != 0:
            last_press = button_press
    except:
        pass
    print(button_press)

def draw_stage():
    global stage, title_fade, go_fade
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

    elif stage == "game":
        player.draw(screen)
        draw_bg()
        for i in pixel.all_checks:
            i.draw(screen)
        for i in pixel.all_enemies:
            i.draw(screen)
            #vvv DEBUG MODE: DRAW ALL HITBOXES vvv
            #pygame.draw.rect(screen, (255, 0, 0), i.get_hitbox().rect)
        screen.blit(drc_hud, (0, 0, 10, 10))

    elif stage == "gameover":
        screen.blit(go_screen, (0, 0, 10, 10))
        go_cover.set_alpha(go_fade)
        go_cover.fill((0, 0, 0))
        if (pygame.time.get_ticks() % 1000 > 500):
            screen.blit(go_screen2, (0, 0, 10, 10))
        screen.blit(go_cover, (0, 0))
        if (go_fade > 0):
            go_fade -= 2

    elif stage == "win":
        screen.blit(win_screen, (0, 0, 10, 10))
        win_cover.set_alpha(win_fade)
        win_cover.fill((0, 0, 0))
        if (pygame.time.get_ticks() % 1000 > 500):
            screen.blit(win_screen2, (0, 0, 10, 10))
        screen.blit(win_cover, (0, 0))
        if (win_fade > 0):
            win_fade -= 2

def draw_bg():
    # Draw edges of PCB
    wall_top.draw(screen)
    wall_bottom.draw(screen)
    wall_left.draw(screen)
    wall_right.draw(screen)

    print(pixel.spawns[0])
    # Draw the via portals (for the monsters to emerge from)
    for i in vias:
        i.draw(screen)

def event_catcher():
    global stage, gun_cd, gcd_length

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

        if pygame.time.get_ticks() - gun_cd > gcd_length:
            if key[pygame.K_w]:
                player.spawn_proj("check", 0, -2)
                gun_cd = pygame.time.get_ticks()

            elif key[pygame.K_s]:
                player.spawn_proj("check", 0, 2)
                gun_cd = pygame.time.get_ticks()

            elif key[pygame.K_a]:
                player.spawn_proj("check", -2, 0)
                gun_cd = pygame.time.get_ticks()

            elif key[pygame.K_d]:
                player.spawn_proj("check", 2, 0)
                gun_cd = pygame.time.get_ticks()

def arduino_events():
    global stage, gun_cd, gcd_length, button_press, last_press
    if button_press != 0 and stage == "title":
        stage = "title_shift"

    if button_press == 1:
        keys_pressed[0] = True
    else:
        keys_pressed[0] = False

    if button_press == 2:
        keys_pressed[1] = True
    else:
        keys_pressed[1] = False

    if button_press == 3:
        keys_pressed[2] = True
    else:
        keys_pressed[2] = False

    if button_press == 4:
        keys_pressed[3] = True
    else:
        keys_pressed[3] = False

    if pygame.time.get_ticks() - gun_cd > gcd_length:
        print("HI")
        print(last_press)
        if last_press == 1:
            player.spawn_proj("check", 0, -2)
            gun_cd = pygame.time.get_ticks()

        if last_press == 2:
            player.spawn_proj("check", 0, 2)
            gun_cd = pygame.time.get_ticks()

        if last_press == 3:
            player.spawn_proj("check", -2, 0)
            gun_cd = pygame.time.get_ticks()

        if last_press == 4:
            player.spawn_proj("check", 2, 0)
            gun_cd = pygame.time.get_ticks()

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
    for i in pixel.all_enemies:
        spd = i.speed
        if (i.get_center()[0] < 640):
            i.move(spd, 0)
        if (i.get_center()[0] > 640):
            i.move(-spd, 0)
        if (i.get_center()[1]  < 320):
            i.move(0, spd)
        if (i.get_center()[1]  > 320):
            i.move(0, -spd)

def move_projectiles():
    i = 0
    while i < len(pixel.all_checks):
        pix = pixel.all_checks[i]
        pix.move(pix.x_dir, pix.y_dir)
        i+=1
        if pix.get_center()[0] < -1000 or pix.get_center()[0] > 2000 or pix.get_center()[1] < -1000 or pix.get_center()[1] > 1000:
            pixel.all_checks.remove(pix)
            del pix
            i-=1

def check_collisions():
    global stage, kills, drc_hud
    # Step 1: Did the player shoot any enemies?
    i = 0
    while i < len(pixel.all_checks):
        pix = pixel.all_checks[i]
        p_hb = pix.get_hitbox()
        j = 0
        while j < len(pixel.all_enemies):
            ene = pixel.all_enemies[j]
            e_hb = ene.get_hitbox()
            print("enemy", e_hb.rect)
            print("proj", p_hb.rect)
            if p_hb.check_hit(e_hb):
                ene.health -= 1
                if ene.health == 0:
                    pixel.all_enemies.remove(ene)
                    kills += 1
                    print("KILLED", kills)
                    if kills == 10: # DRC 2 time
                        drc_hud = pygame.image.load("assets/drc_txts/drc_2.png")
                        zcd_length = 3800
                        bcd_length = 8000
                    if kills == 20: # DRC 3 time
                        drc_hud = pygame.image.load("assets/drc_txts/drc_3.png")
                        zcd_length = 2600
                        bcd_length = 5000
                    if kills == 30: # DRC 4 time
                        drc_hud = pygame.image.load("assets/drc_txts/drc_4.png")
                        zcd_length = 1400
                        bcd_length = 2000
                    if kills == 40: # DRC 5 time
                        drc_hud = pygame.image.load("assets/drc_txts/drc_4.png")
                        zcd_length = 1000
                        bcd_length = 1000
                    if kills == 50: # Win (for now)
                        stage == "win"
                    del ene
                pixel.all_checks.remove(pix)
                del pix
                i-=1
                break
            j+=1
        i+=1
    # Step 2: Did the enemies eat the player?
    p_hb = player.get_hitbox()
    i = 0
    while i < len(pixel.all_enemies):
        e_hb = pixel.all_enemies[i].get_hitbox()
        if p_hb.check_hit(e_hb):
            print("DEAD")
            stage = "gameover"
        i+=1

def spawn_enemies():
    global zombie_cd, zcd_length, brute_cd, bcd_length
    if pygame.time.get_ticks() - zombie_cd > zcd_length:
        zombie_cd = pygame.time.get_ticks()
        spawn_enemy("z")
    if pygame.time.get_ticks() - brute_cd > bcd_length:
        brute_cd = pygame.time.get_ticks()
        spawn_enemy("b")

def spawn_enemy(type: str):
    new = -1
    if type == "z":
        new = pixel.Character(sprites.warning_zombie, True, 0.3)
    else:
        new = pixel.Character(sprites.error_brute, True, 0.1, 3)
    loc = random.choice(pixel.spawns)
    new.move(loc[0], loc[1])

def pygame_stuff():
    screen.fill((0, 0, 0))
    draw_stage()
    if arduino_mode:
        read_ard()
        arduino_events()
    else:
        event_catcher()
    if stage == "game":
        spawn_enemies()
        move_character()
        move_enemies()
        move_projectiles()
        check_collisions()
    clock.tick(fps)
    pygame.display.flip()

while True:
    '''Inf loop for Pygame functionality.'''
    pygame_stuff()
