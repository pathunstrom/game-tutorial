# Guns too fast

So we need to put a limiter on our Player.

    def __init__(self, scene):
        super().__init__(scene)
        self.cooldown = 0

    def update(self, time_delta, *args):
        . . .
        
        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0] and self.cooldown <= 0:
            Bullet(self.scene, self.rect.midtop)
            self.cooldown = 0.35
        self.cooldown -= time_delta

Look at that, nice controlled rate of fire.
