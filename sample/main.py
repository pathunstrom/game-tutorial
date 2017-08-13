from ppb import GameEngine

from scenes import Game

with GameEngine(Game, resolution=(400, 600)) as engine:
    engine.run()
