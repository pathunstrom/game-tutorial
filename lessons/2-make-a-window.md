# My First GUI

The kinds of games you make with **PPB** are going to have graphical
user interfaces. GUIs require a different way of thinking from CLI
programs that are much more common in Python.

A key thing you need to know is it can't stop running to wait for user
input. To that regard, you're going to need a main loop.

## Main Loops

A gui program runs on a basic loop that renders, responds to input,
then updates the model. Very simply, a basic game loop looks like this:

    running = True

    while running:
        handle_input()
        update_state()
        draw_screen()

Thankfully, we don't need to worry about developing and maintaining our
main loop, since PPB comes with one. In a file called `main.py` write
this:

    from ppb import GameEngine, BaseScene

    with GameEngine(BaseScene) as engine:
        engine.run()

Run this and you'll find you have a window. Under the hood this provides
access to the hardware