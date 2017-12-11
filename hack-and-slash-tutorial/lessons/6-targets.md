So we can click to move, but we're going to need to be able to interact
with things. So let's build a chest that we can open by moving to it.

First, let's import logging so we can see if our prototype is working.

    import logging

Then in our call to the game engine in the main block, we'll add the
debug loglevel.

    def main():
        with GameEngine(Game, resolution=(800, 800), log_level=logging.DEBUG) as engine:
            engine.run()

And now, we can build our chest:

    class ClosedChest(DirtySprite):
        def __init__(self, scene, position: Vector):
            super().__init__(scene.groups["interact"])
            self.image = image.load(path.join(path.dirname(__file__),
                                              "chest_closed.png"))
            self.rect = self.image.get_rect()
            self.rect.center = tuple(position)
            self.position = position
            self.dirty = 1
            self.scene = scene

The only interesting thing here is that we're passing the chest its
location, so we can spawn them anywhere in game we want, otherwise this
is exactly like our player.

Now, instead of an update (Because chests don't move) we're going to
give the sprite a method for interacting with it.

        def interact(self, actor):
            logging.debug("Chest opened!")

This is just a stub for us to test, so let's wire it up and see what
happens.

    class Game(BaseScene):
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
            . . .
            chest = ClosedChest(self, Vector(750, 750))
            player = Player(self, chest)

We fail, because a `ClosedChest` doesn't look like a `Vector`, so we
need  to change how our `Player` interacts with its targets.

    class Player(DirtySprite):
        def update(self, time_delta):
            if self.target is not None:
                move_path = self.target.position - self.position
                if move_path.length < self.reach:

So now, instead of our `target` being used as the thing we're moving to,
we'll use the position of the `target`.

Let's try running this version.

So if you just let it move to the chest, it works just fine, but never
interacts. Also, if any of you clicked anywhere you'll get an error.

So, two problems, let's solve the control problem first:

A target now needs a `position`, but the controller only sets a
`Vector`.

First let's make a stub class:

    class EmptyTarget:

        def __init__(self, position: Vector):
            self.position = position

An `EmptyTarget` fulfills the need of the `Player` class, so this will
be useful for clicks on nothing.

Now in the controller, we're going to give in a list of `targets` for
things you can click on. We'll also add a `button_pressed` state to add
a delay to command entry.


    class Controller:

        def __init__(self, actor, targets):
            self.actor = actor
            self.targets = targets
            self.button_pressed = False

And in `respond`, we're going to add a lot:

    def respond(self):
        mouse_buttons = mouse.get_pressed()
        mouse_position = mouse.get_pos()
        if mouse_buttons[0] and not self.button_pressed:
            self.button_pressed = True
            target = EmptyTarget(Vector(*mouse_position))
            for sprite in self.targets.sprites():
                if sprite.rect.collidepoint(mouse_position):
                    target = sprite
                    break
            self.actor.target = target
        if not mouse_buttons[0] and self.button_pressed:
            self.button_pressed = False

The expanded if statements allow us to only set one target per click.

In the click, we instantiate an EmptyTarget, then check to see if our
click hit any object in the target group. If it did, we will use that
as our target instead.

Then we set the target as usual.

Make sure to pass our interact group to the Controller:

    class Game(BaseScene):
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
            . . .
            self.controller = Controller(player, self.groups["interact"])

Run this and we can move around (Without interaction) anywhere we want.
