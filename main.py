#!/usr/bin/env python3

from ui import UI
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an infection simulation.")
    parser.add_argument('-v', '--verbose', help='Be verbose', action='store_true')
    parser.add_argument('-s', '--seed',
     help='Set seed for the random generator', type=int)
    args = vars(parser.parse_args())

    ui = UI(args['verbose'], args['seed'])

    ui.initSimulation()

    input("Press Enter to start simulation")
    ui.startSimulation()
