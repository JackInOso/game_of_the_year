import pygame
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import settings
import ship
import game_functions as gf
import alien


def run_game():

    pygame.init()
    game_settings = settings.Settings()
    screen = pygame.display.set_mode((game_settings.width, game_settings.height))
    pygame.display.set_caption('Alien Invasion')

    # Make the play button
    play_button = Button(game_settings, screen, "Play")

    # Game score and stats
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    # Make a ship, a group of bullets and aliens
    player = ship.Ship(game_settings, screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(game_settings, screen, player, aliens)

    # Make an alien DELETE
    enemy = alien.Alien(game_settings, screen)

    # Start the main loop
    while True:
        gf.check_events(game_settings, screen, stats, sb, play_button, player, aliens, bullets)
        if stats.game_active:
            player.update()
            gf.update_aliens(game_settings, stats, screen, sb, player, aliens, bullets)
            gf.update_bullets(game_settings, screen, stats, sb, player, aliens, bullets)
        gf.update_screen(game_settings, screen, stats, sb, player, aliens, bullets, play_button)


run_game()
