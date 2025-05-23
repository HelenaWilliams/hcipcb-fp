import pygame
import sprites

all_pixels = []
all_verts = []
all_enemies = []
all_checks = []
spawns = []

def move_all(x: int, y:int):
    if x == y:
        x *= 0.7
        y *= 0.7
    for i in all_pixels:
        i.move(x, y)
    for i in all_verts:
        i.move(x, y)
    for i in all_enemies:
        i.get_hitbox().move(x, y)
    for i in spawns:
        i[0] += x
        i[1] += y

class Pixel:
    '''Abstracts away the nitty-gritty of maintaining a perfect pixel system.'''
    def __init__(self, x: int, y:int, opaque=True):
        self.rect = pygame.Rect(x*10, y*10, 10, 10)
        self.x = x
        self.y = y
        self.opaque = opaque
        self.set_color()
        all_pixels.append(self)
    
    def set_color(self):
        '''Updates color to reflect Adafruit display paradigm.'''
        if self.y < 16:
            self.color = (255, 255, 0)
        else:
            self.color = (0, 255, 255)

    def move(self, x: int, y: int):
        '''Moves pixel on screen.'''
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x*10, self.y*10, 10, 10)
    
    def draw(self, screen: pygame.display):
        '''Renders pixel on screen.'''
        self.set_color()
        if self.opaque:
            pygame.draw.rect(screen, self.color, self.rect)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Character:
    '''Further abstracts drawing by enabling control of multiple pixels simultaneously.'''
    def __init__(self, pixels: list, enemy = True, speed = 1, health = 1):
        self.health = health
        self.pixels = [] # Pixels that belong to this character
        s_x = pixels[0][0]
        s_y = pixels[0][1]
        l_x = pixels[0][0]
        l_y = pixels[0][1]
        for i in pixels:
            new_px = Pixel(i[0], i[1])
            if i[0] < s_x:
                s_x = i[0]
            if i[0] > l_x:
                l_x = i[0]
            if i[1] < s_y:
                s_y = i[1]
            if i[1] > l_y:
                l_y = i[1]
            self.pixels.append(new_px)
        self.center_px = self.pixels[0]
        self.speed = speed
        if (enemy):
            all_enemies.append(self)
        self.hitbox = Hitbox(s_x, s_y, (l_x - s_x), (l_y - s_y))
    
    def move(self, x: int, y: int):
        for i in self.pixels:
            i.move(x, y)
        self.hitbox.move(x, y)
    
    def draw(self, screen: pygame.display):
        for i in self.pixels:
            i.draw(screen)

    def get_center(self):
        return self.center_px.rect.center
    
    def get_hitbox(self):
        return self.hitbox

    def spawn_proj(self, type, x, y):
        new_proj = -1
        if type == "check":
            new_proj = Character(sprites.projectile_check, False, 2)
            new_proj.move(64, 32)
            new_proj.x_dir = x
            new_proj.y_dir = y
            all_checks.append(new_proj)
   
class HorizPixel(Pixel):
    '''Abstracts drawing straight horizontal lines, since they're predictable.'''
    def __init__(self, x: int, y:int, width: int, opaque=True):
        self.rect = pygame.Rect(x*10, y*10, width*10, 10)
        self.x = x
        self.y = y
        self.width = width
        self.opaque = opaque
        self.set_color()
        all_pixels.append(self)

    def move(self, x: int, y: int):
        '''Moves pixel on screen.'''
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x*10, self.y*10, self.width*10, 10)
    
class VertPixel():
    '''Abstracts drawing straight vertical lines by manually drawing two rectangles so we can keep the cool Adafruit monitor effect. Technically breaks my rules, but drawing these out of individual pixels caused glitchy effects.'''
    def __init__(self, x: int, y:int, height: int):
        self.x = x
        self.y = y
        self.height = height
        self.set_sides()
        all_verts.append(self)

    def set_sides(self):
        self.blue_side = pygame.Rect(self.x*10, self.y*10, 10, self.height*10)
        if self.y >= 16: # All of it is in the blue zone
            self.yellow_side = pygame.Rect(self.x*10, self.y*10, 10, 0)
        elif self.y + self.height < 16: # All of it is in the yellow zone
            self.yellow_side = pygame.Rect(self.x*10, self.y*10, 10, self.height*10)
        else: # Half and half... ugh.
            self.yellow_side = pygame.Rect(self.x*10, self.y*10, 10, (16-self.y)*10)


    def draw(self, screen: pygame.display):
        pygame.draw.rect(screen, (0, 255, 255), self.blue_side)
        pygame.draw.rect(screen, (255, 255, 0), self.yellow_side)

    def move(self, x: int, y:int):
        self.x += x
        self.y += y
        self.set_sides()
        
    def get_center(self):
        return (self.x + 5, self.y + self.height/2)

    def get_x(self):
        return self.get_center()[0]
    
    def get_y(self):
        return self.get_center()[1]

class Hitbox:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x*10, y*10, width*10 + 10, height*10 + 10)
    
    def check_hit(self, other):
        if self.rect.colliderect(other.rect):
            return True
        return False

    def move(self, x, y):
        self.rect.x = self.rect.x + x*10
        self.rect.y = self.rect.y + y*10
