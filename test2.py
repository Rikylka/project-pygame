import pygame
import os
import sys
pygame.init()
FPS = 30
WIDTH, HEIGHT = 630, 450
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

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

class Borders(pygame.sprite.Sprite):
    image = load_image("borders.png")
    def __init__(self):

        super().__init__(all_sprites)
        self.image = Borders.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = HEIGHT + 10
        self.rect.left = -10

class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 400


class Landing(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.move_ball = [1, 1]
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.x += self.move_ball[0] * 2
        self.rect.y += self.move_ball[1] * 2

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            self.move_ball[1] *= -1

        #проверка на стены
        if not 0 <= self.rect.x <= WIDTH - 20:
            self.move_ball[0] *= -1
        if not 60 <= self.rect.y <= HEIGHT - 20:
            self.move_ball[1] *= -1

        self.rect.x += self.move_ball[0] * 2
        self.rect.y += self.move_ball[1] * 2

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x * 70, pos_y * 50 + 50)


def generator_briks(level):
    screen.fill('black')
    n_walls = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
                n_walls += 1
    return n_walls

pygame.display.set_caption('Десант')

all_sprites = pygame.sprite.Group()
player = Player()
borders = Borders()

tile_images = {
        'wall': load_image('brick.png'),
    }

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Landing(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= 25
            if event.key == pygame.K_RIGHT:
                player.rect.x += 25
    screen.fill('black')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
