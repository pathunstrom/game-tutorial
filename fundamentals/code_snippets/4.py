from os import path

from ppb import BaseScene, GameEngine
from pygame import image
from pygame.sprite import DirtySprite

class Player(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.scene = scene

class Game(BaseScene):

  def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
      super().__init__(engine=engine,
                       background_color=background_color,
                       **kwargs)
      Player(self)