from pygame.transform import smoothscale

image = image.load("player.png")
scaled_image = smoothscale(image,
                           (image.get_width() * 0.5,
                            image.get_height() * 0.5))