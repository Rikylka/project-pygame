import pygame
import sys
import os

pygame.init()
size = width, height = 630, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Столкновение шариков')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


""" def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(350, 350, 2 * radius, 2 * radius)
        self.vx = 2
        self.vy = 2"""


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, *pos):
        super().__init__(all_sprites)
        self.move_ball = [1, 1]
        self.image = Ball.image
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.movex = -1
        self.movey = -1

    def update(self):
        #self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.movey = -self.movey
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.movex = -self.movex
        self.rect = self.rect.move(self.movex, self.movey)

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x * 70, pos_y * 50 + 50)
        Border(pos_x * 70, pos_y * 50 + 50, pos_x * 70 + 70, pos_y * 50 + 50)
        Border(pos_x * 70, pos_y * 50 + 50, pos_x * 70, pos_y * 50 + 90)
        Border(pos_x * 70, pos_y * 50 + 90, pos_x * 70 + 70, pos_y * 50 + 90)
        Border(pos_x * 70 + 70, pos_y * 50 + 50, pos_x * 70 + 70, pos_y * 50 + 90)


def generator_briks(level):
    n_walls = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
                n_walls += 1
    return n_walls


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('brick.png'),
}
Border(0, 50, width, 5)
Border(0, height, width, height)
Border(0, 50, 5, height)
Border(width, 50, width, height)

Ball([300, 300])
level = load_level('test.txt')
n_wall = generator_briks(level)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
