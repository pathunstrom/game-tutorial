from abc import ABC
from abc import abstractmethod
import logging
from math import hypot
from os import path
import random

from ppb import BaseScene
from ppb import GameEngine
from ppb import Vector
from pygame import image
from pygame import mouse
from pygame.sprite import DirtySprite


# ABCs

class TargetABC(ABC):

    @property
    @abstractmethod
    def position(self) -> Vector:
        pass

    @abstractmethod
    def interact(self, player: 'Player'):
        logging.getLogger(type(self).__name__).debug(f"{type(self).__name__} reached!")


# Scenes

class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)

        chest = ClosedChest(self, Vector(750, 750))
        player = Player(self, chest)
        Enemy(self, Vector(600, 600), player)
        self.groups["terrain"].empty()

        self.controller = Controller(player, self.groups["interact"])

    def simulate(self, time_delta: float):
        self.controller.respond()
        super().simulate(time_delta)


# Game Objects

class ClosedChest(DirtySprite, TargetABC):
    def __init__(self, scene, position: Vector) -> None:
        super().__init__(scene.groups["interact"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "chest_closed.png"))
        self.rect = self.image.get_rect()
        self.rect.center = tuple(position)
        self._position = position
        self.dirty = 1
        self.scene = scene

    @property
    def position(self):
        return self._position

    def interact(self, player):
        OpenChest(self.scene, self.position)
        self.kill()


class Enemy(DirtySprite, TargetABC):
    def __init__(self, scene, position: Vector, player: 'Player'):
        super().__init__(scene.groups["interact"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = tuple(position)
        self._position = position
        self.direction = Vector(0, 1).rotate(random.randint(0, 359))
        self.dirty = 1
        self.scene = scene
        self.speed = 30
        self.reach = 20
        self.sense_limit = 200
        self.player = player

    @property
    def position(self):
        return self._position

    def interact(self, player: 'Player'):
        logging.getLogger(type(self).__name__).debug("Enemy killed.")
        self.kill()

    def update(self, time_delta):
        direction_to_player = self.player.position - self.position
        distance_to_player = direction_to_player.length
        if distance_to_player < self.reach:
            pass
        elif distance_to_player < self.sense_limit:
            self._position += direction_to_player.scale(self.speed * time_delta)
        else:
            self.direction = self.direction.rotate(random.randint(-2, 2))
            self._position += self.direction.scale(self.speed * time_delta * .5)
        self.rect.center = tuple(self.position)
        self.dirty = 1


class OpenChest(DirtySprite):
    def __init__(self, scene, position: Vector):
        super().__init__(scene.groups["terrain"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "chest_open.png"))
        self.rect = self.image.get_rect()
        self.rect.center = tuple(position)
        self.position = position
        self.dirty = 1
        self.scene = scene


class Player(DirtySprite):

    def __init__(self, scene, target: TargetABC=None):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.position = Vector(*self.rect.center)
        self.scene = scene
        self._target = target
        self.speed = 120
        self.reach = hypot(0.5 * self.image.get_height(),
                           0.5 * self.image.get_width())

    @property
    def target(self) -> TargetABC:
        return self._target

    @target.setter
    def target(self, target: TargetABC):
        self._target = target

    def update(self, time_delta):
        if self.target is not None:
            move_path = self.target.position - self.position
            if move_path.length < self.reach:
                self.target = self.target.interact(self)
                self.target = None
            else:
                self.position += move_path.scale(self.speed * time_delta)
                self.rect.center = tuple(int(x) for x in self.position)
                self.dirty = True


# Utility classes

class Controller:

    def __init__(self, player: Player, targets):
        self.player = player
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
            self.player.target = target
        if not mouse_buttons[0] and self.button_pressed:
            self.button_pressed = False


class EmptyTarget:

    def __init__(self, position: Vector):
        self.position = position

    def interact(self, player):
        logging.getLogger(type(self).__name__).debug(f"{type(self).__name__} reached!")


TargetABC.register(EmptyTarget)


def main():
    with GameEngine(Game, resolution=(800, 800), log_level=logging.DEBUG) as engine:
        engine.run()

if __name__ == "__main__":
    main()
