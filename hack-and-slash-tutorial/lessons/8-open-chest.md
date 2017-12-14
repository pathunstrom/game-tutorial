Now let's make the chest open!

First, we're going to add a new sprite: An `OpenChest`:

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

First, this doesn't interact, so we need a new sprite group, which
I've called terrain here. Other than that, this looks exactly like the
other sprites.

Now, in `ClosedChest` let's change interact:

    class ClosedChest(
        def interact(self, player):
            OpenChest(self.scene, self.position)
            self.kill()

We create our new chest, and then kill the `ClosedChest`.

If we run this, we'll run into one problem, though:

    RuntimeError: dictionary changed size during iteration

The reason we get this is because we make a new group in the middle of
our update loop. So we just need to force that group to exist:

    class Game(BaseScene):
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
            . . .
            player = Player(self, chest)
            self.groups["terrain"].empty()
            . . .
