# Building Sprites

Now let's draw something. You should have a sprite for your player, but
if not the resource folder in this repo includes a player.png sourced
from kenney.nl/assets.

Using that, we're going to draw our player.

First put your player image into your working directory alongside
`main.py`.

Then, we need a game object. Above our `Game` class, let's make our
`Player`.

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

Now run again.

Your sprite sits in the top left corner because a rectangle obtained
from `get_rect` returns a rectangle with the top left at the origin.

The origin is in the top left because that's how computers render:
unlike the graphs you learn in school with an origin in the bottom left
corner and y values ascending going up the side, the origin of your
computer screen is the top right, and y values ascend going down.

Try experimenting by assigning a tuple to the sprite's rect.center:
`self.rect.center = (200, 300)`
