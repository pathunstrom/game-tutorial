class Bullet(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["bullets"])
        b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
        self.image = b_image
        self.rect = self.image.get_rect()
        self.rect.bottom = 600
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += -10
        self.dirty = True