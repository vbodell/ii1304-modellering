from person import Person

class Population:
    def __init__(self, simulation, N, infected):
        self.N = N
        self._simulation = simulation

        self._persons = [[Person() for _ in range(N)] for _ in range(N)]
        for x in range(N):
            for y in range(N):
                self._persons[x][y].setNeighbors(self.getNeighbors(x,y, True))

        self.currentSimulationDay = 0

        for (x,y) in infected:
            self._persons[x][y].infect(self.currentSimulationDay, 1)

    def getNeighbors(self, x, y, verbose=False):
        neighbors = []
        indices = []
        for xOffs in range(-1,2):
            for yOffs in range(-1,2):
                # Wraparound so that every individual has 8 neighbors
                nX = (x + xOffs) % self.N if (x + xOffs) != -1 else self.N - 1
                nY = (y + yOffs) % self.N if (y + yOffs) != -1 else self.N - 1
                if self.validPosition(nX, nY) and not (nX == x and nY == y):
                    neighbors.append(self._persons[nX][nY])
                    indices.append((nX,nY))
        if verbose:
            print("[%d,%d] has %d neighbors: %s" % (x,y,len(neighbors),indices))
        return neighbors

    def validPosition(self, x, y):
        # if not (x >= 0 and x < self.N) and (y >= 0 and y < self.N):
        #     print("Invalid Position?!")
        return (x >= 0 and x < self.N) and (y >= 0 and y < self.N)

    @property
    def currentInfectedIndividuals(self):
        return [p for row in self._persons for p in row if p.isInfected]

    def __str__(self):
        s = "\n"
        for x in range(self.N):
            for y in range(self.N):
                s += str(self._persons[x][y]) + " "
            s += "\n"
        return s

    @property
    def allDead(self):
        return all([p.isDead for row in self._persons for p in row])

    @property
    def allHealthy(self):
        return all([p.isHealthy for row in self._persons for p in row])

    def simulateDay(self, day):
        self.currentSimulationDay = day

        todaysDeathCount = todaysInfectionCount = todaysGotHealthyCount = 0

        #TODO Clear this up as well...:
        # Infected people whose period of sickness is up get healthy


        # Infect neighbor with probabiltiy probInfect, number of days neighbor
        #  becomes sick is a random integer in the interval [minDays, maxDays]

        # Die with probability probDeath

        return {'infected': len(self.currentInfectedIndividuals),
                'died': 0,
                'gotHealthy': 0,
                'gotInfected': 0}
