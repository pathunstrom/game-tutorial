import ppb
from ppb import BaseSprite


class Player(BaseSprite):
    pass


def main():
    game_kwargs = {"set_up": scene_setup}

    ppb.run(resolution=(800, 800),
            scene_kwargs=game_kwargs)


def scene_setup(scene):
    scene.add(Player())


if __name__ == "__main__":
    main()
