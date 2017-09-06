# Something to shoot

We can shoot things, we can move, now we need targets. Get your enemy
sprite, or get `enemy.png` from the resources file.

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

Our enemies will spawn just off screen, and fly in straight lines to
the bottom.

Now let's test one, inside Game:

    class Game(BaseScene):

    def __init__(self, engine, background_color=(90, 55, 100), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        Player(self)
        Bullet(self, (0, 0)).kill()
        Enemy(self, 200)

So we have enemies that move, a player that shoots, but nothing else.

Let's make some collisions!

    from pygame.sprite import groupcollide

    class Game(BaseScene):

        def simulate(self, time_delta):
            super().simulate(time_delta)
            player = self.groups[sprites.Player.group]
            bullets = self.groups[sprites.Bullet.group]
            enemies = self.groups[sprites.Enemy.group]
            groupcollide(player, enemies, True, True)
            groupcollide(enemies, bullets, True, True)

`groupcollide` takes two sprite groups and checks every sprite inside
against each other. The two booleans are telling group collide to kill
all sprites in the first or second group that have collided with at
least one object in the other group.

Now all we need is to be able to make more than one enemy and we'll
have a game.
