import sys
from simulation import Simulation

class UI:
    N = 8
    probInfect = 0.5
    minDaysSick = 2
    maxDaysSick = 4
    probDeath = 0.5
    initialSick = 7 # 10%
    initialSickNdx = [(i,i) for i in range(initialSick)]

    def __init__(self, verbose, seed):
        self.verbose = verbose
        self.seed = seed
        self.simulation = None

    def initSimulation(self):
        print("### Welcome to the virus simulation ###\n\n")
        print("To start the simulation, please fill in the following values (or press Enter to use the [default] value)")

        N = input("Enter population parameter N [%d]: " % UI.N)
        N = int(N) if N else UI.N
        if N < 0:
            print("Invalid N entered. Terminating.")
            sys.exit(1)

        probInfect = input("Probability of infecting neighbor [%.2f]: " % UI.probInfect)
        probInfect = float(probInfect) if probInfect else UI.probInfect
        if probInfect < 0.0 or probInfect > 1.0:
            print("Invalid probability entered. Terminating.")
            sys.exit(1)

        minDaysSick = input("Minimum days of sickness [%d]: " % UI.minDaysSick)
        minDaysSick = int(minDaysSick) if minDaysSick else UI.minDaysSick
        if minDaysSick < 1:
            print("Invalid minimum number of days entered. Terminating.")
            sys.exit(1)

        maxDaysSick = input("Maximum days of sickness [%d]: " % UI.maxDaysSick)
        maxDaysSick = int(maxDaysSick) if maxDaysSick else UI.maxDaysSick
        if maxDaysSick < minDaysSick:
            print("Max days cannot be less than min days. Terminating.")
            sys.exit(1)

        probDeath = input("Probability of dying during sickness [%.2f]: " % UI.probDeath)
        probDeath = float(probDeath) if probDeath else UI.probDeath
        if probDeath < 0.0 or probDeath > 1.0:
            print("Invalid probability entered. Terminating.")
            sys.exit(1)

        initialSick = input("Initial number of sick people [%d]: " % UI.initialSick)
        initialSick = int(initialSick) if initialSick else UI.initialSick
        if initialSick < 0 or initialSick > N*N:
            print("Invalid number of sick entered (must be in the interval [0,N*N]). Terminating.")
            sys.exit(1)

        if initialSick != UI.initialSick:
            initialSickNdx = self._readInitialSick(initialSick, N)
        else:
            ansPrompt = "You choose the default value for initial sick,\n" +\
             " do you wish to specify your own positions still? [Y/N]: "
            ans = input(ansPrompt)
            if ans in ['y','Y']:
                initialSickNdx = self._readInitialSick(initialSick, N)
            else:
                initialSickNdx = UI.initialSickNdx

        self.simulation = Simulation(N, probInfect, minDaysSick, maxDaysSick,
         probDeath, initialSickNdx, self.verbose, self.seed)


    def _readInitialSick(self, initialSick, upperBound):
        initSickPos = []

        for ndx in range(initialSick):
            xy = input("Enter positions for sick person #%d (separated by comma): " % (ndx+1))
            (x,y) = xy.split(',')
            x = int(x)
            y = int(y)

            if x < 0 or x >= upperBound or y < 0 or y >= upperBound or (x,y) in initSickPos:
                print("Invalid index, must be in interval [0,%d) and cannot be same as a previous position. Terminating" % upperBound)
                sys.exit(1)

            initSickPos.append((x,y))

        return initSickPos

    def startSimulation(self):
        if self.simulation:
            self.simulation.start()
