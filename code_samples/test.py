from os import path

from ppb import BaseScene, GameEngine
from pygame import image
from pygame.sprite import DirtySprite
from pygame import mouse 
from pygame.sprite import groupcollide
from itertools import count 

class Spawner(object):

    def __init__(self, scene, generator, enemy_class):
        self.scene = scene
        self.enemy_class = enemy_class
        self.generator = generator
        self.running = True
        self.time = 0
        self.next_time = None
        self.next_position = None
        self.prime()

    def spawn(self, time_delta):
        self.time += time_delta
        while self.running and self.time >= self.next_time:
            self.enemy_class(self.scene, self.next_position)
            self.prime()

    def prime(self):
        try:
            self.next_spawn, self.next_position = next(self.generator)
        except StopIteration:
            self.running = False

# def simple_infinite_spawn(time_step, x_val):
#     for value in count(1):
#         time = time_step * value
#         yield time, x_val

def file_spawner(file_name):
    with open(path.join(path.dirname(__file__), file_name), "r") as spawn_file:
        spawn_reader = csv.reader(csvfile)
        for row in spawn_reader:
            yield float(row[0]), int(row[1])

class Enemy(DirtySprite):

    def __init__(self, scene, x_position):
        super().__init__(scene.groups["enemy"])
        p_image = image.load(path.join(path.dirname(__file__), "enemy.png"))
        self.image = p_image
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = x_position
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += 3
        self.dirty = True

class Player(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.scene = scene
        self.bullet_limiter = 0.25
        self.bullet_delay = 0

    # def update(self, time_delta):
    #     self.rect.center = mouse.get_pos()
    #     self.dirty = True
    def update(self, *args):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y
        if diff_x or diff_y:
            self.dirty = True
        pressed = mouse.get_pressed()
        if pressed[0] and self.bullet_delay > self.bullet_limiter:
            Bullet(self.scene, self.rect.midtop)
            self.bullet_delay = 0
        time_delta = .1
        self.bullet_delay += time_delta

class Bullet(DirtySprite):

    # def __init__(self, scene):
    #     super().__init__(scene.groups["bullets"])
    #     b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
    #     self.image = b_image
    #     self.rect = self.image.get_rect()
    #     self.rect.bottom = 600
    #     self.scene = scene

    def __init__(self, scene, position):
        super().__init__(scene.groups["bullets"])
        b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
        self.image = b_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = position  # Modify this
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += -10
        self.dirty = True

class Game(BaseScene):

    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine, 
                         background_color=background_color,
                         **kwargs)
    def simulate(self, time_delta):
        super().simulate(time_delta)
        player = self.groups[sprites.Player.group]
        bullets = self.groups[sprites.Bullet.group]
        enemies = self.groups[sprites.Enemy.group]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, bullets, True, True)
        Player(self)
        Bullet(self, (0, 0)).kill()
        # Enemy(self, 200)
        # self.spawner = Spawner(self, simple_infinite_spawn(1.5, 200), Enemy)
        self.spawner = Spawner(self, file_spawner('spawn.csv'), Enemy)
def main():
    with GameEngine(Game, resolution=(400, 600)) as engine:
        engine.run()

if __name__ == "__main__":
    main()