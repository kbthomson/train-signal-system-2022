#!/usr/bin/env python3

"""Class to create and manage the map of the Train Signaling System"""

import os
import sys
import datetime
import string
import Constants
from queue import Queue
from SystemClasses import BeginningPoint, EndPoint, TrackSegment, Signal, Junction, Train


class SystemMap(object):
	"""Class responsible for building and managing the map (Cartesian grid)"""
	def __init__(self, size):
		self.__size = size
		self.__map = list()
		self.__visited = list()
		self.__begin = [-1, -1]
		self.__end = [-1, -1]
		for i in range(self.__size):
			row = [None] * self.__size
			visit = [False] * self.__size
			self.__map.append(row)
			self.__visited.append(visit)
		self.draw_map()
		print("System Map Created - Size {} x {}".format(self.__size, self.__size))
		print("Origin (0, 0) is at the TOP LEFT corner - All values are positive\n")

	def get_size(self):
		return self.__size

	def get_map(self):
		return self.__map

	def get_visited(self):
		return self.__visited

	def get_begin(self):
		return self.__begin

	def get_end(self):
		return self.__end

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

	def get_travel_coords(self, x, y):
		"""Function to return surrounding coordinates of point (x, y) which may be traversed"""
		coords = list()
		for k in Constants.DIRECTION.keys():
			direction = Constants.DIRECTION[k]
			pos = [x, y]
			pos[0] += direction[0]
			pos[1] += direction[1]
			if self.check_valid_coords(pos[0], pos[1]) and self.__map[pos[0]][pos[1]] is not None:
				coords.append(pos)
		return coords

	def add_coords(self, pos1, pos2):
		"""Adds set of (x1, y1) coordinates to (x2, y2) coordinates and returns"""
		new_x = pos1[0] + pos2[0]
		new_y = pos1[1] + pos2[1]
		return [new_x, new_y]

	def get_surrounding_objects(self, x, y):
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
						if train is not None and j == train.get_x() and i == train.get_y():
							map_string += train.get_designator()
						else:
							map_string += self.__map[j][i].get_designator()
				else:
					if self.__map[j][i] is None:
						map_string += "   ."
					else:
						if train is not None and j == train.get_x() and i == train.get_y():
							map_string += "   " + train.get_designator()
						else:
							map_string += "   " + self.__map[j][i].get_designator()
			map_string += "\n\n"
		print(map_string)

	def inspect_coordinate(self, x, y):
		"""Outputs string representation of common object properties at location (x, y)"""
		obj = self.__map[x][y]
		if obj is None:
			print("No Track Object (None) is present at coordinates ({}, {})\n".format(x, y))
		else:
			obj_type = obj.get_type()
			print("TrackObject Type: {}".format(obj_type))
			print("{} Designator: {}".format(obj_type, obj.get_designator()))
			print("{} X Location: {}".format(obj_type, obj.get_x()))
			print("{} Y Location: {}".format(obj_type, obj.get_y()))
			if obj_type == "Signal":
				print("{} State: {}".format(obj_type, obj.get_state()))
			if obj_type == "Junction":
				print("{} Direction: {}".format(obj_type, obj.get_direction()))
			if obj_type == "Train":
				print("{} Direction: {}".format(obj_type, obj.get_direction()))
				print("{} Moving: {}".format(obj_type, obj.get_moving()))
			print("\n")

	def remove_object(self, x, y):
		"""Remove or reset element at location (x, y) from the map"""
		self.__map[x][y] = None
		self.__visited[x][y] = False
		print("Map object removed at ({}, {}) - coordinate is now 'None'\n".format(x, y))

	def validate_direction(self, obj):
		"""Check placement of object with direction property on map"""
		x = obj.get_x()
		y = obj.get_y()
		tmp_move = Constants.DIRECTION[obj.get_direction()]
		check_dir = [x+tmp_move[0], y+tmp_move[1]]
		if self.__map[check_dir[0]][check_dir[1]] is None:
			print("Invalid Direction property for TrackObject at ({}, {})".format(x, y))
			print("Map must have object in Direction of movement\n")
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
					nearby = self.get_surrounding_objects(i, j)
					if self.__map[i][j].get_type() == "Junction":
						if not self.validate_direction(self.__map[i][j]):
							return False
						elif len(nearby) < 3:
							print("Invalid placement of Junction at ({}, {})".format(i, j))
							print("Junctions must have at least 3 surrounding objects\n")
							return False
					else:
						if self.__map[i][j].get_type() == "Begin":
							b_count += 1
						if self.__map[i][j].get_type() == "End":
							e_count += 1
						if len(nearby) < 1:
							print("Invalid placement of Track Object at ({}, {})".format(i, j))
							print("Track Objects must have at least 1 surrounding objects\n")
							return False
		if b_count != 1:
			print("Map must have 1 BeginningPoint defined to run\n")
			return False
		if e_count != 1:
			print("Map must have 1 EndPoint defined to run\n")
			return False
		return True

	def place_beginning(self, x, y):
		"""Place BeginningPoint object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = BeginningPoint(x, y)
			self.__begin = [x, y]
			self.draw_map()
			print("BeginningPoint object added to map ({}, {})\n".format(x, y))
		else:
			raise ValueError("Invalid X, Y coordinate given at ({}, {})".format(x, y))

	def place_endpoint(self, x, y):
		"""Place EndPoint object map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = EndPoint(x, y)
			self.__end = [x, y]
			self.draw_map()
			print("EndPoint object added to map ({}, {})\n".format(x, y))
		else:
			raise ValueError("Invalid X, Y coordinate given at ({}, {})".format(x, y))

	def place_track(self, x, y):
		"""Place TrackSegment object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = TrackSegment(x, y)
			self.draw_map()
			print("TrackSegment object added to map ({}, {})\n".format(x, y))
		else:
			raise ValueError("Invalid X, Y coordinate given at ({}, {})".format(x, y))

	def place_signal(self, x, y, state):
		"""Place Signal object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = Signal(x, y, state)
			self.draw_map()
			print("Signal object added to map ({}, {})\n".format(x, y))
		else:
			raise ValueError("Invalid X, Y coordinate given at ({}, {})".format(x, y))

	def place_junction(self, x, y, direction):
		"""Place Junction object on map"""
		if self.check_valid_coords(x, y):
			self.__map[x][y] = Junction(x, y, direction)
			self.draw_map()
			print("Junction object added to map ({}, {})\n".format(x, y))
		else:
			raise ValueError("Invalid X, Y coordinate given at ({}, {})".format(x, y))

	def clear_map(self):
		"""Clears all objects in a train map to reset the grid"""
		self.__map = list()
		self.__visited = list()
		self.__begin = [-1, -1]
		self.__end = [-1, -1]
		for i in range(self.__size):
			row = [None] * self.__size
			visit = [False] * self.__size
			self.__map.append(row)
			self.__visited.append(visit)
		self.draw_map()
		print("System Map Reset - Size {} x {}".format(self.__size, self.__size))
		print("Origin (0, 0) is at the TOP LEFT corner - All values are positive\n")

	def preset_map(self):
		"""Build a sample train map for testing and validation"""
		self.place_beginning(1, 1)
		self.place_track(2, 1)
		self.place_junction(3, 1, "RIGHT")
		self.place_track(4, 1)
		self.place_track(5, 1)
		self.place_track(5, 2)
		self.place_junction(5, 3, "DOWN")
		self.place_track(5, 4)
		self.place_junction(5, 5, "RIGHT")
		self.place_track(5, 6)
		self.place_junction(5, 7, "DOWN")
		self.place_track(5, 8)
		self.place_track(6, 8)
		self.place_track(7, 8)

		self.place_track(6, 3)
		self.place_track(7, 3)
		self.place_signal(8, 3, "RED")
		self.place_track(9, 3)
		self.place_track(9, 4)
		self.place_junction(9, 5, "LEFT")
		self.place_track(8, 5)
		self.place_track(7, 5)
		self.place_track(6, 5)

		self.place_track(1, 2)
		self.place_track(3, 2)
		self.place_signal(3, 3, "GREEN")
		self.place_track(2, 3)
		self.place_junction(1, 3, "DOWN")
		self.place_track(1, 4)
		self.place_signal(1, 5, "RED")
		self.place_track(1, 6)
		self.place_track(1, 7)
		self.place_track(2, 7)
		self.place_signal(3, 7, "GREEN")
		self.place_track(4, 7)

		self.place_track(9, 6)
		self.place_signal(9, 7, "RED")
		self.place_track(9, 8)

		self.place_endpoint(8, 8)

		print("Preset map loaded to system !!!\n")

	def map_bfs(self):
		"""Find the shortest path between beginning and ending on the track using grid Breadth First Search"""
		q_start = [self.__begin, []]
		q = Queue()
		q.put(q_start)
		self.__visited[self.__begin[0]][self.__begin[1]] == True
		while q.qsize() != 0:
			q_obj = q.get()
			node = q_obj[0]
			path = q_obj[1]
			if node == self.__end:
				return True, path
			possible_moves = self.get_travel_coords(node[0], node[1])
			move_up = self.add_coords(node, Constants.DIRECTION["UP"])
			move_down = self.add_coords(node, Constants.DIRECTION["DOWN"])
			move_left = self.add_coords(node, Constants.DIRECTION["LEFT"])
			move_right = self.add_coords(node, Constants.DIRECTION["RIGHT"])

			'''
			junct_dir = self.__map[node[0]][node[1]].get_direction()
			junct_coords = self.add_coords(node, Constants.DIRECTION[junct_dir])
			if junct_coords not in possible_moves:
			'''

			if move_up in possible_moves and self.__visited[move_up[0]][move_up[1]] == False:
				path_up = path + ["UP"]
				q.put([move_up, path_up])
				self.__visited[move_up[0]][move_up[1]] == True
			if move_down in possible_moves and self.__visited[move_down[0]][move_down[1]] == False:
				path_down = path + ["DOWN"]
				q.put([move_down, path_down])
				self.__visited[move_down[0]][move_down[1]] == True
			if move_left in possible_moves and self.__visited[move_left[0]][move_left[1]] == False:
				path_left = path + ["LEFT"]
				q.put([move_left, path_left])
				self.__visited[move_left[0]][move_left[1]] == True
			if move_right in possible_moves and self.__visited[move_right[0]][move_right[1]] == False:
				path_right = path + ["RIGHT"]
				q.put([move_right, path_right])
				self.__visited[move_right[0]][move_right[1]] == True
		return False, []

'''
if __name__ == '__main__':
	sm = SystemMap(10)
	sm.preset_map()
	result, path = sm.map_bfs()
	print(result)
	print(path)
'''
