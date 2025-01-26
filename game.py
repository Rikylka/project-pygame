import os
import sys
import pygame

FPS = 30
WIDTH, HEIGHT = 630, 450

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

# закрытие игры
def terminate():
    pygame.quit()
    sys.exit()


# уровень
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# отрисовка квадратов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x * 70, pos_y * 50 + 50)


# подсчёт кол-во блоков
def number_of_walls(level):
    kol_wall = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                kol_wall += 1
    return kol_wall

def break_walls(level, ball_xy, move_ball):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                if x * 70 + 10 <= ball_xy[0] <= x * 70 + 80 and y * 50 + 60 <= ball_xy[1] <= y * 50 + 100:
                    level[y] = level[y][:x] + "." + level[y][x+1:]
                    if x * 70 + 10 <= ball_xy[0] <= x * 70 + 80:
                        move_ball[0] *= -1

                    if y * 50 + 60 <= ball_xy[1] <= y * 50 + 100:
                        move_ball[1] *= -1
    return [level, move_ball]



# генерация лвл
def generate_level(screen, level):
    screen.fill('black')
    n_walls = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
                n_walls += 1
    return n_walls


# игра
def game(level, n_wall, tiles_group):
    x_player = 250
    y_player = 400
    sprite.rect.x = 350
    sprite.rect.y = 350
    move_ball = [-1, -1]
    r = 10
    v = 150
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # движение платформы
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_player > 0:
                    x_player -= 25
                if event.key == pygame.K_RIGHT and x_player < 500:
                    x_player += 25
        screen.fill('black')

        # движение шарика
        ball_xy[0] += move_ball[0] * v / FPS
        ball_xy[1] += move_ball[1] * v / FPS

        # уничтожение блоков
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    if x * 70 + 10 <= ball_xy[0] <= x * 70 + 80 and y * 50 + 60 <= ball_xy[1] <= y * 50 + 100:
                        level[y] = level[y][:x] + "." + level[y][x + 1:]
                        if y * 50 + 60 <= ball_xy[1] <= y * 50 + 100:
                            move_ball[1] *= -1
                        else:
                            move_ball[0] *= -1

        # генерация блоков
        n_wall_now = generate_level(screen, level)
        tiles_group.draw(screen)

        # отталкивание от стен
        if not 0 <= sprite.rect.x <= 440:
            move_ball[0] *= -1
        if not r + 50 <= ball_xy[1] <= HEIGHT - r - 1:
            move_ball[1] *= -1
        pygame.draw.circle(screen, 'white', (int(ball_xy[0]), int(ball_xy[1])), r)

        # отталкивание от игрока
        if x_player <= ball_xy[0] <= x_player + 150 and ball_xy[1] <= y_player <= ball_xy[1] + 20:
            move_ball[1] *= -1

        #надпись
        font = pygame.font.Font(None, 30)
        text = font.render(f"Количество сломанных блоков:{n_wall - n_wall_now}", True, "white")
        screen.blit(text, (10, 20))

        pygame.draw.rect(screen, 'white', (x_player, y_player, 150, 20))
        clock.tick(FPS)
        pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('игра')
    clock = pygame.time.Clock()

    #агрузка изображений
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('brick.png'),
    }
    player_image = load_image('player.png')
    ball_imager = load_image('player.png')
    tile_width, tile_height = 70, 50

    # загрузка лвл
    level = load_level('test.txt')
    n_wall = number_of_walls(level)
    game(level, n_wall, tiles_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
