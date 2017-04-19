from ppb import BaseScene

import sample.sprites as sprites


class Game(BaseScene):
    def __init__(self, engine, **kwargs):
        super().__init__(engine=engine,
                         background_color=(45, 30, 55),
                         **kwargs)
        self.play_area = engine.display.get_rect()
        sprites.Player(self)
        sprites.Bullet(self, self.play_area.midbottom)

    def change(self):
        return not self.running, {}
