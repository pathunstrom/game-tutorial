from os import path

from ppb import BaseScene, GameEngine
from pygame import image
from pygame import mouse
from pygame.sprite import DirtySprite
from pygame.sprite import groupcollide


class Bullet(DirtySprite):

    def __init__(self, scene, position):
        super().__init__(scene.groups["bullets"])
        b_image = image.load(path.join(path.dirname(__file__), "bullet.png"))
        self.image = b_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += -10
        self.dirty = True


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


class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        Player(self)
        Bullet(self, (0, 0)).kill()
        Enemy(self, 200)

    def simulate(self, time_delta):
        super().simulate(time_delta)
        player = self.groups["player"]
        bullets = self.groups["bullets"]
        enemies = self.groups["enemy"]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, bullets, True, True)


class Player(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.scene = scene
        self.bullet_limiter = 0.25
        self.bullet_delay = 0.0

    def update(self, time_delta):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y
        if diff_x or diff_y:
            self.dirty = True

        pressed = mouse.get_pressed()
        if pressed[0] and self.bullet_delay > self.bullet_limiter:
            Bullet(self.scene, self.rect.midtop)
            self.bullet_delay = 0
        self.bullet_delay += time_delta


def main():
    with GameEngine(Game, resolution=(400, 600)) as engine:
        engine.run()

if __name__ == "__main__":
    main()
