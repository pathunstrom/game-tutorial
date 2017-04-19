from math import floor
from os import path

from ppb import BaseScene
import pygame as pg
from pygame.sprite import DirtySprite, GroupSingle

from shooter import IMG_PATH


def infinite_enemies(play_area):
    x = play_area.centerx
    time = 0
    while True:
        yield time, x
        time += 1.5


class Game(BaseScene):

    def __init__(self, engine, level=None, **kwargs):
        super().__init__(engine=engine, **kwargs)
        self.play_area = engine.display.get_rect()
        # initialize player
        self.groups[Player.group] = GroupSingle()
        Player(self)
        # initialize enemy generator
        self.enemy_generator = infinite_enemies(self.play_area)
        self.next_enemy_spawn = None
        self.next_enemy_position = None
        self.next_enemy()
        self.run_time = 0

    def simulate(self, time_delta: float):
        self.run_time += time_delta
        while self.run_time >= self.next_enemy_spawn:
            Enemy(self, self.next_enemy_position)
            self.next_enemy()
        super().simulate(time_delta)
        players = self.groups[Player.group]
        enemies = self.groups[Enemy.group]
        bullets = self.groups[Bullet.group]
        pg.sprite.groupcollide(players, enemies, True, True)
        pg.sprite.groupcollide(bullets, enemies, True, True)

    def next_enemy(self):
        next_spawn, next_pos = next(self.enemy_generator)
        self.next_enemy_spawn = next_spawn
        self.next_enemy_position = next_pos

    def change(self):
        return not self.running, {}

    def __mouse_up__(self, event):
        player = self.groups[Player.group].sprite
        if player.ready:
            Bullet(self, player.rect.midtop)
            player.cooldown()


class GameSprite(DirtySprite):
    group = "no_group"
    speed = 0
    image_path = "none.png"
    image = None

    def __init__(self, scene):
        cls = self.__class__
        super().__init__(scene.groups[cls.group])
        if cls.image is None:
            sprite_image = pg.image.load(path.join(IMG_PATH, cls.image_path))
            scale_size = [floor(x * .5) for x in sprite_image.get_size()]
            cls.image = pg.transform.smoothscale(sprite_image, scale_size)
        self.rect = self.image.get_rect()
        self.scene = scene


class Player(GameSprite):
    group = "player_group"
    speed = 4
    image_path = "player.png"

    def __init__(self, scene):
        super().__init__(scene)
        self.rect.midbottom = scene.play_area.midbottom
        self.cooldown_timer = 0

    def update(self, time_delta: float, *args):
        self.cooldown_timer -= time_delta
        x, _ = pg.mouse.get_pos()
        difference = x - self.rect.centerx
        multiplier = -1 if difference < 0 else 1
        self.rect.centerx += min(abs(difference), Player.speed) * multiplier

        if self.rect.right > self.scene.play_area.right:
            self.rect.right = self.scene.play_area.right
        if self.rect.left < self.scene.play_area.left:
            self.rect.left = self.scene.play_area.left
        self.dirty = True

    @property
    def ready(self):
        return self.cooldown_timer <= 0

    def cooldown(self):
        self.cooldown_timer = .5


class Enemy(GameSprite):
    group = "enemy_group"
    speed = 3
    image_path = "enemy.png"

    def __init__(self, scene, x_pos):
        super().__init__(scene)
        self.rect.bottom = scene.play_area.top
        self.rect.centerx = x_pos

    def update(self, *args):
        self.rect.centery += Enemy.speed
        self.dirty = True


class Bullet(GameSprite):
    group = "bullet_group"
    speed = 6
    image_path = "bullet.png"

    def __init__(self, scene, tail_position):
        super().__init__(scene)
        self.rect.midbottom = tail_position

    def update(self, *args):
        self.rect.centery += -Bullet.speed
        self.dirty = True
