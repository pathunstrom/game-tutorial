class Bullet(DirtySprite):

    def __init__(self, scene, position):
        super().__init__(scene.groups["bullets"])
        b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
        self.image = b_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = position  # Modify this
        self.scene = scene