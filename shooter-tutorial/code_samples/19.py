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
            self.next_spawn, self.next_position = next(self.generator)
        except StopIteration:
            self.running = False