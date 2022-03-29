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


class Signal(object):
	"""Signal class to control the flow of traffic along track segments"""

	__SIGNAL_STATES = ['GREEN', 'RED']

	def __init__(self, x, y, state):
		super(TrackObject, self).__init__()
		if state.upper() not in __SIGNAL_STATES:
			raise ValueError("Invalid Signal State Given!")
		else:
			self.state = state.upper()


class Junction(object):
	"""Junction class to direct train traffic only to one of the forked tracks at a given time"""

	__DIRECTIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]

	def __init__(self, x, y, direction):
		self.direction = direction

	@property
	def direction(self):
		return self.direction

	@direction.setter
	def direction(self, new_direction):
		self.direction = new_direction
