#!/usr/bin/env python3

"""Class to manage static values and constants for the project"""

from enum import Enum


X_BOUNDS 		= 0
Y_BOUNDS 		= 0
MAX_SIZE 		= 20

SIGNAL_STATES 	= ["GREEN", "RED"]

DIRECTION = {
				"UP" 	: [0, -1],
				"DOWN"	: [0, 1],
				"LEFT" 	: [-1, 0],
				"RIGHT"	: [1, 0]
			}

CMD_LIST		= ["B", "E", "T", "S", "J", "P", "V", "C", "R", "H", "Q"]
CMD_STR = """
B - Place [B]eginningPoint object on map grid
    Inputs: x, y

E - Place [E]ndPoint object on map grid
    Inputs: x, y

T - Place [T]rackSegment object on map grid
    Inputs: x, y

S - Place [S]ignal object on map grid
    Inputs: x, y, state ("GREEN, "RED")

J - Place [J]unction object on map grid
    Inputs: x, y, direction ("UP", "DOWN", "LEFT", "RIGHT")

P - Load [P]re-set map configuration

V - [V]alidate map configuration before running

C - [C]lear map back to empty configuration

R - [R]un train on map to start simulation

H - [H]elp function to list all available commands

Q - [Q]uit\n
"""
