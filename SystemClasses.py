#!/usr/bin/env python3

"""Create base classes for building and running Train Signaling System

Class list:
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


class Signal(object):
	"""Signal class to control the flow of traffic along track segments"""

	def __init__(self, x, y, state):
		self.x = x
		self.y = y
		self.type = "SIGNAL"
		self.designator = "S"
		if state.upper() not in Constants.SIGNAL_STATES:
			raise ValueError("Invalid Signal State Given!")
		else:
			self.state = state.upper()

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_pos(self):
		return [self.x, self.y]

	def get_type(self):
		return self.type

	def get_designator(self):
		return self.designator
		
	def get_state(self):
		return self.state

	def set_state(self, new_state):
		if new_state.upper() not in Constants.SIGNAL_STATES:
			raise ValueError("Invalid Signal State Given!")
		else:
			self.state = new_state.upper()


class Junction(object):
	"""Junction class to direct train traffic only to one of the forked tracks at a given time"""

	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.type = "JUNCTION"
		self.designator = "J"
		if direction.upper() not in Constants.DIRECTIONS:
			raise ValueError("Invalid Junction Direction Given!")
		else:
			self.direction = direction.upper()

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_pos(self):
		return [self.x, self.y]

	def get_type(self):
		return self.type

	def get_designator(self):
		return self.designator
		
	def get_direction(self):
		return self.direction

	def set_direction(self, new_direction):
		if new_direction.upper() not in Constants.DIRECTIONS:
			raise ValueError("Invalid Junction Direction Given!")
		else:
			self.direction = new_direction.upper()


class Train(object):
	"""Train class represents moving object with starting position and direction moving towards endpoint"""

	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.type = "TRAIN"
		self.designator = "*"
		self.moving = False
		if direction.upper() not in Constants.DIRECTIONS:
			raise ValueError("Invalid Junction Direction Given!")
		else:
			self.direction = direction.upper()

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_pos(self):
		return [self.x, self.y]

	def get_type(self):
		return self.type

	def get_designator(self):
		return self.designator

	def get_moving(self):
		return self.moving

	def set_moving(self, bool):
		if bool:
			self.moving = True
		else:
			self.moving = False
		
	def get_direction(self):
		return self.direction

	def set_direction(self, new_direction):
		if new_direction.upper() not in Constants.DIRECTIONS:
			raise ValueError("Invalid Train Direction Given!")
		else:
			self.direction = new_direction.upper()

	def move_train(self, direction):
		movement = list()
		if not self.moving:
			raise Exception("Train Is Stopped - It Must Be Set To Moving First")
		if direction.upper() not in Constants.DIRECTIONS:
			raise ValueError("Invalid Train Direction Given!")

		if direction == "UP":
			movement = Constants.UP
		elif direction == "DOWN":
			movement = Constants.DOWN	
		elif direction == "LEFT":
			movement = Constants.LEFT
		elif direction == "RIGHT":	
			movement = Constants.RIGHT

		new_x = self.x + movement[0]
		new_y = self.y + movement[1]
		if new_x <= Constants.MAX_SIZE and new_x >= Constants.X_BOUNDS and new_y <= Constants.MAX_SIZE and new_y >= Constants.Y_BOUNDS:
			self.x = new_x
			self.y = new_y
			self.direction = direction


if __name__ == '__main__':
	s = Signal(2, 2, "GREEN")
	j = Junction(4, 4, "DOWN")
	t = Train(0, 0, "RIGHT")
	g1 = t.get_pos()
	t.set_moving(True)
	t.move_train("DOWN")
	t.move_train("DOWN")
	t.move_train("DOWN")
	g2 = t.get_pos()

	print(g1)
	print(g2)		
