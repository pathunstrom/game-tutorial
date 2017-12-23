# Controls

We have a moving sprite, now let's hook up some controls.

For we add a couple of imports:

    from pygame import mouse

We'll use mouse to access the buttons and position of the mouse.

First, we're going to design our controller. The point of this object
is to move the mouse controls outside the Sprites so we can change the
interfaces later if we want.

    class Controller:

        def __init__(self, actor):
            self.actor = actor

        def respond(self):
            mouse_buttons = mouse.get_pressed()
            if mouse_buttons[0]:
                mouse_position = mouse.get_pos()
                self.actor.target = Vector(*mouse_position)

Simple right? `mouse_buttons` is a tuple. Each button on a mouse has an
identity, and we tend to think of them as numbers. The left click is
button 1, which lives at index 0 in the tuple.

The position is a 2-tuple that is the data we need for our Vector
target.

Now let's wire this all together:

First, let's instantiate this in the `Game.__init__`.

    class Game(BaseScene):
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
            . . .
            player = Player(self, Vector(750, 750))
            self.controller = Controller(player)

We need to store the player for a moment to pass it as the actor to the
`Controller`. We'll store the controller on the instance so we can call
that `respond` method.

So we'll modify how the `Scene.simulate` handles things:

    def simulate(self, time_delta: float):
        self.controller.respond()
        super().simulate(time_delta)

Because simulate is defined on the `BaseScene` we obviously need to call
super, but we should do interface responses first.

And now we can run this and have our character move wherever we want.