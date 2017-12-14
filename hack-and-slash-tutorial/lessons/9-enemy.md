Now, let's get something we can hit!

Imports:
    import random

Our new class:

    class Enemy(DirtySprite, TargetABC):

        def __init__(self, scene, position: Vector, player: Player):
            super().__init__(scene.groups["interact"], scene.groups["enemies"])
            self.image = image.load(path.join(path.dirname(__file__),
                                              "enemy.png"))
            self.rect = self.image.get_rect()
            self.rect.center = tuple(position)
            self._position = position
            self.direction = Vector(0, 1).rotate(random.randint(0, 359))
            self.dirty = 1
            self.scene = scene
            self.speed = 30
            self.reach = 20
            self.sense_limit = 200
            self.player = player

        @property
        def position(self):
            return self._position

        def interact(self, player: 'Player'):
            self.kill()

        def update(self, time_delta):
            direction_to_player = self.player.position - self.position
            distance_to_player = direction_to_player.length
            if distance_to_player < self.reach:
                pass
            elif distance_to_player < self.sense_limit:
                self._position += direction_to_player.scale(self.speed * time_delta)
            else:
                self.direction = self.direction.rotate(random.randint(-2, 2))
                self._position += self.direction.scale(self.speed * time_delta * .5)
            self.rect.center = tuple(position)
            self.dirty = 1

We're leaving our first if statement open for right now because we need
to add code to our player before we can actually hit them.

And let's spawn this guy somewhere.

    class Game(BaseScene):
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):

            player = Player(self, chest)
            Enemy(self, Vector(600, 600), player)
            . . .

