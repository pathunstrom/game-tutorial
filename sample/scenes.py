from ppb import BaseScene
from pygame.sprite import groupcollide

import sample.sprites as sprites


def simple_enemies(time_step, x_val):
    time = time_step
    while True:
        yield time, x_val
        time += time_step


class Game(BaseScene):
    def __init__(self, engine, **kwargs):
        super().__init__(engine=engine,
                         background_color=(45, 30, 55),
                         **kwargs)
        self.play_area = engine.display.get_rect()
        self.run_time = 0
        self.spawn = simple_enemies(1.5, 200)
        self.next_spawn, self.next_x = next(self.spawn)
        _ = self.groups[sprites.Bullet.group]  # force setting the key.
        sprites.Player(self)

    def simulate(self, time_delta):
        self.run_time += time_delta
        while self.next_spawn <= self.run_time:
            sprites.Enemy(self, self.next_x)
            self.next_spawn, self.next_x = next(self.spawn)
        super().simulate(time_delta)
        player = self.groups[sprites.Player.group]
        bullets = self.groups[sprites.Bullet.group]
        enemies = self.groups[sprites.Enemy.group]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, bullets, True, True)

    def change(self):
        return not self.running, {}
