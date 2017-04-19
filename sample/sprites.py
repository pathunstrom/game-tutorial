from os import path

from pygame import image, mouse
from pygame.sprite import DirtySprite

IMG_PATH = path.join(path.dirname(__file__), "img")


class BaseSprite(DirtySprite):
    group = None
    image_path = None
    image = None

    def __init__(self, scene):
        cls = self.__class__
        super().__init__(scene.groups[cls.group])
        if cls.image is None:
            cls.image = image.load(path.join(IMG_PATH, cls.image_path))
        self.rect = self.image.get_rect()
        self.scene = scene

    def update(self, *args):
        self.dirty = True


class Player(BaseSprite):
    group = "player_group"
    image_path = "player.png"

    def __init__(self, scene):
        super().__init__(scene)
        self.cooldown = 0

    def update(self, time_delta, *args):
        super().update(*args)
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y

        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0] and self.cooldown <= 0:
            Bullet(self.scene, self.rect.midtop)
            self.cooldown = 0.35
        self.cooldown -= time_delta


class Bullet(BaseSprite):
    group = "bullet_group"
    image_path = "bullet.png"

    def __init__(self, scene, tail_position):
        super().__init__(scene)
        self.rect.midbottom = tail_position

    def update(self, *args):
        super().update(*args)
        self.rect.centery += -6
        if self.rect.bottom < self.scene.play_area.top:
            self.kill()


class Enemy(BaseSprite):
    group = "enemy_group"
    image_path = "enemy.png"

    def __init__(self, scene, x_position):
        super().__init__(scene)
        self.rect.midbottom = scene.play_area.midtop
        self.rect.centerx = x_position

    def update(self, *args):
        super().update(*args)
        self.rect.centery += 4
