# Hordes of Enemies

Now we need to make more than one enemy:

## scenes.py

    def simple_enemies(time_step, x_val):
        time = time_step
        while True:
            yield time, x_val
            time += time_step

    class Game(BaseScene):
        def __init__(self, engine, **kwargs):
            . . .
            self.run_time = 0
            self.spawn = simple_enemies(1.5, 200)
            self.next_spawn, self.next_x = next(self.spawn)
        
        def simulate(self, time_delta):
            self.run_time += time_delta
            while self.next_spawn <= self.run_time:
                sprites.Enemy(self, self.next_x)
                self.next_spawn, self.next_x = next(self.spawn)
            . . .

And here's where it gets cool: if you write a generator that reads a given file
and outputs its values as pairs of ints, you can hand design your enemy waves.
