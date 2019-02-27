from population import Population

class Simulation:
    def __init__(self, N, probInfect, minDaysSick, maxDaysSick, probDeath,
     initialSick, VERBOSE, SEED):

        self.N = N
        self.probInfect = probInfect
        self.totalSickCount = len(initialSick)
        self.totalDeathCount = 0

        self.printInitString(VERBOSE, SEED, N, probInfect, minDaysSick,
         maxDaysSick, probDeath, initialSick)

        self.currentSimulationDay = 0
        self._population = Population(N, probInfect, minDaysSick,
         maxDaysSick, probDeath, initialSick, VERBOSE, SEED)
        print(self._population)

    def start(self):
        while not self.simulationFinished():
            self.currentSimulationDay += 1
            values = self._population.simulateDay(self.currentSimulationDay)

            self.printDailyReport(values)
            self.totalSickCount += values['gotInfected']
            self.totalDeathCount += values['died']

        self.printCumulativeReport()

    def simulationFinished(self):
        return self._population.allDead or self._population.allLivingHealthy

    def printDailyReport(self, values):
        print("Day %d:" % self.currentSimulationDay)
        print(" # got infected: %d" % values['gotInfected'])
        print(" # deaths:       %d" % values['died'])
        print(" # got healthy:  %d" % values['gotHealthy'])
        print(" # infected:     %d" % values['infected'])
        print(self._population)

    def printCumulativeReport(self):
        if not self.simulationFinished():
            print("Simulation hasn't terminated yet!")
            return

        print("===Simulation ran a total of %d days===" % self.currentSimulationDay)
        print("   Total # of infected: %d" % self.totalSickCount)
        print("   Total # of deaths:   %d" % self.totalDeathCount)
        print("   Proportion infected: %.3f" % (self.totalSickCount/(self.N*self.N)))
        print("CSV:%.3f,%.3f" % (self.probInfect, self.totalSickCount/(self.N*self.N)))

    def printInitString(self, VERBOSE, SEED, N, probInfect,
     minDaysSick, maxDaysSick, probDeath, initialSick):
        initSimString = "\n### Initializing simulation with the" +\
         " following parameters ###\n"
        initSimString += " Verbose=%s\n" % VERBOSE
        initSimString += " SEED=%s\n" % SEED
        initSimString += "   N=%d\n" % N
        initSimString += "   probInfect=%.2f\n" % probInfect
        initSimString += "   minDaysSick=%d\n" % minDaysSick
        initSimString += "   maxDaysSick=%d\n" % maxDaysSick
        initSimString += "   probDeath=%.2f\n" % probDeath
        initSimString += "   initialSick=%d\n" % len(initialSick)

        for ndx in range(len(initialSick)):
            initSimString += "      Sick position #%d: [%d,%d]\n" % (ndx+1,
             initialSick[ndx][0], initialSick[ndx][1])

        print(initSimString)
