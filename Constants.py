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
