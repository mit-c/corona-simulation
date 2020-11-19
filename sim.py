import pygame
import numpy as np
import random
from sklearn.neighbors import KDTree


class Simulation:
    def __init__(self, width=500, height=500, people=[]):
        self.screen = pygame.display.set_mode([width, height])
        self.people = people

    def add_person(self, pos, infected, recovered, velocity=[0, 0]):
        person = Person(pos, infected, recovered, velocity)
        self.people.append(person)
        return person

    def add_people_random(self, n, infected, recovered, velocity=[0, 0]):
        # Add a n people (either S I or R). (infected=False and recovered = False) => S
        w = self.screen.get_width()
        h = self.screen.get_height()
        # Generating random position in our screen range.
        for i in range(n):
            x_pos = w * random.random()
            y_pos = h * random.random()
            self.add_person([x_pos, y_pos], infected, recovered, velocity)

    def display(self):

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        white = (255, 255, 255)
        self.screen.fill(white)
        for person in self.people:
            if person.infected:
                colour = red
            elif person.recovered:
                colour = green
            else:
                colour = blue
            pygame.draw.circle(self.screen, colour, person.pos, 5)
        pygame.display.flip()

    def update_pos(self, time_step):
        # velocity will be normalised
        if not self.people:
            print("people list empty")
            return
        for person in self.people:
            w = self.screen.get_width()
            h = self.screen.get_height()

            if person.pos[0] < 0 or person.pos[0] > w:  # if outside board
                v0 = -np.sign(person.pos[0])  # set speed to towards board
            else:
                v0 = person.velocity[0]

            if person.pos[1] < 0 or person.pos[1] > h:
                v1 = -np.sign(person.pos[1])
            else:
                v1 = person.velocity[1]

            v_size = (v0 * v0 + v1 * v1) ** 0.5
            v = [v0 / v_size, v1 / v_size]
            person.velocity = v
            person.pos[0] += v[0] * time_step
            person.pos[1] += v[1] * time_step

    def add_random_vel(self, amount):
        if not self.people:
            print("can't initialise speed for no people")
            return

        for person in self.people:
            v0 = -amount + 2 * amount * random.random() + person.velocity[0]
            v1 = -amount + 2 * amount * random.random() + person.velocity[1]
            vec_size = (v0 * v0 + v1 * v1) ** 0.5
            person.velocity = [v0 / vec_size, v1 / vec_size]

    def update_people(self, k, infection_radius, infection_prob, time_to_recover):
        self.update_people_susceptible(k, infection_radius, infection_prob)
        self.update_people_infected(time_to_recover)
        return

    def update_people_susceptible(self, k, infection_radius, infection_prob):
        # want to use KD-trees (sklearn)
        #
        '''
        TODO:
            The KDTree approach gets inefficient when the amount of infected people gets small.
            This in turn makes the tree small - so we are searching loads of infected people through a small tree.
            Fix:  If number of infected people < susceptible then do the same.
            Otherwise create an infected KDTree and search the susceptible points through it.
        '''
        points = [person.pos for person in self.people if not person.infected and not person.recovered]

        k = min(len(points), k)
        print(k)
        if k == 0:
            return
        arr = np.array(points)
        my_tree = KDTree(arr)
        infected_persons = ([person.pos for person in self.people if person.infected])
        infected_persons_points = np.array(infected_persons)
        if not infected_persons:
            return
        array_pair = my_tree.query(infected_persons_points, k)
        index_mem = []
        for j in range(len(infected_persons)):
            indices = array_pair[1][j]
            distances = array_pair[0][j]

            for i, distance in enumerate(distances):
                ix = indices[i]
                if distance < infection_radius:
                    if random.random() < infection_prob:
                        index_mem.append(ix)

        if not index_mem:
            return

        x = my_tree.data
        for index in index_mem:
            pos = [x[index][0], x[index][1]]
            for person in self.people:
                if person.pos == pos:
                    person.infected = True
                    break

    def update_people_infected(self, time_to_recover):
        for person in self.people:
            if person.infected:
                person.time += 1
                if person.time > time_to_recover:
                    person.infected=False
                    person.recovered=True

class Person:
    def __init__(self, pos, infected=False, recovered=False, velocity=[0, 0]):
        self.pos = pos
        self.infected = infected
        self.velocity = velocity
        self.recovered = recovered
        self.time = 0
        # Can add more features but got the basics.
