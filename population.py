from person import Person

class Population:
    def __init__(self, N, probInfect, minDaysSick, maxDaysSick,
     probDeath, infected, VERBOSE, SEED):
        self.N = N

        self.probInfect = probInfect
        self.minDaysSick = minDaysSick
        self.maxDaysSick = maxDaysSick
        self.probDeath = probDeath

        if VERBOSE:
            Person.VERBOSE = True
        if SEED:
            Person.setSeed(SEED)

        self._persons = [[Person(x,y) for y in range(N)] for x in range(N)]
        for x in range(N):
            for y in range(N):
                self._persons[x][y].setNeighbors(self.getNeighbors(x,y, VERBOSE))

        self.currentSimulationDay = 0

        for (x,y) in infected:
            self._persons[x][y].infect(self.currentSimulationDay,
                                       (self.minDaysSick, self.maxDaysSick))

    def getNeighbors(self, x, y, verbose=False):
        # Get the immediate neighbors for a person with position (x,y)
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
    def allLivingHealthy(self):
        return all([p.isHealthy for row in self._persons for p in row if not p.isDead])

    def simulateDay(self, day):
        self.currentSimulationDay = day

        deathCount = infectedCount = gotHealthyCount = 0

        # Infected people whose period of sickness is up get healthy
        for p in self.currentInfectedIndividuals:
            gotHealthyCount += p.getHealthy(day)

        # Infect neighbor with probabiltiy probInfect, number of days neighbor
        #  becomes sick is a random integer in the interval [minDays, maxDays]
        # Note that the list of infected has now updated accounting for healthy
        for p in self.currentInfectedIndividuals:
            infectedCount += p.infectNeighbors(self.probInfect, day,
                              (self.minDaysSick, self.maxDaysSick))

        # Die with probability probDeath
        for p in self.currentInfectedIndividuals:
            deathCount += p.die(self.probDeath)

        return {'infected': len(self.currentInfectedIndividuals),
                'died': deathCount,
                'gotHealthy': gotHealthyCount,
                'gotInfected': infectedCount}
