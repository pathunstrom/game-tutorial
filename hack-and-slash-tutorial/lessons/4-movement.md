In your classic hack and slash games, you click to move. This means
your control over your character is not as _immediate_ as other action
games.

What we're going to do is make it so our player has a target point,
then moves towards it every frame, until it reaches it.

First we need to add some imports.

    from ppb import Vector
    from math import hypot

And now let's modify our `Player` sprite's `__init__`.

    class Player(DirtySprite):

        def __init__(self, scene, target=None):
            . . .
            self.position = Vector(*self.rect.center)
            self.target = target
            self.speed = 60
            self.reach = hypot(0.5 * self.image.get_height(),
                               0.5 * self.image.get_width())

These values will get used in our movement code. Let's add an update
function to our sprite.

    class Player(DirtySprite):
        . . .
        def update(self, time_delta):
            if self.target is not None:
                move_path = self.target - self.position
                if move_path.length < self.reach:
                    self.target = None
                else:
                    self.position += move_path.scale(self.speed * time_delta)
                    self.rect.center = tuple(int(x) for x in self.position)
                    self.dirty = True

This will have our sprite move to its target, then stop when it gets
close enough.

In our Scene, we're going to set the Player's target to a point in the
bottom right corner of the screen.

    class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        Player(self, target=Vector(750, 750))

And running our game, we see our sprite lazily move towards the far
corner.
