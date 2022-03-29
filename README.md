# ecobee-case-study-2022

### Job Information
Company: ecobee
Position: Embedded Developer, Test Fixtures
Case Study: Train Signaling System

### Contact Information
Submitted By: Kyle Thomson
Email: kyle.b.thomson@gmail.com
Cell: 613-301-2339

Embedded Case Study - Train Signaling System
==============================================

## Project Description

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


Table Of Contents
===================


How To Install and Run
========================


Instructions For Use
======================
