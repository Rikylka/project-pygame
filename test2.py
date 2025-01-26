import pygame
import os
import sys

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


class Mountain(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 400


class Landing(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.move_ball = [0, 1]
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.x += self.move_ball[0] * 1
        self.rect.y += self.move_ball[1] * 1

    def update(self):
        if pygame.sprite.collide_mask(self, mountain):
            self.move_ball = [0, -1]
        self.rect.x += self.move_ball[0] * 1
        self.rect.y += self.move_ball[1] * 1

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Десант')

all_sprites = pygame.sprite.Group()
mountain = Mountain()

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
                mountain.rect.x -= 25
            if event.key == pygame.K_RIGHT:
                mountain.rect.x += 25
    screen.fill('black')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
