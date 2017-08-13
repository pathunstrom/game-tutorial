# Building Sprites

Now you need something to draw.

## sprites.py

    from os import path

    from pygame import image
    from pygame.sprite import DirtySprite
    
    IMG_PATH = path.join(path.dirname(__file__), "img")
    
    
    class Player(DirtySprite):
        group = "player_group"
        image_path = "player.png"
        image = None
    
        def __init__(self, scene):
            super().__init__(scene.groups[Player.group])
            if Player.image is None:
                Player.image = image.load(path.join(IMG_PATH, Player.image_path))
            self.rect = self.image.get_rect()
            self.scene = scene
    
        def update(self, *args):
            self.dirty = True

PPB sprites are based on Pygame sprites, and Pygame sprites need two things: an
image and a rectangle, called `image` and `rect`.

This implementation uses the flywheel pattern to limit the number of images you
need floating around to one per class.

The `update` function currently requires the `self.dirty == True` due to an
engine bug.

## scenes.py

    import mygame.sprites as sprites

First we need to import the sprites module.

    def __init__(self, engine, **kwargs):
        super().__init__(engine=engine,
                         background_color=(45, 30, 55),
                         **kwargs)
        sprites.Player(self)

Then we instantiate a Player during the scene set up, then run your game again.

Your sprite sits in the top left corner because a rectangle obtained from
`get_rect` returns a rectangle at the origin.

Try changing that by setting `Player.rect.center` to a new tuple value.