# -*- coding: utf-8 -*-
import fire_dungeon
from credits import Credits
import pygame
import pygame_menu
from db_related import Scores
from utils import *
from create_level import create_level


pygame.init()

FPS = 60
display_info = pygame.display.Info()
clock = pygame.time.Clock()

window_size = window_width, window_height = 800, 800
game_size = g_width, g_height = 800, 800

main_menu = None
credits, game, loading = False, False, False
surface = pygame.display.set_mode(window_size)

background_image = pygame_menu.baseimage.BaseImage(
    image_path=get_data_path('background.png', 'img'))

pygame.mixer.init()


def draw_background():
    background_image.draw(surface)


def loaded():
    global loading
    loading = False


def game_over():
    global game
    game = False


def start_the_game_from_menu():
    global game
    global loading
    game = True
    loading = True


def main():
    global game
    global loading
    pygame.mixer.music.load(get_data_path('menu_theme.wav', 'music'))
    pygame.mixer.music.play(-1)

    main_menu = pygame_menu.Menu(300, 300, 'Fire Dungeon',
                                 theme=pygame_menu.themes.THEME_BLUE)
    scores_menu = Scores(window_width, window_height)
    main_menu.add_button('Play', start_the_game_from_menu)

    main_menu.add_button('Scores', scores_menu.menu)

    credit_list = [
        "CREDITS - The Departed",
        " ",
        "Leonardo DiCaprio - Billy",
        "Matt Damon - Colin Sullivan",
        "Jack Nicholson - Frank Costello",
        "Mark Wahlberg - Dignam",
        "Martin Sheen - Queenan"]
    c = Credits(credit_list, surface, 'Sigma Five.otf')
    main_menu.add_button('About', c.main)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pass

            if not game:
                main_menu.update(events)

        if not game:
            draw_background()
            if not loading:
                main_menu.draw(surface)
            if loading:
                surface.fill((0, 0, 0))
        else:
            # if loading:
            surface.fill((0, 0, 0))
            level = create_level(31, 31, 1, callback=loaded)
            if not loading:
                fd = fire_dungeon.FireDungeon(
                    level, g_width, g_height, game_over_func=game_over)

                fd.run_game(gravity=False)

        # Credits(credit_list, surface, 'Sigma Five.otf').main()
        pygame.display.update()


if __name__ == '__main__':
    main()
