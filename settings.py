class Settings:
    # Game settings
    def __init__(self):
        # Settings
        self.width = 1200
        self.height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ships_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_max_number = 3

        # Aliens settings
        self.alien_drop_speed = 10

        # Leveling up
        self.speed_up_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initialize settings that can change throughout the game
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 0.5
        self.alien_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        # Increase speed settings
        # self.ship_speed *= self.speed_up_scale
        # self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale

        self.alien_points = int(self.alien_points * self.score_scale)
