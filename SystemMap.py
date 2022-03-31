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
			raise ValueError("Map Size Out Of Bounds!")
		else:
			self.__size = size

		self.map = list()
		for i in range(self.__size):
			row = [None] * self.__size
			self.map.append(row)

		print("System Builder Created - Map Size {} x {}".format(self.__size, self.__size))
		print("Origin (0, 0) is at the TOP LEFT corner. All values are positive.")
		self.draw_map()

	def get_size(self):
		return self.__size

	def check_valid_coords(self, x, y):
		"""Function to check whether (x,y) coordinate on the map are valid"""
		if x <= self.__size and x >= Constants.X_BOUNDS and y <= self.__size and y >= Constants.Y_BOUNDS:
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
			if self.map[pos[0]][pos[1]] is not None:
				surround_obj.append(self.map[pos[0]][pos[1]].get_type())
		return surround_obj

	def draw_map(self):
		"""Outputs current map representation to console"""
		map_string = ""
		for i in range(self.__size):
			for j in range(self.__size):
				if j == 0 or j == self.__size:
					if self.map[i][j] is None:
						map_string += "."
					else:
						map_string += self.map[i][j].get_designator()
				else:
					if self.map[i][j] is None:
						map_string += "   ."
					else:
						map_string += "   " + self.map[i][j].get_designator()
			map_string += "\n\n"
		print(map_string)

	def place_beginning(self, x, y):
		"""Place BeginningPoint object on map"""
		if self.check_valid_coords(x, y):
			self.map[x][y] = BeginningPoint(x, y)
		print("BeginningPoint object added to map ({}, {})".format(x, y))
		self.draw_map()

	def place_endpoint(self, x, y):
		"""Place EndPoint object map"""
		if self.check_valid_coords(x, y):
			self.map[x][y] = EndPoint(x, y)
		print("EndPoint object added to map ({}, {})".format(x, y))
		self.draw_map()

	'''
	def place_track(self, x, y):
		"""Place TrackSegment object on map"""
		component_found = False
		if self.__check_valid_coords(x, y) and self.__get_component(x, y) == ".":
			positions = self.__get_surrounding(x, y)
			for pos in positions:
				if self.__get_component(pos[0], pos[1]) != ".":
					component_found = True
					self.__set_component("T", x, y)
			if not component_found:
				print("Cannot place TRACK at ({}, {}) with no surrounding connections.".format(x, y))
				return False
		else:
			print("Component already present at at ({}, {}).".format(x, y))
			return False
		self.draw_map()
		return True

	def place_signal(self, x, y):
		"""Place signal component on map"""
		component_found = False
		if self.__check_valid_coords(x, y) and self.__get_component(x, y) == ".":
			positions = self.__get_surrounding(x, y)
			for pos in positions:
				if self.__get_component(pos[0], pos[1]) != ".":
					component_found = True
					self.__set_component("S", x, y)
			if not component_found:
				print("Cannot place SIGNAL at ({}, {}) with no surrounding connections.".format(x, y))
				return False
		else:
			print("Component already present at at ({}, {}).".format(x, y))
			return False
		self.draw_map()
		return True

	def place_junction(self, x, y):
		"""Place junction component on map"""
		component_found = False
		junct_count = 0
		junct_list = list()
		if self.__check_valid_coords(x, y) and self.__get_component(x, y) == ".":
			positions = self.__get_surrounding(x, y)
			for pos in positions:
				if self.__get_component(pos[0], pos[1]) != ".":
					component_found = True
					junct_count += 1
					self.__set_component("J", x, y)
				else:
					junct_list.append(pos)
			if not component_found:
				print("Cannot place JUNCTION at ({}, {}) with no surrounding connections.".format(x, y))
				return False
			if junct_count < 2:
				print("Junction must have an INPUT and TWO OUTPUTS. Please add component to {} of the following coordinates:".format(2-junct_count))
				for i in range(len(junct_list)):
					print("{} - {}".format(i+1, junct_list[i]))
		else:
			print("Component already present at at ({}, {}).".format(x, y))
			return False
		self.draw_map()
		return True
	'''

if __name__ == '__main__':
	sm = SystemMap(10)
	sm.place_beginning(0, 2)
	sm.place_beginning(1, 1)
	sm.place_endpoint(2, 2)
	sm.place_endpoint(1, 3)
	num = sm.count_surrounding_objects(1, 2)
	print(num)
	beg = num.count('Begin')
	end = num.count('End')
	print(beg)
	print(end)

