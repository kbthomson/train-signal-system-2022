#!/usr/bin/env python3

"""Class to manage static values and constants for the project"""

from enum import Enum


X_BOUNDS = 0
Y_BOUNDS = 0
MAX_SIZE = 20

SIGNAL_STATES = ["GREEN", "RED"]

DIRECTION = {
	"UP" 	: [0, -1],
	"DOWN"	: [0, 1],
	"LEFT" 	: [-1, 0],
	"RIGHT"	: [1, 0]
}

CMD_LIST = ["B", "E", "T", "S", "J", "I", "X", "P", "D", "V", "C", "R", "H", "A", "Q"]
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

I - [I]nspect map element for more data

X - Remove or [X]-out map element at specific location

P - Load [P]re-set map configuration

D - [D]raw current map configuration to console

V - [V]alidate map configuration before running

C - [C]lear map back to empty configuration

R - [R]un train on map to start simulation

H - [H]elp function to list all available commands

A - [A]bout the author

Q - [Q]uit
"""

AUTHOR = """
About the Author:

Kyle Thomson
kyle.b.thomson@gmail.com

"There are locomotive olympics for which you have to train really hard."

"When a train is tired, it is called a slowcomotive."

"Train drivers are known for their engine-uity!"
"""
