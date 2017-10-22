from pygame.sprite import groupcollide

class Game(BaseScene):

    def simulate(self, time_delta):
        super().simulate(time_delta)
        player = self.groups[sprites.Player.group]
        bullets = self.groups[sprites.Bullet.group]
        enemies = self.groups[sprites.Enemy.group]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, bullets, True, True)