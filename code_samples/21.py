class Game(BaseScene):
    def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
        . . .
        # Enemy(self, 200)  # Delete this
        self.spawner = Spawner(self, simple_infinite_spawn(1.5, 200), Enemy)

    def simulate(self, time_delta):
        super().simulate(time_delta)
        self.spawner.spawn(time_delta)
        . . .