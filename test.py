import os
import sys
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
FPS = 30
WIDTH, HEIGHT = 630, 450

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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


def game(level, n_wall, tiles_group, sprite_ball, sprite_player, sprite_brick):
    sprite_player.rect.x = 250
    sprite_player.rect.y = 400
    sprite_ball.rect.x = 350
    sprite_ball.rect.y = 350
    move_ball = [-1, -1]
    v = 150
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # движение платформы
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sprite_player.rect.x -= 25
                if event.key == pygame.K_RIGHT:
                    sprite_player.rect.x += 25
        screen.fill('black')

        # движение шарика
        sprite_ball.rect.x += move_ball[0] * v / FPS
        sprite_ball.rect.y += move_ball[1] * v / FPS

        # уничтожение блоков


        # генерация блоков
        n_wall_now = generator_briks(level)
        tiles_group.draw(screen)

        # отталкивание от стен
        if not 0 <= sprite_ball.rect.x <= WIDTH - 20:
            move_ball[0] *= -1
        if not 50 <= sprite_ball.rect.y <= HEIGHT - 20:
            move_ball[1] *= -1

        # отталкивание от игрока


        # надпись
        font = pygame.font.Font(None, 30)
        text = font.render(f"Количество сломанных блоков:{n_wall - n_wall_now}", True, "white")
        screen.blit(text, (10, 20))

        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('игра')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

# создадим спрайт
sprite_brick = pygame.sprite.Sprite()
sprite_ball = pygame.sprite.Sprite(all_sprites)
sprite_player = pygame.sprite.Sprite(all_sprites)

# определим его вид
sprite_brick.image = load_image("brick.png")
sprite_ball.image = load_image("ball.png")
sprite_player.image = load_image("player.png")

# и размеры
sprite_brick.rect = sprite_brick.image.get_rect()
sprite_ball.rect = sprite_ball.image.get_rect()
sprite_player.rect = sprite_player.image.get_rect()

tile_images = {
    'wall': load_image('brick.png')
}

level = [".#######.", '#########', '#########', '.#######.']
n_wall = generator_briks(level)
game(level, n_wall, tiles_group, sprite_ball, sprite_player, sprite_brick)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
