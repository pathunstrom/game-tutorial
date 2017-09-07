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