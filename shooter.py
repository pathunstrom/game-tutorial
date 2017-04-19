from ppb import GameEngine

from shooter.scenes import Game

with GameEngine(Game, resolution=(400, 600)) as engine:
    engine.run()
