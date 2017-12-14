# Setting up your first scene

We just used PPB's base scene, but we're going to need to modify it in
order to make our game. So let's subclass it.

In `main.py` let's define our first scene: `Game`.

    from ppb import GameEngine, BaseScene
    
    class Game(BaseScene):
    
        def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
            super().__init__(engine=engine, 
                             background_color=background_color,
                             **kwargs)

For those who have never done additive color, the background_color is a
tuple of `(red, green, blue)`. If you've ever used hex-colors on the web
you've used this scheme before. The values are between 0 and 255, making
our background a 24 bit color pallet.

Depending on what sprite images you brought with you, you'll want to
pick a background color that contrasts well. (Don't worry, you can
change this later.)

Now, let's hook our new scene into the engine, and pick our display
resolution.
    
    def main():
        with GameEngine(Game, resolution=(800, 800)) as engine:
            engine.run()

    if __name__ == "__main__":
        main()

Why do we pass the game class and not an instance?

PPB is designed to load game resources as lazily as possible. Instead
of loading every resource at the beginning of the game, we'll wait
until a scene is actually needed to load the various resources.

Resolution is an entirely optional parameter as already demonstrated,
but the goal is an old school style shooter that is taller than it is
wide, so we want to flip the resolution for now.

Why "Scene"?

Scene is just a common word for a part of a game. In general games use
language similar to film: We have scenes in which actors act and a
camera that provides a view into the gameplay.
