import os
import sys

import pygame

FPS = 50
WIDTH, HEIGHT = 550, 550

def start_screen():
    intro_text = ["МЕНЮ", "",
                  "Правила игры",
                  "Нажмите любую клавишу что бы начать игру",
                  "Что бы выбрать уровень нажмите соответсующую цифру"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = "LOL.txt"
                    return level
                elif event.key == pygame.K_2:
                    level = "map.txt"
                    return level
                elif event.key == pygame.K_3:
                    level = "map2.txt"
                    return level
        pygame.display.flip()
        clock.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()


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


def start_screen():
    intro_text = ["МЕНЮ", "",
                  "Правила игры",
                  "Нажмите любую клавишу что бы начать игру",
                  "Что бы выбрать уровень нажмите соответсующую цифру"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 'LOL.txt'
                    return level
                if event.key == pygame.K_2:
                    level = 'map.txt'
                    return level
                if event.key == pygame.K_3:
                    level = 'map2.txt'
                    return level
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))

    print(list(map(lambda x: x.ljust(max_width, '.'), level_map)))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move(obj, direction):
    x, y = obj.pos
    if direction == 'left' and x > 0 and level[y][x - 1] != '#':
        obj.move(x - 1, y)
    if direction == 'right' and x < level_x and level[y][x + 1] != '#':
        obj.move(x + 1, y)
    if direction == 'up' and y > 0 and level[y - 1][x] != '#':
        obj.move(x, y - 1)
    if direction == 'down' and y < level_y and level[y + 1][x] != '#':
        obj.move(x, y + 1)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
level_name = start_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png', -1)

tile_width = tile_height = 50
level = load_level(level_name)
player, level_x, level_y = generate_level(level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(player, 'left')
            if event.key == pygame.K_RIGHT:
                move(player, 'right')
            if event.key == pygame.K_UP:
                move(player, 'up')
            if event.key == pygame.K_DOWN:
                move(player, 'down')
    screen.fill('black')
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
