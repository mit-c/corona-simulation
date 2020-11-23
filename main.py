import pygame
import numpy as np
import sim
import matplotlib.pyplot as plt
import pandas as pd

pygame.init()

# Set up the drawing window. I want to have a particle width and height and a game width and height.
# This will enable quarantining.
width = 500
height = 500
time_step = 0.5
infection_radius = 15
# The below probability is checked for every time_step an infected person in within the infection radius of a sus person.
# Therefore it is more of an infection rate.
infection_prob = 0.1
k = 5  # nearest neighbours to check
time_to_recover = 2000
incubation_period = 200
num_susceptible = 100
num_infected = 2
screen = pygame.display.set_mode([width, height])
sim = sim.Simulation(width, height, [])
sim.add_people_random(num_susceptible, infected=False, recovered=False, asymptomatic=False, velocity=[0, 0])
sim.add_people_random(num_infected, infected=True, recovered=False, asymptomatic=False, velocity=[0, 0])
sim.add_random_vel(1)

counts_susceptible = []
counts_infected = []
counts_recovered = []
running = True
time_counter = 0
while running:
    time_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sim.display()
    sim.update_pos(time_step)
    sim.add_random_vel(0.5)
    sim.update_people(k, infection_radius, infection_prob, incubation_period,time_to_recover)
    L = len(sim.people)
    #  The above is because I might want to introduce deaths of infected so need to be calculated every loop.
    current_sus_prop = len([person for person in sim.people if not (person.recovered or person.infected)]) / L
    current_inf_prop = len([person for person in sim.people if person.infected]) / L
    current_rec_prop = len([person for person in sim.people if person.recovered]) / L
    counts_susceptible.append(current_sus_prop)
    counts_infected.append(current_inf_prop)
    counts_recovered.append(current_rec_prop)
    if current_inf_prop == 0:
        print("The infection is no longer in the population")
        break

# Done! Time to quit.
pygame.quit()

plot_dict = {"infected": counts_infected, "susceptible": counts_susceptible, "recovered": counts_recovered}
print(plot_dict)
column_names = ["susceptible count", "infected count", "recovered count"]
fig, ax = plt.subplots()
ax.set_xlim([0, time_counter])
ax.set_ylim([0, 1])
df = pd.DataFrame.from_dict(data=plot_dict)
ax.stackplot(df.index, df.values.T)

plt.show()
# Implement isolation - send some proportion e.g. 90% of infected people to same spot.
# Might need to add bool isolation to person. If a person is isolated those points are ignore until isolation is over.
# Might need to store something like isolation_data which holds last known position and speed for those particle to be reintroduced.
# Need to figure out how to move isolated people - I could send them out the game screen but I want this sim to be visual.
# Therefore I should probably add widht and height property to my sim but set game width and height to be different.
