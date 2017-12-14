import logging
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
        chest = ClosedChest(self, Vector(750, 750))
        player = Player(self, chest)
        self.controller = Controller(player, self.groups["interact"])

    def simulate(self, time_delta: float):
        self.controller.respond()
        super().simulate(time_delta)


class ClosedChest(DirtySprite):
    def __init__(self, scene, position: Vector):
        super().__init__(scene.groups["interact"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "chest_closed.png"))
        self.rect = self.image.get_rect()
        self.rect.center = tuple(position)
        self.position = position
        self.dirty = 1
        self.scene = scene

    def interact(self, actor):
        logging.debug("Chest opened!")


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
            move_path = self.target.position - self.position
            if move_path.length < self.reach:
                self.target = None
            else:
                self.position += move_path.scale(self.speed * time_delta)
                self.rect.center = tuple(int(x) for x in self.position)
                self.dirty = True


class Controller:

    def __init__(self, actor, targets):
        self.actor = actor
        self.targets = targets
        self.button_pressed = False

    def respond(self):
        mouse_buttons = mouse.get_pressed()
        mouse_position = mouse.get_pos()
        if mouse_buttons[0] and not self.button_pressed:
            self.button_pressed = True
            target = EmptyTarget(Vector(*mouse_position))
            for sprite in self.targets.sprites():
                if sprite.rect.collidepoint(mouse_position):
                    target = sprite
                    break
            self.actor.target = target
        if not mouse_buttons[0] and self.button_pressed:
            self.button_pressed = False


class EmptyTarget:
    def __init__(self, position: Vector):
        self.position = position


def main():
    with GameEngine(Game, resolution=(800, 800), log_level=logging.DEBUG) as engine:
        engine.run()

if __name__ == "__main__":
    main()
