In your classic hack and slash games, you click to move. This means
your control over your character is not as _immediate_ as other action
games.

What we're going to do is make it so our player has a target point,
then moves towards it every frame.

    from ppb import Vector

    class Player(DirtySprite):

        def __init__(self, scene, target=None):
            super().__init__(scene.groups["player"])
            self.image = image.load(path.join(path.dirname(__file__),
                                              "player.png"))
            self.rect = self.image.get_rect()
            self.position = Vector(*self.rect.center)
            self.scene = scene
            self.target = target
            self.speed = 25

        def update(self, time_delta):
            if self.target is not None:
                move_path = self.target - self.position
                self.position += move_path.scale(self.speed * time_delta)
                self.rect.center = tuple(int(x) for x in self.position)
                self.dirty = True

In our Scene, we're going to move our player from the top left corner
down to the bottom right.

    class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        Player(self, target=Vector(750, 750))

And running our game, we see our sprite lazily move towards the far
corner.
