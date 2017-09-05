# Movement

So we have a player, but it doesn't move, and that's not a lot of fun.

Let's do something really simple and just use the mouse to move our
character.

First, we need a new import because we need access to the mouse
position.

    from pygame import mouse

Then we're going to add an update function to our Player.

    class Player(DirtySprite):
        . . .
        def update(self, time_delta):
            self.rect.center = mouse.get_pos()
            self.dirty = True

This code simply puts the center of our sprite at the mouse position,
almost like a cursor.

You'll notice that the update function takes a time_delta. Time delta,
or delta time just means the amount of time from the last time we
called this function, to this time.

**PPB** uses fixed step simulation, which means every call to update
will have the same amount of time passed to it, in this case about 16
milliseconds. You can change your simulation steps by passing
`delta_time` to your GameEngine with a float in seconds.

Now we're going to want to limit how fast you can move the player, since
we want to be able to balance the game play eventually.

    def update(self, *args):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y
        if diff_x or diff_y:
            self.dirty = True

So we're limiting our speed to five pixels per update, go ahead and
change those and see if you like your movement different ways.

If you'd like to try a different method of movement, pygame has a key
module with a get_pressed module that returns an array. It also has
a host of key constants that look like:

    K_a
    K_w
    K_s
    K_d
    K_UP
    K_DOWN
    K_LEFT
    K_RIGHT

You can use these to figure out which directions to move your ship and
use the same basic algorithm as above.

What is Sprite.dirty?

Under the hood, we're using dirty rect rendering, which means we only
update the parts of the screen that has been changed. Setting a sprite
to dirty tells the engine that we've updated it.
