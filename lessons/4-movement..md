# Movement

Let's move the ship around.

## sprites.py

    from pygame import image, mouse

We need the mouse interface for this.

    def update(self, *args):
        self.rect.center = mouse.get_pos()

This isn't a great feel for movement, so we're going to separate the movement
from the mouse sensitivity.

    def update(self, *args):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.center = diff_x, diff_y

Now you can move your ship.