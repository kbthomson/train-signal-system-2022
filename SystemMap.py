#!/usr/bin/env python3

"""Class to create and manage the map of the Train Signaling System"""

import os
import sys
import time
import string
import datetime
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

	def add_coords(self, pos1, pos2):
		"""Adds set of (x1, y1) coordinates to (x2, y2) coordinates and returns"""
		new_x = pos1[0] + pos2[0]
		new_y = pos1[1] + pos2[1]
		return [new_x, new_y]

	def check_valid_coords(self, x, y):
		"""Function to check whether (x,y) coordinate on the map are valid"""
		if x < self.__size and x >= Constants.X_BOUNDS and y < self.__size and y >= Constants.Y_BOUNDS:
			return True
		return False

	def get_surrounding_data(self, x, y):
		"""Function to return valid, surrounding coordinates of point (x, y)"""
		coords = list()
		travels = list()
		types = list()

		for k in Constants.DIRECTION.keys():
			direction = Constants.DIRECTION[k]
			pos = self.add_coords([x, y], direction)
			if self.check_valid_coords(pos[0], pos[1]):
				coords.append(pos)
				if self.__map[pos[0]][pos[1]] is not None:
					travels.append(pos)
					types.append(self.__map[pos[0]][pos[1]].get_type())

		return coords, travels, types

	def inspect_object(self, x, y):
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
		self.draw_map()
		print("Map object removed at ({}, {}) - coordinate is now 'None'\n".format(x, y))

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

	def validate_map(self):
		"""Check placement of all objects on map before running"""
		b_count = 0
		e_count = 0
		for i in range(self.__size):
			for j in range(self.__size):

				if self.__map[i][j] is not None:
					coords, travels, types = self.get_surrounding_data(i, j)

					if self.__map[i][j].get_type() == "Junction":
						dir_move = Constants.DIRECTION[self.__map[i][j].get_direction()]
						temp_move = self.add_coords([i, j], dir_move)
						if temp_move not in travels:
							print("Invalid Direction property for TrackObject at ({}, {})".format(i, j))
							print("Map must have object in Direction of movement\n")
							return False
						elif len(types) < 3:
							print("Invalid placement of Junction at ({}, {})".format(i, j))
							print("Junctions must have at least 3 surrounding objects\n")
							return False

					else:
						if self.__map[i][j].get_type() == "Begin":
							b_count += 1
						if self.__map[i][j].get_type() == "End":
							e_count += 1
						if len(types) < 1:
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
		self.place_signal(5, 1, "RED") # Change to RED for Signal example
		self.place_track(5, 2)
		self.place_junction(5, 3, "DOWN")
		self.place_track(5, 4)
		self.place_junction(5, 5, "DOWN") # Change to RIGHT for Junction example
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
		self.place_junction(9, 5, "DOWN")
		self.place_track(8, 5)
		self.place_track(7, 5)
		self.place_track(6, 5)

		self.place_track(1, 2)
		self.place_track(3, 2)
		self.place_signal(3, 3, "GREEN")
		self.place_track(2, 3)
		self.place_junction(1, 3, "DOWN") # Change to UP for Junction example
		self.place_track(1, 4)
		self.place_signal(1, 5, "GREEN") # Change to RED for Signal example
		self.place_track(1, 6)
		self.place_track(1, 7)
		self.place_track(2, 7)
		self.place_signal(3, 7, "GREEN") # Change to RED for Signal example
		self.place_track(4, 7)

		self.place_track(9, 6)
		self.place_signal(9, 7, "GREEN")
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
			
			coords, travels, types = self.get_surrounding_data(node[0], node[1])
			move_up = self.add_coords(node, Constants.DIRECTION["UP"])
			move_down = self.add_coords(node, Constants.DIRECTION["DOWN"])
			move_left = self.add_coords(node, Constants.DIRECTION["LEFT"])
			move_right = self.add_coords(node, Constants.DIRECTION["RIGHT"])

			if self.__map[node[0]][node[1]].get_type() == "Signal":
				if self.__map[node[0]][node[1]].get_state() == "RED":
					path_wait = path + ["SIGNAL-CHANGE-RED-TO-GREEN"]
					q.put([node, path_wait])
					self.__visited[node[0]][node[1]] == True
					self.__map[node[0]][node[1]].set_state("GREEN")
					continue

			elif self.__map[node[0]][node[1]].get_type() == "Junction":
				junct_dir = self.__map[node[0]][node[1]].get_direction()
				junct_coord = self.add_coords(node, Constants.DIRECTION[junct_dir])

				if junct_coord in travels:
					junct_path = path + [junct_dir]
					q.put([junct_coord, junct_path])
					self.__visited[junct_coord[0]][junct_coord[1]] == True
					continue

			if move_up in travels and self.__visited[move_up[0]][move_up[1]] == False:
				path_up = path + ["UP"]
				q.put([move_up, path_up])
				self.__visited[move_up[0]][move_up[1]] == True

			if move_down in travels and self.__visited[move_down[0]][move_down[1]] == False:
				path_down = path + ["DOWN"]
				q.put([move_down, path_down])
				self.__visited[move_down[0]][move_down[1]] == True

			if move_left in travels and self.__visited[move_left[0]][move_left[1]] == False:
				path_left = path + ["LEFT"]
				q.put([move_left, path_left])
				self.__visited[move_left[0]][move_left[1]] == True

			if move_right in travels and self.__visited[move_right[0]][move_right[1]] == False:
				path_right = path + ["RIGHT"]
				q.put([move_right, path_right])
				self.__visited[move_right[0]][move_right[1]] == True

		return False, []

	def drive_train(self, path):
		"""Animate Train object travelling along the found path on the system map in console"""
		print("!!! Train is leaving the station !!!")
		t = Train(self.__begin[0], self.__begin[1], path[0], False)
		self.draw_map(t)
		time.sleep(1)

		for moves in path:
			if moves not in Constants.DIRECTION.keys():
				print("!!! Train stopping to wait for track action !!!")
				print("Action: {}".format(moves))
				t.set_moving(False)
				time.sleep(2)
			else:
				t.set_direction(moves)
				t.set_moving(True)
				t.move()
				time.sleep(1)
			self.draw_map(t)

		print("!!! Train has arrived !!!")
		return True
