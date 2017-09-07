# Clean Up

So we have a few minor code issues that we can improve and make other
development easier.

The primary issues:

1. Repeated boilerplate
2. magic strings
3. using more memory on images than needed
4. updating useless sprites

The first three can be solved with one primary change. The last is a
minor behavior we can build quite easily.

First, let's talk about the things we do in all of our sprites:

1. We call super to hook the sprite into the scene's groups.
2. We set a reference to the scene.
3. We load and attach an image.
4. We move the sprite to its intended position.

One thing that's happening that you don't see is we're getting a copy
of the image every time we instantiate things.

So let's pull these things out into a BaseObject

    from pygame import Rect

    ROOT_DIR = path.dirname(__file__)

    class BaseGameObject(DirtySprite):
        group = None
        image_path = None
        image = None

        def __init__(self, scene, position=(0, 0)):
            cls = self.__class__
            cls.group = cls.__name__
            super().__init__(scene.groups[cls.group], scene.groups["render"])
            self.scene = scene
            cls.image = image.load(path.join(ROOT_DIR, cls.image_path))
            self.rect = cls.image.get_rect()
            self.rect.center = position
            self.last_position = position

        def update(self, time_delta):
            self.simulate(time_delta)
            if self.rect.center != self.last_position:
                self.dirty = True
                self.last_position = self.rect.center

        def simulate(self, time_delta):
            pass

We now have a more robust basic game object that will make defining new
object much faster. Importantly, we now use one image per type of
object using what is known as the Flywheel Pattern. By sharing the
memory space, we reduce the memory needs of our game. Also, instead of
magic strings for identity, we use the name of the sprite type.

So with this base class built, let's rewrite our game objects.

    class Player(BaseGameObject):
        image_path = "player.png"

        def __init__(self, scene):
            super().__init__(scene)
            self.bullet_limiter = 0.25
            self.bullet_delay = 0

        def simulate(self, time_delta):
            mouse_x, mouse_y = mouse.get_pos()
            diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
            diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
            self.rect.centerx += diff_x
            self.rect.centery += diff_y

            pressed = mouse.get_pressed()
            if pressed[0] and (self.bullet_delay >= self.bullet_limiter):
                Bullet(self.scene, self.rect.midtop)
                self.bullet_delay = 0
            self.bullet_delay += time_delta


    class Bullet(BaseGameObject):
        image_path = "bullet.png"

        def simulate(self, time_delta):
            self.rect.centery += -10


    class Enemy(BaseGameObject):
        image_path = "enemy.png"

        def __init__(self, scene, x_position):
            super().__init__(scene, (x_position, 0))

        def simulate(self, time_delta):
            self.rect.centery += 3

The key part of this work is that future game objects look like this
instead of all looking like BaseGameObject.

The last change to get all of this working:

    class Game(BaseScene):
        . . .
        def simulate(time_delta):
            self.spawner.spawn(time_delta)

            player = self.groups[Player.group]
            bullets = self.groups[Bullet.group]
            enemies = self.groups[Enemy.group]
            groupcollide(player, enemies, True, True)
            . . .
