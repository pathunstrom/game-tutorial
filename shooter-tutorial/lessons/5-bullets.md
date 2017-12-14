# Bullets

Now we can move, but what good is a shooter if you can't shoot
something? Of course, it's hard to shoot something if you don't have
something to shoot.

So let's add a projectile!

So, first, let's get our projectile image. Same as last time, if you
didn't bring one, the repo has one available. `bullet.png` is ready for
use.

Let's copy our Player object's basic setup:

    class Bullet(DirtySprite):

        def __init__(self, scene):
            super().__init__(scene.groups["bullets"])
            b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
            self.image = b_image
            self.rect = self.image.get_rect()
            self.rect.bottom = 600
            self.scene = scene

    def update(self, time_delta):
        self.rect.centery += -10
        self.dirty = True

Next, let's add bullets to the Game.

    class Game(BaseScene):

        def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
            super().__init__(engine=engine,
                             background_color=background_color,
                             **kwargs)
            Player(self)
            Bullet(self)

Try running this and see what happens.

Now, we don't want to instantiate these when the game starts, so let's
make a few changes to Bullet and Player.

    class Bullet(DirtySprite):

        def __init__(self, scene, position):
            super().__init__(scene.groups["bullets"])
            b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
            self.image = b_image
            self.rect = self.image.get_rect()
            self.rect.midbottom = position  # Modify this
            self.scene = scene

So here we need to change how we instantiate Bullet, by telling where
to spawn.

    class Player(DirtySprite):

        def __init__(self, scene):
            . . .
            self.scene = scene
            self.bullet_limiter = 0.25
            self.bullet_delay = 0

        def update(self, time_delta):
            . . .
            if diff_x or diff_y:
                self.dirty = True

            pressed = mouse.get_pressed()
            if pressed[0] and self.bullet_delay > self.bullet_limiter:
                Bullet(self.scene, self.rect.midtop)
                self.bullet_delay = 0
            self.bullet_delay += time_delta

There's only one more thing we need to do. Because BaseScene uses a
defaultdict to guarantee you can always access the containers you need.
Unfortunately, that means if you try to access it during updating, it
changes the size of the dictionary. So let's trick it into making the
group exist!

    class Game(BaseScene):

        def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
            super().__init__(engine=engine,
                             background_color=background_color,
                             **kwargs)
            Player(self)
            Bullet(self, (0, 0)).kill()

And now you should be able to see your new bullet in action!
