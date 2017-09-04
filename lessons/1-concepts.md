# Concepts

Basic game dev concepts

## Main Loop  _move to setup_

_TBD_

## Engine versus Framework _introductory_

Fraught territory but basics: An engine is given your code and calls
into it, a framework provides a library that your game calls into.

## Scenes _move to designing scene_

Scene is a common term in game development and is the basic building
block of a game. Any given scene represents a self contained unit of
game play, such as a single level in Arkanoid.

## Sprite _move to designing sprite_

Sprite, when working with Pygame, is an overloaded term that can mean
both a pixel animation or a given game object. Mostly it will refer to
the game objects.

## Time_delta _Expand? move to main loop discussion_

The time difference between the last of a given action and the next.

## Cartesian points  _rewrite_

Graphics tend to calculate the origin in the top left corner, instead
of the bottom left corner. In other words: positive Y values go down,
and negative Y values go up.