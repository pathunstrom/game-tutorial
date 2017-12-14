from ppb import GameEngine, BaseScene


class Game(BaseScene):
    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)


def main():
    with GameEngine(Game, resolution=(800, 800)) as engine:
        engine.run()

if __name__ == "__main__":
    main()
