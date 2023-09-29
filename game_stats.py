class GameStats:

    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        with open('record.txt') as inp:
            self.high_score = int(inp.readline())
        self.level=  1

    def reset_stats(self):
        self.ships_left = self.game_settings.ships_limit
        self.score = 0