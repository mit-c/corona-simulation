import pygame
import numpy as np
import sim
import matplotlib.pyplot as plt


pygame.init()

# Set up the drawing window
width = 1200
height = 500
time_step = 0.5
infection_radius = 5
infection_prob = 1
k=5 # nearest neighbours to check
time_to_recover = 2000
screen = pygame.display.set_mode([width, height])
sim = sim.Simulation(width, height, [])
sim.add_people_random(2000, infected=False, recovered=False, velocity=[0, 0])
sim.add_people_random(10, infected=True, recovered=False, velocity=[0, 0])
sim.add_random_vel(1)

counts_susceptible = []
counts_infected = []
counts_recovered = []
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sim.display()
    sim.add_random_vel(0.05)
    sim.update_pos(time_step)
    sim.add_random_vel(0.5)
    sim.update_people(k,infection_radius, infection_prob, time_to_recover)
    counts_susceptible.append(len([person for person in sim.people if not(person.recovered or person.infected)]))
    counts_infected.append(len([person for person in sim.people if person.infected]))
    counts_recovered.append(len([person for person in sim.people if person.recovered]))

# Done! Time to quit.
pygame.quit()
plt.plot(counts_infected, label="Total infected")
plt.plot(counts_susceptible, label= "Total susceptible")
plt.plot(counts_recovered, label = "Total recovered")
plt.xlabel("t")
plt.legend()
plt.show()
# I think the general idea
