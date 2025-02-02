import os
import sys

import pygame

FPS = 50
WIDTH, HEIGHT = 630, 450

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


def final_screen(result, n_wall):
    if result == 0:
        intro_text = ["Вы проиграли!", "",
                      f"Ваш счёт: {n_wall}",]
        fon_jpg = 'fon_fall.jpg'
    else:
        intro_text = ["Вы выиграли!!", "",]
        fon_jpg = 'fon_win.jpg'

    fon = pygame.transform.scale(load_image(fon_jpg), (WIDTH, HEIGHT))
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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
itog = 0
n_wall = 20

final_screen(itog, n_wall)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill('black')
    pygame.display.flip()
    clock.tick(FPS)
