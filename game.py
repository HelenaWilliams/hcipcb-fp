import pygame
import pixel

pygame.init()
pygame.font.init()

sw = 1280 # Fake OLED screen--each "pixel" is 10x10 px
sh = 640
screen = pygame.display.set_mode((sw, sh))
font = pygame.font.Font(size=70)
clock = pygame.time.Clock()
fps = 30

cyan = (0, 255, 255)
yellow = (255, 255, 0)

t1 = pixel.Pixel(5, 5)
t2 = pixel.Pixel(6, 5)
t3 = pixel.Pixel(5, 6)
t4 = pixel.Pixel(6, 6)

test = pixel.Character([[0, 0], [1, 1], [2, 2], [3, 3]])

while True:
    '''Inf loop for Pygame and Arduino listening'''
    screen.fill((0, 0, 0))
    # t1.move(0, 1)
    # t1.draw(screen)
    # t2.move(0, 1)
    # t2.draw(screen)
    # t3.move(0, 1)
    # t3.draw(screen)
    # t4.move(0, 1)
    # t4.draw(screen)
    test.draw(screen)
    test.move(0, 1)
    clock.tick(fps)
    pygame.display.flip()