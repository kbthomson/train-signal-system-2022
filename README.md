# train-signal-system-2022

### Contact Information

Submitted By: Kyle Thomson
Email: kyle.b.thomson@gmail.com

Train Signaling System
==============================================

### Problem Statement

Design a software program to control a simulation of a train traffic and signaling system. The system should include the following components:
- Several track segments, which consist of a length of track (of arbitrary length), plus two connection points at each end.
- Each of the two connection points in a track segment can:
- Link with another track connection point directly, such that the next track segment is a continuation of the first
- Link with another track segment in a junction, providing a fork in the track
- End in a terminator.
- Junctions can direct train traffic only to one of the forked tracks at any given time
- Signals, which control the flow of traffic along track segments. Signals are optionally placed at the ends of each track segment. Signals can have the following states:
- Green – train traffic is allowed through
- Red – train traffic must stop before proceeding to the next track segment
- Trains, which are initially placed in a specific track segment, and given a direction. Trains can either be moving or stopped. Assume trains are one track segment long. Trains stop once they reach a terminator.
- Automatic route planning should be built to ensure trains find optimal routes between their starting point and destination.
- The simulation should automatically set signals in order to avoid collisions.

### Requirements

The system has the following requirements:
- Provide a facility to build the system by adding track segments, connections between track segments, signals, and a train.
- Provide a facility to start the system and run the simulation. The simulation ends when all trains have stopped.

### [Optional]

You may choose to implement one or more of the following optional features:
- Provide a facility to display the complete system once built. The format of this display is left to the implementation and could be as simple as a list of segments and signals, or as elaborate as a graphical display.
- Provide a facility to save the layout of the system to file, and to retrieve a layout from file.
- Implement support for multiple trains running concurrently.
- Implement support for trains longer than one track segment.

How To Install and Run
========================

### 1  Installation

No custom installations or libraries required. All source code compatible with Python3.9 base installation.
Python3.9 is required to run.

### 2  Run

python TrainSignalSystem.py

### 3  Define Map Size

Enter size of the train system map with an integer to create an NxN grid.

### 4  Commands

Use the key commands to build, change, inspect, and run the train signal system.

B - Place [B]eginningPoint object on map grid
    Inputs: x, y

E - Place [E]ndPoint object on map grid
    Inputs: x, y

T - Place [T]rackSegment object on map grid
    Inputs: x, y

S - Place [S]ignal object on map grid
    Inputs: x, y, state ("GREEN, "RED")

J - Place [J]unction object on map grid
    Inputs: x, y, direction ("UP", "DOWN", "LEFT", "RIGHT")

I - [I]nspect map element for more data

X - Remove or [X]-out map element at specific location

P - Load [P]re-set map configuration

D - [D]raw current map configuration to console

V - [V]alidate map configuration before running

C - [C]lear map back to empty configuration

R - [R]un train on map to start simulation

H - [H]elp function to list all available commands

A - [A]bout the author

Q - [Q]uit
