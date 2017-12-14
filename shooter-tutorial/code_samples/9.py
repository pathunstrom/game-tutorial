def update(self, *args):
    mouse_x, mouse_y = mouse.get_pos()
    diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
    diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
    self.rect.centerx += diff_x
    self.rect.centery += diff_y
    if diff_x or diff_y:
        self.dirty = True