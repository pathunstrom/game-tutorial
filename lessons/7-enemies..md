# Something to shoot

Now we get something to shoot at.

## sprites.py

    class Enemy(BaseSprite):
        group = "enemy_group"
        img_path = "enemy.png"
        
        def __init__(self, scene, x_position):
            super().__init__(scene)
            self.rect.midbottom = scene.play_area.midtop
            self.rect.centerx = x_position
        
        def update(self, *args):
            super().update(*args)
            self.rect.centery += 4
            if self.top > self.scene.play_area.bottom:
                self.kill()

So we only need to know where in the lane to start our enemy, after that, it
just flies down.

## scenes.py

Let's test by putting it somewhere.

    class Game(BaseScene):
        def __init__(self, engine, **kwargs):
            . . .
            sprites.Player(self)
            _ = self.groups[sprites.Bullet.group]
            sprites.Enemy(self, 200)

We work around another bug by reading the Bullet group, and add the single
enemy.

Of course, nothing is interacting, we have a bunch of things flying past each
other.

    from pygame.sprite import groupcollide

    class Game(BaseScene):
        def simulate(self, time_delta):
            super().simulate(time_delta)
            player = self.groups[sprites.Player.group]
            bullets = self.groups[sprites.Bullet.group]
            enemies = self.groups[sprites.Enemy.group]
            groupcollide(player, enemies, True, True)
            groupcollide(enemies, bullets, True, True)

