class Player(DirtySprite):
    . . .
    def update(self, time_delta):
        self.rect.center = mouse.get_pos()
        self.dirty = True