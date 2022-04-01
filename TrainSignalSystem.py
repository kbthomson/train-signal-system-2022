#!/usr/bin/env python3

"""Train Signal System Main Python Script"""

import os
import sys
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
			size = int(input("Enter a grid size for the track map (N x N): "))
			if size <= Constants.X_BOUNDS:
				print("Size cannot be zero or a negative integer\n")
			elif size > Constants.MAX_SIZE:
				print("Size cannot be greater than {}\n".format(Constants.MAX_SIZE))
			else:
				status = False
		except ValueError as e:
			print("User input must be an integer\n")
	return size


def GetUserCommand():
	"""Parse and restrict user input to set of commands"""
	status = True
	while status:
		try:
			char = str(input("Enter a command for the Train Signal System: "))
			if char.upper() not in Constants.CMD_LIST:
				print("Please enter a valid command character - Press 'H' to get command help\n")
			else:
				status = False
		except ValueError as e:
			print("User input must be a character\n")
	return char.upper()

def GetCoordinates():
	pass


def TrainSignalSystem():
	"""Main function for building and running the Train Signal System"""
	quit = False
	end = False
	sm = None

	print("~~~ Welcome to the Track Signal System ~~~")
	print("You will build a track and have the train run along it")
	print("Begin by setting the grid size for the track map\n")
	map_size = EnterMapSize()
	sm = SystemMap(map_size)

	print("Build and run the simulation using the following commands\n")
	print(Constants.CMD_STR)

	while not quit and not end:
		cmd = GetUserCommand()

		if cmd == "B":
			b_x, b_y = GetCoordinates()
			try:
				sm.place_beginning(b_x, b_y)
			except ValueError as v:

		elif cmd == "E":
			e_x, e_y = GetCoordinates()
			sm.place_endpoint(e_x, e_y)

		elif cmd == "T":
			t_x, t_y = GetCoordinates()
			sm.place_track(t_x, t_y)

		elif cmd == "S":
			s_x, s_y = GetCoordinates()
			sm.place_signal(s_x, s_y)

		elif cmd == "J":
			j_x, j_y = GetCoordinates()
			sm.place_junction(j_x, j_y)

		elif cmd == "P":
			sm.preset_map()

		elif cmd == "V":
			sm.validate_map()

		elif cmd == "C":
			sm.clear_map()

		elif cmd == "R":
			pass

		elif cmd == "H":
			print(Constants.CMD_STR)

		elif cmd == "Q":
			print("Quitting the Train Signaling System")
			quit = True


if __name__ == '__main__':
	TrainSignalSystem()
