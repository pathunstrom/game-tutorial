# Building Sprites

Now you need something to draw.

## sprites.py

    from os import path
    
    from pygame import image
    from pygame.sprite import DirtySprite
    
    IMG_PATH = path.join(path.dirname(__file__), "resources", "img")