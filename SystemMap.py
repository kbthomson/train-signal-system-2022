#!/usr/bin/env python3

"""Class to create and manage the map of the Train Signaling System"""

import os
import sys
import datetime
import string
import Constants
from SystemClasses import BeginningPoint, EndPoint, TrackSegment, Signal, Junction, Train


class SystemMap(object):
	"""Class responsible for building and managing the map (Cartesian grid)"""
	def __init__(self, size):
		if size > Constants.MAX_SIZE:
			raise ValueError("Map Size Out Of Bounds !!!")
		else:
			self.__size = size

		self.__map = list()
		for i in range(self.__size):
			row = [None] * self.__size
			self.__map.append(row)

		print("System Builder Created - Map Size {} x {}".format(self.__size, self.__size))
		print("Origin (0, 0) is at the TOP LEFT corner - All values are positive")
		self.draw_map()

	def get_size(self):
		return self.__size

	def get_map(self):
		return self.__map

	def check_valid_coords(self, x, y):
		"""Function to check whether (x,y) coordinate on the map are valid"""
		if x < self.__size and x >= Constants.X_BOUNDS and y < self.__size and y >= Constants.Y_BOUNDS:
			return True

	def get_surrounding_coords(self, x, y):
		"""Function to return valid, surrounding coordinates of point (x, y)"""
		coords = list()
		for k in Constants.DIRECTION.keys():
			direction = Constants.DIRECTION[k]
			pos = [x, y]
			pos[0] += direction[0]
			pos[1] += direction[1]
			coords.append(pos) if self.check_valid_coords(pos[0], pos[1]) else coords
		return coords

	def count_surrounding_objects(self, x, y):
		"""Function to return count of object types surrounding point (x, y)"""
		surround_obj = list()
		coords = self.get_surrounding_coords(x, y)
		for pos in coords:
			if self.__map[pos[0]][pos[1]] is not None:
				surround_obj.append(self.__map[pos[0]][pos[1]].get_type())
		return surround_obj

	def draw_map(self, train=None):
		"""Outputs current map representation to console"""
		map_string = ""
		for i in range(self.__size):
			for j in range(self.__size):
				if j == 0 or j == self.__size:
					if self.__map[i][j] is None:
						map_string += "."
					else:
						if train is not None and i == train.get_x() and j == train.get_y():
							map_string += train.get_designator()
						else:
							map_string += self.__map[j][i].get_designator()
				else:
					if self.__map[j][i] is None:
						map_string += "   ."
					else:
						if train is not None and i == train.get_x() and j == train.get_y():
							map_string += "   " + train.get_designator()
						else:
							map_string += "   " + self.__map[j][i].get_designator()
			map_string += "\n\n"
		print(map_string)

	def validate_direction(self, obj):
		"""Check placement of object with direction property on map"""
		x = obj.get_x()
		y = obj.get_y()
		tmp_move = Constants.DIRECTION[obj.get_direction()]
		check_dir = [x+tmp_move[0], y+tmp_move[1]]
		if self.__map[check_dir[0]][check_dir[1]] is None:
			print("Invalid Direction property for TrackObject at ({}, {})".format(x, y))
			print("Map must have object in Direction of movement")
			return False
		return True

	def validate_map(self):
		"""Check placement of all objects on map before running"""
		b_count = 0
		e_count = 0
		for i in range(self.__size):
			for j in range(self.__size):
				nearby = list()
				if self.__map[i][j] is not None:
					nearby = self.count_surrounding_objects(i, j)
					if self.__map[i][j].get_type() == "Junction":
						if not self.validate_direction(self.__map[i][j]):
							return False
						elif len(nearby) < 3:
							print("Invalid placement of Junction at ({}, {})".format(i, j))
							print("Junctions must have at least 3 surrounding objects")
							return False
					else:
						if self.__map[i][j].get_type() == "Begin":
							b_count += 1
						if self.__map[i][j].get_type() == "End":
							e_count += 1
						if len(nearby) < 1:
							print("Invalid placement of Track Object at ({}, {})".format(i, j))
							print("Track Objects must have at least 1 surrounding objects")
							return False
		if b_count + e_count < 2:
			print("Map must have at least 2 objects present. Map requires 1 BeginningPoint and 1 EndPoint")
			return False
		return True

	def place_beginning(self, x, y):
		"""Place BeginningPoint object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = BeginningPoint(x, y)
			print("BeginningPoint object added to map ({}, {})".format(x, y))
			self.draw_map()

	def place_endpoint(self, x, y):
		"""Place EndPoint object map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = EndPoint(x, y)
			print("EndPoint object added to map ({}, {})".format(x, y))
			self.draw_map()

	def place_track(self, x, y):
		"""Place TrackSegment object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = TrackSegment(x, y)
			print("TrackSegment object added to map ({}, {})".format(x, y))
			self.draw_map()

	def place_signal(self, x, y, state):
		"""Place Signal object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = Signal(x, y, state)
			print("Signal object added to map ({}, {})".format(x, y))
			self.draw_map()

	def place_junction(self, x, y, direction):
		"""Place Junction object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = Junction(x, y, direction)
			print("Junction object added to map ({}, {})".format(x, y))
			self.draw_map()

	def clear_map(self):
		"""Clears all objects in a train map to reset the grid"""
		self.__map = list()
		for i in range(self.__size):
			row = [None] * self.__size
			self.__map.append(row)
		print("System Builder Reset - Map Size {} x {}".format(self.__size, self.__size))
		print("Origin (0, 0) is at the TOP LEFT corner - All values are positive")
		self.draw_map()

	def preset_map(self):
		"""Build a sample train map for testing and validation"""
		sm.place_beginning(1, 1)
		sm.place_track(2, 1)
		sm.place_junction(3, 1, "DOWN")
		sm.place_track(4, 1)
		sm.place_track(5, 1)
		sm.place_track(5, 2)
		sm.place_junction(5, 3, "RIGHT")
		sm.place_track(5, 4)
		sm.place_junction(5, 5, "DOWN")
		sm.place_track(5, 6)
		sm.place_junction(5, 7, "UP")
		sm.place_track(5, 8)
		sm.place_track(6, 8)
		sm.place_track(7, 8)

		sm.place_track(6, 3)
		sm.place_track(7, 3)
		sm.place_signal(8, 3, "RED")
		sm.place_track(9, 3)
		sm.place_track(9, 4)
		sm.place_junction(9, 5, "UP")
		sm.place_track(8, 5)
		sm.place_track(7, 5)
		sm.place_track(6, 5)

		sm.place_track(1, 2)
		sm.place_track(3, 2)
		sm.place_signal(3, 3, "GREEN")
		sm.place_track(2, 3)
		sm.place_junction(1, 3, "DOWN")
		sm.place_track(1, 4)
		sm.place_signal(1, 5, "RED")
		sm.place_track(1, 6)
		sm.place_track(1, 7)
		sm.place_track(2, 7)
		sm.place_signal(3, 7, "GREEN")
		sm.place_track(4, 7)

		sm.place_track(9, 6)
		sm.place_signal(9, 7, "RED")
		sm.place_track(9, 8)

		sm.place_endpoint(8, 8)

'''
if __name__ == '__main__':
	sm = SystemMap(10)
	sm.place_beginning(1, 1)
	sm.place_track(1, 2)
	sm.place_endpoint(1, 3)
	#sm.preset_map()
	sm.validate_map()
'''
