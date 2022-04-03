#!/usr/bin/env python3

"""Train Signal System Main Python Script"""

import os
import sys
import time
import signal
import string
import datetime
import argparse
import Constants
import UserInputs as UI
from SystemClasses import BeginningPoint, EndPoint, TrackSegment, Signal, Junction, Train
from SystemMap import SystemMap


def UserExit(signum, frame):
	"""Catch CTRL-C user event"""
	print("\n\n\n~~~ User CTRL-C Event Detected ~~~\n")
	print("~~~ Quitting the Train Signaling System ~~~\n")
	exit(0)


def TrainSignalSystem():
	"""Main function for building and running the Train Signal System"""
	quit = False
	sm = None

	print("\n~~~ Welcome to the Track Signal System ~~~")
	print("You will build a track and have a train run along it\n")
	print("Begin by setting the grid size for the track map")
	map_size = UI.GetMapSize()
	sm = SystemMap(map_size)

	input("System Map created - press any button to continue ... \n")
	print("Build and run the simulation using the following commands\n")
	print(Constants.CMD_STR)

	while not quit:
		cmd = UI.GetUserCommand()

		if cmd == "B":
			b_x, b_y = UI.GetCoordinates()
			try:
				sm.place_beginning(b_x, b_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "E":
			e_x, e_y = UI.GetCoordinates()
			try:
				sm.place_endpoint(e_x, e_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "T":
			t_x, t_y = UI.GetCoordinates()
			try:
				sm.place_track(t_x, t_y)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "S":
			s_x, s_y = UI.GetCoordinates()
			state = UI.GetState()
			try:
				sm.place_signal(s_x, s_y, state)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "J":
			j_x, j_y = UI.GetCoordinates()
			direction = UI.GetDirection()
			try:
				sm.place_junction(j_x, j_y, direction)
			except ValueError as v:
				print("\n{}\n".format(v))

		elif cmd == "I":
			i_x, i_y = UI.GetCoordinates()
			print("Inspecting coordinate ({}, {}) for more information".format(i_x, i_y))
			sm.inspect_object(i_x, i_y)

		elif cmd == "X":
			x_x, x_y = UI.GetCoordinates()
			print("Removing element at coordinate ({}, {}) from map".format(x_x, x_y))
			sm.remove_object(x_x, x_y)

		elif cmd == "P":
			print("Using preset map configuration will clear any existing work")
			if UI.GetUserConfirmation():
				sm.clear_map()
				sm.preset_map()
			
		elif cmd == "D":
			print("Outputting current map configuration to console\n")
			sm.draw_map()

		elif cmd == "V":
			print("Validating current map configuration\n")
			if sm.validate_map():
				print("System map configuration is valid\n")

		elif cmd == "C":
			print("This command will clear any existing work and reset the map")
			if UI.GetUserConfirmation():
				sm.clear_map()

		elif cmd == "R":
			print("~~~ Running TrainSignalSystem Simuation ~~~\n")
			result, path = sm.map_bfs()
			if result:
				print("!!! Path found between BeginningPoint and EndPoint !!!\n")
				for i in range(len(path)):
					print("Move #{} - {}".format(i+1, path[i]))
				print("Do you want to view the Train travelling along path found?\n")
				if UI.GetUserConfirmation():
					sm.drive_train(path)
			else:
				print("XXX Error, path could not be completed between BeginningPoint and EndPoint XXX")
				print("Please review the system map layout and run the simaulation again\n")

		elif cmd == "H":
			print(Constants.CMD_STR)

		elif cmd == "A":
			print(Constants.AUTHOR)

		elif cmd == "Q":
			print("~~~ Quitting the Train Signaling System ~~~\n")
			quit = True


if __name__ == '__main__':
	signal.signal(signal.SIGINT, UserExit)
	TrainSignalSystem()
