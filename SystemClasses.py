#!/usr/bin/env python3

"""Create base classes for objects used to build and run the Train Signaling System

Class list:
- TrackObject (BaseClass)
- BeginningPoint
- EndPoint
- TrackSegment
- Signal
- Junction
- Train
"""

import os
import sys
import datetime
import string
import Constants


class TrackObject(object):
	"""Base class for any object being placed to a coordinate on the map as part of a track"""
	def __init__(self, x, y, type, designator):
		self.__x = x
		self.__y = y
		self.__type = type
		self.__designator = designator.upper()

	def get_x(self):
		return self.__x

	def get_y(self):
		return self.__y

	def get_type(self):
		return self.__type

	def get_designator(self):
		return self.__designator

	def get_position(self):
		return [self.__x, self.__y]

	def set_x(self, new_x):
		if new_x < Constants.X_BOUNDS or new_x > Constants.MAX_SIZE:
			raise ValueError("Position X value is out of bounds")
		self.__x = new_x

	def set_y(self, new_y):
		if new_y < Constants.Y_BOUNDS or new_y > Constants.MAX_SIZE:
			raise ValueError("Position Y value is out of bounds")
		self.__y = new_y

	def set_type(self, new_type):
		if type(new_type) is not str:
			raise TypeError("Type property must be a string value")
		self.__type = new_type

	def set_designator(self, new_designator):
		if len(new_designator) != 1:
			raise ValueError("Designator property must be a single character")
		if type(new_designator) is not str:
			raise TypeError("Designator property must be a string value")
		self.__designator = new_designator.upper()

	def set_position(self, new_pos):
		if len(new_pos) != 2:
			raise IndexError("Position must be array of 2 elements - Length given was: {}".format(len(new_pos)))
		self.set_x(new_pos[0])
		self.set_y(new_pos[1])


class BeginningPoint(TrackObject):
	"""Class reprenting the Beginning Track Segment on the grid"""
	def __init__(self, x, y):
		super().__init__(x, y, "Begin", "B")


class EndPoint(TrackObject):
	"""Class reprenting the Ending Track Segment on the grid"""
	def __init__(self, x, y):
		super().__init__(x, y, "End", "E")


class TrackSegment(TrackObject):
	"""Class reprenting a Track Segment object on the grid"""
	def __init__(self, x, y):
		super().__init__(x, y, "TrackSegment", "T")


class Signal(TrackObject):
	"""Class reprenting a Track Segment object with a Signal on the grid"""
	def __init__(self, x, y, state):
		super().__init__(x, y, "Signal", "S")
		self.__state = state
		if self.__state == "RED":
			self.set_designator("R")
		elif self.__state == "GREEN":
			self.set_designator("G")

	def get_state(self):
		return self.__state

	def set_state(self, new_state):
		if new_state.upper() not in Constants.SIGNAL_STATES:
			raise ValueError("State must be given value of GREEN or RED only")
		self.__state = new_state.upper()
		
		if self.__state == "RED":
			self.set_designator("R")
		elif self.__state == "GREEN":
			self.set_designator("G")


class Junction(TrackObject):
	"""Class reprenting a Track Junction object on the grid"""
	def __init__(self, x, y, direction):
		super().__init__(x, y, "Junction", "J")
		self.__direction = direction

		if self.__direction == "UP":
			self.set_designator("^")
		elif self.__direction == "DOWN":
			self.set_designator("v")
		elif self.__direction == "LEFT":
			self.set_designator("<")
		elif self.__direction == "RIGHT":
			self.set_designator(">")

	def get_direction(self):
		return self.__direction

	def set_direction(self, new_direction):
		if new_direction.upper() not in Constants.DIRECTION.keys():
			raise ValueError("Direction must be given value of UP, DOWN, LEFT, or RIGHT only")
		self.__direction = new_direction.upper()

		if self.__direction == "UP":
			self.set_designator("^")
		elif self.__direction == "DOWN":
			self.set_designator("v")
		elif self.__direction == "LEFT":
			self.set_designator("<")
		elif self.__direction == "RIGHT":
			self.set_designator(">")


class Train(TrackObject):
	"""Class reprenting a Train object which traverses the map"""
	def __init__(self, x, y, direction, moving):
		super().__init__(x, y, "Train", "*")
		self.__direction = direction
		self.__moving = moving

	def get_direction(self):
		return self.__direction

	def get_moving(self):
		return self.__moving

	def set_direction(self, new_direction):
		if new_direction.upper() not in Constants.DIRECTION.keys():
			raise ValueError("Direction must be given value of UP, DOWN, LEFT, or RIGHT only")
		self.__direction = new_direction.upper()

	def set_moving(self, boolean):
		if type(boolean) is not bool:
			raise ValueError("Moving property must be a boolean True or False value")
		self.__moving = boolean

	def move(self):
		if not self.__moving:
			raise ValueError("Train is stopped and must be set in motion before moving")
		position = self.get_position()
		movement = Constants.DIRECTION[self.__direction]
		position[0] += movement[0]
		position[1] += movement[1]
		self.set_position(position)
