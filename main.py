import pygame
import numpy as np
import sim

pygame.init()

# Set up the drawing window
width = 500
height = 500
screen = pygame.display.set_mode([width, height])
sim = sim.Simulation(width, height, [])
sim.add_people_random(100, False, False, [0,0])


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sim.display()


# Done! Time to quit.
pygame.quit()

# TODO: I have to decide whether I want to use taxicab distance or Euclidean.
# I think the general idea