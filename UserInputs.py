#!/usr/bin/env python3

"""Train Signal System User Input Functions"""

import os
import sys
import time
import string
import datetime
import Constants


def GetMapSize():
	"""User input for Cartesian grid size of the map"""
	status = True
	while status:
		try:
			size = int(input("--> Enter a grid size for the track map (N x N): "))
			if size <= Constants.X_BOUNDS:
				print("Size cannot be zero or a negative integer\n")
			elif size > Constants.MAX_SIZE:
				print("Size cannot be greater than {}\n".format(Constants.MAX_SIZE))
			else:
				status = False
				print("\n")
		except ValueError as v:
			print("User input must be an integer\n")
	return size


def GetUserCommand():
	"""Parse and restrict user input to set of commands"""
	status = True
	while status:
		try:
			char = str(input("--> Enter a command for the Train Signal System: "))
			if char.upper() not in Constants.CMD_LIST:
				print("Please enter a valid command character - Press 'H' to get command help\n")
			else:
				status = False
				print("\n")
		except ValueError as v:
			print("User input must be a character\n")
	return char.upper()


def GetUserConfirmation():
	"""Parse and restrict user input to 'Y' character only to confirm actions"""
	try:
		char = str(input("--> Enter 'Y' to continue, otherwise this action will cancel: "))
		if char.upper() == "Y":
			print("Action confirmed by user\n")
			return True
		else:
			print("Action will not be performed\n")
			return False
	except ValueError as v:
		print("Action will not be performed\n")
		return False


def GetCoordinates():
	"""Parse and restrict user input to entering X, Y map coordinates"""
	status = True
	while status:
		try:
			print("Enter X and Y coordinates on the system map.\nUse format: 'X,Y' with X and Y being integers separeted by a comma")
			coords = str(input("--> Enter X and Y coordinates: "))
			if coords.index(",") < 0:
				print("No comma detected as seperator\n")
			parse = coords.split(",", 1)
			x = int(parse[0].strip())
			y = int(parse[1].strip())
			if type(x) is not int or type(y) is not int:
				print("X and Y values must be integer values\n")
			else:
				status = False
				print("\n")
		except ValueError as v:
			print("Format error - please enter two integer numbers seperated by a comma")
			print("Example: '1,2'\n")
	return x, y


def GetState():
	"""Parse and restrict user input to entering GREEN or RED signal state"""
	status = True
	while status:
		try:
			print("Enter Signal State for the given coordinate.\nValue can either be 'GREEN' or 'RED'")
			state = str(input("--> Type Signal State now: "))
			if state.upper() not in Constants.SIGNAL_STATES:
				print("Value must be either 'GREEN' or 'RED'\n")
			else:
				status = False
				print("\n")
		except ValueError as v:
			print("Format error - please enter a string value of 'GREEN' or 'RED'\n")
	return state.upper()


def GetDirection():
	"""Parse and restrict user input to entering UP, DOWN, LEFT, or RIGHT grid directions"""
	status = True
	while status:
		try:
			print("Enter Direction for the given coordinate.\nValue can either be 'UP', 'DOWN', 'LEFT', or 'RIGHT'")
			direction = str(input("--> Type Direction now: "))
			if direction.upper() not in Constants.DIRECTION:
				print("Value must be either 'UP', 'DOWN', 'LEFT', or 'RIGHT'\n")
			else:
				status = False
				print("\n")
		except ValueError as v:
			print("Format error - please enter a string value of 'UP', 'DOWN', 'LEFT', or 'RIGHT'\n")
	return direction.upper()
