from population import Population

class Simulation:
    def __init__(self, N, probInfect, minDaysSick, maxDaysSick, probDeath,
     initialSick):

        self.N = N
        self.probInfect = probInfect
        self.minDaysSick = minDaysSick
        self.maxDaysSick = maxDaysSick
        self.probDeath = probDeath
        self.initialSick = initialSick # List of positions for the initially infected

        self.totalSickCount = len(initialSick)
        self.totalDeathCount = 0

        self.printInitString()

        self.currentSimulationDay = 0
        self._population = Population(self, N, self.initialSick)
        print(self._population)


    def printInitString(self):
        initSimString = "\n### Initializing simulation with the" +\
         " following parameters ###\n"
        initSimString += "   N=%d\n" % self.N
        initSimString += "   probInfect=%.2f\n" % self.probInfect
        initSimString += "   minDaysSick=%d\n" % self.minDaysSick
        initSimString += "   maxDaysSick=%d\n" % self.maxDaysSick
        initSimString += "   probDeath=%.2f\n" % self.probDeath
        initSimString += "   initialSick=%d\n" % len(self.initialSick)

        for ndx in range(len(self.initialSick)):
            initSimString += "      Sick position #%d: [%d,%d]\n" % (ndx+1,
             self.initialSick[ndx][0], self.initialSick[ndx][1])

        print(initSimString)

    def start(self):
        while not self.simulationFinished():
            self.currentSimulationDay += 1
            values = self._population.simulateDay(self.currentSimulationDay)

            self.printDailyReport(values)
            self.totalSickCount += values['gotInfected']
            self.totalDeathCount += values['died']

        self.printCumulativeReport()

    def simulationFinished(self):
        return True
        # return self._population.allDead or self._population.allLivingHealthy or \
        #  self._population.noMoreInfections

    def printDailyReport(self, values):
        print("Day %d:" % self.currentSimulationDay)
        print("# got infected: %d" % values['gotInfected'])
        print("# deaths:       %d" % values['died'])
        print("# got healthy:  %d" % values['gotHealthy'])
        print("# infected:     %d" % values['infected'])
        print(self._population)

    def printCumulativeReport(self):
        if not self.simulationFinished():
            print("Simulation hasn't terminated yet!")
            return

        print("Simulation ran for a total of %d days" % self.currentSimulationDay) # TODO: +1?
        print("Total # of infected: %d" % self.totalSickCount)
        print("Total # of deaths:   %d" % self.totalDeathCount)
