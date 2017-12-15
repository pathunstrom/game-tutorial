Now, let's add an interface so that our `Player` can interact with
`Targets`. As usual, we add our imports first:

    from abc import ABC
    from abc import abstractmethod

Now, near the top of your file, let's define TargetABC:

    class TargetABC(ABC):

        @property
        @abstractmethod
        def position(self) -> Vector:
            pass

        @abstractmethod
        def interact(self, player: 'Player'):
            logging.getLogger(type(self).__name__).debug(f"{type(self).__name__} reached!")

So, now we have a defined interface for our player's targets.

So in our `Player.__init__` let's add a single type hint:

    class Player(DirtySprite):

        def __init__(self, scene, target: TargetABC=None):
            . . .
            self.target: TargetABC = target
            . . .

Now let's make our `EmptyTarget` match the ABC:

    class EmptyTarget:

        def interact(self, player):
            logging.getLogger(type(self).__name__).debug(f"{type(self).__name__} reached!")

An empty target doesn't do anything, but let's add a logging statement
for debugging.

And we're going to tell `TargetABC` that `EmptyTarget` matches the ABC.

    TargetABC.register(EmptyTarget)

This feels pretty pointless, but now we can go back to our chest!

First, let's rewrite the class a bit to make it a TargetABC.

    class ClosedChest(DirtySprite, TargetABC):
        def __init__(self, scene, position: Vector) -> None:
            . . .
            self._position = position
            . . .

        @property
        def position(self):
            return self._position

        def interact(self, player):
            super().interact(player)

And one last step to make sure everything is working, let's set the
`GameEngine`'s `log_level` to `logging.DEBUG`.

    def main():
        with GameEngine(Game, resolution=(800, 800), log_level=logging.DEBUG) as engine:
            engine.run()

