from math import hypot
from os import path

from ppb import BaseScene
from ppb import GameEngine
from ppb import Vector
from pygame import image
from pygame import mouse
from pygame.sprite import DirtySprite


class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        Player(self, Vector(750, 750))


class Player(DirtySprite):

    def __init__(self, scene, target=None):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.position = Vector(*self.rect.center)
        self.scene = scene
        self.target = target
        self.speed = 60
        self.reach = hypot(0.5 * self.image.get_height(), 0.5 * self.image.get_width())

    def update(self, time_delta):
        if self.target is not None:
            move_path = self.target - self.position
            if move_path.length < self.reach:
                self.target = None
            else:
                self.position += move_path.scale(self.speed * time_delta)
                self.rect.center = tuple(int(x) for x in self.position)
                self.dirty = True


def main():
    with GameEngine(Game, resolution=(800, 800)) as engine:
        engine.run()

if __name__ == "__main__":
    main()
