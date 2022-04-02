#!/usr/bin/env python3

"""Train Signal System Main Python Script"""

import os
import sys
import time
import datetime
import string
import argparse
import Constants
from SystemClasses import BeginningPoint, EndPoint, TrackSegment, Signal, Junction, Train
from SystemMap import SystemMap


def EnterMapSize():
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
		except ValueError as e:
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
		except ValueError as e:
			print("User input must be a character\n")
	return char.upper()


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


######################################################################################
###                                      MAIN                                      ###
######################################################################################

def TrainSignalSystem():
	"""Main function for building and running the Train Signal System"""
	quit = False
	end = False
	sm = None

	print("\n~~~ Welcome to the Track Signal System ~~~")
	print("You will build a track and have a train run along it\n")
	print("Begin by setting the grid size for the track map")
	map_size = EnterMapSize()
	sm = SystemMap(map_size)

	input("System Map created - press any button to continue ... \n")
	print("Build and run the simulation using the following commands\n")
	print(Constants.CMD_STR)

	while not quit and not end:
		cmd = GetUserCommand()

		if cmd == "B":
			b_x, b_y = GetCoordinates()
			try:
				sm.place_beginning(b_x, b_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "E":
			e_x, e_y = GetCoordinates()
			try:
				sm.place_endpoint(e_x, e_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "T":
			t_x, t_y = GetCoordinates()
			try:
				sm.place_track(t_x, t_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "S":
			s_x, s_y = GetCoordinates()
			state = GetState()
			try:
				sm.place_signal(s_x, s_y, state)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "J":
			j_x, j_y = GetCoordinates()
			direction = GetDirection()
			try:
				sm.place_junction(j_x, j_y, direction)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "I":
			i_x, i_y = GetCoordinates()
			print("Inspecting coordinate ({}, {}) for more information".format(i_x, i_y))
			sm.inspect_coordinate(i_x, i_y)

		elif cmd == "X":
			x_x, x_y = GetCoordinates()
			print("Removing element at coordinate ({}, {}) from map".format(x_x, x_y))
			sm.remove_object(x_x, x_y)

		elif cmd == "P":
			print("Using preset map configuration will clear any existing work")
			try:
				char = str(input("--> Enter 'Y' to continue, otherwise this action will cancel: "))
				if char.upper() == "Y":
					sm.clear_map()
					sm.preset_map()
				else:
					print("\n")
			except ValueError as v:
				print("\n")
				pass

		elif cmd == "D":
			print("Outputting current map configuration to console\n")
			sm.draw_map()

		elif cmd == "V":
			print("Validating current map configuration\n")
			if sm.validate_map():
				print("System map configuration is valid\n")

		elif cmd == "C":
			print("This command will clear any existing work and reset the map")
			try:
				char = str(input("--> Enter 'Y' to continue, otherwise this action will cancel: "))
				if char.upper() == "Y":
					sm.clear_map()
				else:
					print("\n")
			except ValueError as v:
				print("\n")
				pass

		elif cmd == "R":
			print("~~~ Running TrainSignalSystem Simuation ~~~\n")
			result, path = sm.map_bfs()
			if result:
				print("!!! Path found between BeginningPoint and EndPoint !!!\n")
				for i in range(len(path)):
					print("Move #{} - {}".format(i+1, path[i]))
				print("!!! Train leaving the station !!!")
				begin = sm.get_begin()
				t = Train(begin[0], begin[1], path[0], False)
				sm.draw_map(t)
				time.sleep(1.5)
				for moves in path:
					t.set_direction(moves)
					t.set_moving(True)
					t.move()
					time.sleep(1.5)
					sm.draw_map(t)
				print("!!! Train has arrived !!!")
			else:
				print("XXX Error, path could not be completed between BeginningPoint and EndPoint XXX\n")

		elif cmd == "H":
			print(Constants.CMD_STR)

		elif cmd == "A":
			print(Constants.AUTHOR)

		elif cmd == "Q":
			print("~~~ Quitting the Train Signaling System ~~~\n")
			quit = True


if __name__ == '__main__':
	TrainSignalSystem()
