# Setting up your first scene

## scenes.py

    from ppb import BaseScene
    
    class Game(BaseScene):
    
        def __init__(self, engine, **kwargs):
            super().__init__(engine=engine, 
                             background_color=(0, 0, 0),
                             **kwargs)
        
        def change(self):
            return not self.running, {}

BaseScene provides some basic tools that you need for the rest of the project.
Most importantly, it's already set up with `groups` which will store all the
sprites we build later.

We had to define `change` because of a standing bug in the engine.

## main.py

    from ppb import GameEngine
    
    from mygame.scenes import Game
    
    with GameEngine(Game, resolution=(400, 600)) as engine:
        engine.run()

That third line of code actually runs 19 lines of boilerplate, setting up your
hardware and prepping basic state.

`run` is where the real magic happens. A complex game loop ready to go.

## shell

    python main.py

Run your code! Right now, it's just a blank screen. Hit the close button and
see behavior the engine gives you.