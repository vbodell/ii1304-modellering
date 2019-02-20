from enum import Enum
import random

class Person():
    State = Enum('State', 'HEALTHY INFECTED DEAD')

    kMaxNeighbors = 8

    # def __init__(population, position, firstDayOfInfection=-1, state=HEALTHY, isImmune=False):
    def __init__(self, firstDayOfInfection=-1, state=State.HEALTHY, isImmune=False):
        # self.population = population
        # self.position = position
        self.neighbors = None
        self.firstDayOfInfection = firstDayOfInfection
        self.state = state
        self.isImmune = isImmune
        self.infectionDays = None

        # Find neighbors
        # self.neighbors = []
        # (i, j) = self.position
        # for x in range(-1,1):
        #     for y in range(-1,1):
        #         nX = i + x
        #         nY = j + y
        #         if self.population.validPosition(nX, nY) and (i != x and j != y):
        #             self.neighbors.append((nX, nY))

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    def infectNeighbor(self, prob, currentDay, infectionDays):
        if self.wasInfectedToday or self.isDead or self.isHealthy or not self.neighbors:
            return

        # neighborToInfect = random.choice(self.neighbors)
        # if random.choices([True, False], weights=[prob, 1-prob])[0]:
            # neighborToInfect.infect(currentDay, infectionDays)

    def die(self, prob):
        if self.isDead or self.wasInfectedToday: # TODO: Infected today?
            return

        if random.choices([True, False], weights=[prob, 1-prob])[0]:
            self.state = Person.State.DEAD

    @property
    def wasInfectedToday(self, day):
        return day == self.firstDayOfInfection

    @property
    def isHealthy(self):
        return self.state == Person.State.HEALTHY

    @property
    def isInfected(self):
        return self.state == Person.State.INFECTED

    @property
    def isDead(self):
        return self.state == Person.State.DEAD

    def infect(self, infectionDay, infectionDays):
        if self.isImmune or self.isInfected or self.isDead:
            return

        self.firstDayOfInfection = infectionDay
        self.state = Person.State.INFECTED

    def getHealthy(self, currentDay):
        # Returns True iff self was infected and got healthy
        if not self.isInfected:
            return False

        if currentDay == self.firstDayOfInfection + self.infectionDays:
            self.state = Person.State.HEALTHY
            self.isImmune = True

        return self.isHealthy

    def __str__(self):
        s = ""
        if self.state is Person.State.HEALTHY:
            s += "H"
        elif self.state == Person.State.INFECTED:
            s += "I"
        else:
            s += "D"

        s += "x" if self.isImmune else "."
        return s

if __name__ == "__main__":
    p = Person()
    print(p)

# class PersonTester():
#     def __init__(self, person):
#         self.person = person
#
#     def test1(self):
#         pass
