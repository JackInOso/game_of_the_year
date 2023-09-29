import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # Virgin ship
    def __init__(self, game_settings, screen):
        super(Ship, self).__init__()

        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value of the ship's center
        self.center = float(self.rect.centerx)
        self.center2 = float(self.rect.centery)

        # Movement status set
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.center2 -= self.game_settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center2 += self.game_settings.ship_speed
        self.rect.centerx = self.center
        self.rect.centery = self.center2

    def blitme(self):
        # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.center2 = self.screen_rect.bottom - self.rect.height / 2

