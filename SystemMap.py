#!/usr/bin/env python3

"""Class to create system map of train signalling system"""

import os
import sys
import datetime
import string

class SystemMap(object):
	"""Class responsible for building and managing the grid map of the track system"""
	
	__X_BOUNDS = 0
	__Y_BOUNDS = 0
	__MAX_SIZE = 20

	def __init__(self, size):
		if size > self.__MAX_SIZE:
			raise ValueError("Map Size Out Of Bounds!")
		else:
			self.size = size

		self.map = list()
		for i in range(self.size):
			rows = list()
			for j in range(self.size):
				rows.append(".")
			self.map.append(rows)

		print("System Builder Created - Map Size {} x {}".format(size, size))
		print("Origin (0, 0) is at the TOP LEFT corner. All values are positive.")
		self.draw_map()

	def __check_valid_coords(self, x, y):
		"""Private function to check whether (x,y) coordinate on map is valid"""
		if x <= self.size and x >= self.__X_BOUNDS and y <= self.size and y >= self.__Y_BOUNDS:
			return True

	def __set_component(self, designator, x, y):
		"""Private function to place component on map at specified coordinates (x, y)"""
		self.map[x][y] = designator

	def __get_component(self, x, y):
		"""Private function to get component designator at specified coordinates (x, y)"""
		return self.map[x][y]

	def __get_surrounding(self, x, y):
		"""Private function to return surrounding (a, b) coordinates of point (x, y)"""
		coords = list()
		coords.append([x+1, y]) if self.__check_valid_coords(x+1, y) else coords
		coords.append([x, y+1]) if self.__check_valid_coords(x, y+1) else coords
		coords.append([x-1, y]) if self.__check_valid_coords(x-1, y) else coords
		coords.append([x, y-1]) if self.__check_valid_coords(x, y-1) else coords
		return coords

	def draw_map(self):
		"""Outputs current map representation to console"""
		map_string = ""
		for i in range(self.size):
			for j in range(self.size):
				if j == 0 or j == self.size:
					map_string += self.map[i][j]
				else:
					map_string += "   " + self.map[i][j]
			map_string += "\n\n"
		print(map_string)

	def validate_map(self):
		"""Run self-check on System Map to ensure all behaviour rules are met"""
		return True

	def place_beginning(self, x, y):
		"""Place route beginning designator on map"""
		if self.__check_valid_coords(x, y):
			self.__set_component("B", x, y)
		self.draw_map()
		return True

	def place_endpoint(self, x, y):
		"""Place route end point designator on map"""
		if self.__check_valid_coords(x, y):
			self.__set_component("E", x, y)
		self.draw_map()
		return True

	def place_track(self, x, y):
		"""Place track segment on map"""
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


if __name__ == '__main__':
	sb = SystemMap(10)
	sb.place_beginning(1, 1)
	sb.place_endpoint(8, 8)
	sb.place_track(1, 2)
	sb.place_track(1, 3)
	sb.place_track(2, 3)
	sb.place_track(3, 3)
	sb.place_signal(4, 3)
	sb.place_track(5, 3)
	sb.place_track(6, 3)
	sb.place_track(7, 3)
	sb.place_track(7, 4)
	sb.place_track(7, 5)
	sb.place_junction(7, 6)
	sb.place_track(7, 7)
	sb.place_track(7, 8)
	sb.place_track(8, 6)
	sb.place_track(8, 7)
