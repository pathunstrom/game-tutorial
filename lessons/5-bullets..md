# Bang Bang

Next, let's add bullets to the game.

## sprites.py

First, we're going to take all of the base code for `Player` and make it a 
`BaseSprite`.

    class BaseSprite(DirtySprite):
    group = None
    image_path = None
    image = None

    def __init__(self, scene):
        cls = self.__class__
        super().__init__(scene.groups[cls.group])
        if cls.image is None:
            cls.image = image.load(path.join(IMG_PATH, cls.image_path))
        self.rect = self.image.get_rect()
        self.scene = scene

    def update(self, *args):
        self.dirty = True
    
    
    class Player(BaseSprite):
        group = "player_group"
        image_path = "player.png"

        def update(self, *args):
            super().update(*args)
            mouse_x, mouse_y = mouse.get_pos()
            diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
            diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
            self.rect.centerx += diff_x
            self.rect.centery += diff_y

Then we make our new bullet.

    class Bullet(BaseSprite):
        group = "bullet_group"
        image_path = "bullet.png"
        
        def __init__(self, scene, tail_position):
            super().__init__(scene)
            self.rect.midbottom = tail_position
        
        def update(self, *args):
            super().update(*args)
            self.rect.centery += -6
            if self.rect.bottom < self.scene.play_area:
                self.kill()

We check to see if the bullet is totally off screen then kill it to prevent
keeping extra bullets in memory.

Remember that negative y is "up."

## scenes.py

Let's test it by spawning it in the bottom of the screen:

    def __init__(engine, **kwargs):
        . . .
        sprites.Player(self)
        sprites.Bullet(self, self.play_area.midbottom)

It works! Now to make it fire when you click.

## sprites.py

We'll modify `Player.update`

    def update(self, *args):
        super().update(*args)
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y
        
        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0]:
            Bullet(self.scene, self.rect.midtop)

That _almost_ works.
