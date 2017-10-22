class Enemy(DirtySprite):

    def __init__(self, scene, x_position):
        super().__init__(scene.groups["enemy"])
        p_image = image.load(path.join(path.dirname(__file__), "enemy.png"))
        self.image = p_image
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = x_position
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += 3
        self.dirty = True