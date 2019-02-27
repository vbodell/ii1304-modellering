from enum import Enum
from numpy import random

class Person():
    State = Enum('State', 'HEALTHY INFECTED DEAD')
    VERBOSE = False

    @staticmethod
    def setSeed(SEED):
        if Person.VERBOSE:
            print("Seed was set to %d" % SEED)
        random.seed(SEED)

    def __init__(self, x, y):
        self.name = "[%s, %s]" % (x,y) # A unique identifier for each person
        self.neighbors = None
        self.firstDayOfInfection = None
        self.state = Person.State.HEALTHY
        self.isImmune = False
        self.infectionDays = None
        self.hasTriedInfecting = False

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    def infectNeighbors(self, prob, currentDay, daysInterval):
        # Returns the number of neighbors that were infected
        if self.wasInfectedToday(currentDay) or self.isDead or\
         self.isHealthy or self.hasTriedInfecting or not self.neighbors:
            return 0

        infectCount = 0
        if random.choice([True, False], 1, p=[prob, 1-prob])[0]:
            for n in self.neighbors:
                infectCount += n.infect(currentDay, daysInterval)

        self.hasTriedInfecting = True
        return infectCount

    def die(self, prob):
        if self.isDead: # Note that an individual infected today may still die
            return

        died = random.choice([True, False], 1, p=[prob, 1-prob])[0]
        if died:
            self.state = Person.State.DEAD
        return died

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

    def infect(self, infectionDay, daysInterval):
        if self.isImmune or self.isInfected or self.isDead:
            return False

        self.state = Person.State.INFECTED
        self.firstDayOfInfection = infectionDay
        self.infectionDays = self.randomInfectionDays(daysInterval)

        if Person.VERBOSE:
            print("%s was infected on day %d and will be sick for %d days" %\
             (self.name, self.firstDayOfInfection, self.infectionDays))
        return True

    def getHealthy(self, currentDay):
        # Returns True iff self was infected and got healthy
        if not self.isInfected:
            return False

        if currentDay == self.firstDayOfInfection + self.infectionDays:
            self.state = Person.State.HEALTHY
            self.isImmune = True

        return self.isHealthy

    @staticmethod
    def randomInfectionDays(interval):
        return random.randint(interval[0], interval[1])

    def __str__(self):
        s = ""
        if self.state is Person.State.HEALTHY:
            s += "h"
        elif self.state == Person.State.INFECTED:
            s += "/"
        else:
            s += "-"

        s += "X" if self.isImmune else "."
        return s

if __name__ == "__main__":
    assert Person.randomInfectionDays((2,2)) == 2
    assert Person.randomInfectionDays((2,4)) > 1
    assert Person.randomInfectionDays((2,4)) < 5

    p = Person(0,1)
    Person.VERBOSE = True
    assert p.isHealthy
    assert not p.isImmune
    assert not p.isDead
    assert not p.isInfected
    assert str(p) == "h."
    assert not p.getHealthy(0)

    print("Infect p:")
    p.infect(1, (2,2))
    assert not p.isHealthy
    assert not p.isDead
    assert p.isInfected
    assert str(p) == "/."

    assert p.firstDayOfInfection == 1
    assert p.infectionDays == 2
    assert not p.getHealthy(1)
    assert not p.getHealthy(2)
    assert p.getHealthy(3)

    # p is now healthy
    assert p.isHealthy
    assert p.isImmune
    assert str(p) == "hX"

    p.infect(1, (2,2))
    assert p.isHealthy

    p = Person(0,0)
    p.infect(1, (2,2))
    assert not p.die(0)
    assert p.die(1.0)
    assert p.isDead
    assert not p.isHealthy
    assert not p.isInfected
    print("Passed all tests")
