#!/usr/bin/env

from ui import UI

if __name__ == "__main__":
    ui = UI()

    ui.initSimulation()

    input("Press Enter to start simulation")
    ui.startSimulation()
