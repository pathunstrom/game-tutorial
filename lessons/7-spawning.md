# Hordes of Enemies

Now we need to make more than one enemy. One option is to spawn them all
at various y offsets so that they all can spawn at the beginning of the
game, but that's more expensive in memory, especially the way we've
written our sprites.

So let's make a spawner!

    class Spawner(object):

        def __init__(self, scene, generator, enemy_class):
            self.scene = scene
            self.enemy_class = enemy_class
            self.generator = generator
            self.running = True
            self.time = 0
            self.next_time = None
            self.next_position = None
            self.prime()

        def spawn(self, time_delta):
            self.time += time_delta
            while self.running and self.time >= self.next_time:
                self.enemy_class(self.scene, self.next_position)
                self.prime()

        def prime(self):
            try:
                self.next_time, self.next_position = next(self.generator)
            except StopIteration:
                self.running = False

To use this, we're going to need to write a generator that outputs a
2-tuple of a timestamp in seconds since the game started, and an
x-position to spawn the enemy at.

    from itertools import count

    def simple_infinite_spawn(time_step, x_val):
        for value in count(1):
            time = time_step * value
            yield time, x_val

Now let's hook it into our Game.

    class Game(BaseScene):
        def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
            . . .
            # Enemy(self, 200)  # Delete this
            self.spawner = Spawner(self, simple_infinite_spawn(1.5, 200), Enemy)

        def simulate(self, time_delta):
            super().simulate(time_delta)
            self.spawner.spawn(time_delta)
            . . .

Now let's make a second generator that can handle a CSV file.

Make a file called `spawn.csv` and let's populate it:

    1.5,200
    1.6,300
    1.7,100

Now we'll make a new generator:

    def file_spawner(file_name):
        with open(path.join(path.dirname(__file__), file_name), "r") as spawn_file:
            spawn_reader = csv.reader(csvfile)
            for row in spawn_reader:
                yield float(row[0]), int(row[1])

Then replace our simple spawner with this.

    self.spawner = Spawner(self, file_spawner('spawn.csv'), Enemy)
