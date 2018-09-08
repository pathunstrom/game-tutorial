import ppb
from ppb import BaseSprite
from ppb.events import Update


class Player(BaseSprite):
    def on_update(self, update: Update, signal):
        self.position += (update.mouse.position - self.position).scale(3) * update.time_delta


def main():
    game_kwargs = {"set_up": scene_setup}

    ppb.run(resolution=(800, 800),
            scene_kwargs=game_kwargs)


def scene_setup(scene):
    scene.add(Player())


if __name__ == "__main__":
    main()
