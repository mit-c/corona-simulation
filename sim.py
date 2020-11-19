import pygame
import numpy as np
import random


class Simulation:
    def __init__(self, width=500, height=500, people=[]):
        self.screen = pygame.display.set_mode([width, height])
        self.people = people

    def add_person(self, pos, infected, recovered, velocity=[0,0]):
        person = Person(pos, infected, recovered, velocity)
        self.people.append(person)
        return person

    def add_people_random(self, n, infected, recovered, velocity=[0,0]):
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


class Person:
    def __init__(self, pos, infected=False, recovered=False, speed=0):
        self.pos = pos
        self.infected = infected
        self.speed = speed
        self.recovered = recovered
        # Can add more features but got the basics.
