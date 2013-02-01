#!/usr/bin/env python3

import argparse
import sys

class Input(object):
    """ Class that parses input."""
    def __init__(self, filename='map.txt'):
        self.Filename = filename
        self.Width = None
        self.Height = None
        self.StartX = None
        self.StartY = None
        self.GoalX = None
        self.GoalY = None
        self.InputMap = ()
        self.Costs = zip(
                ['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False])

        self._read_contents()

    def _read_map(self, contents):
        """ Makes a tuple of tuple map from contents."""
        input_map = []
        for i in range(0, self.Height):      # size[1] is height
            input_map.append(tuple(list(contents[i])[0:-1]))    # Remove \n
        return tuple(input_map)

    def _read_contents(self):
        """ Opens map file and grabs size, start, goal, and map."""
        with open(self.Filename, 'r') as f:
            contents = f.readlines()

        size = [int(i) for i in contents[0].split()]
        self.Width, self.Height = size[0], size[1]

        start = [int(i) for i in contents[1].split()]
        self.StartX, self.StartY = start[0], start[1]

        goal = [int(i) for i in contents[2].split()]
        self.GoalX, self.GoalY= goal[0], goal[1]

        self.InputMap = self._read_map(contents[3:])

class BreadFirst(object):
    """ Class for bread first search method."""
    def __init__(self, InputMap):
        self.Map = InputMap.InputMap
        self.Size = (InputMap.Width, InputMap.Height)
        self.Start = (InputMap.StartX, InputMap.StartY)
        self.Goal = (InputMap.GoalX, InputMap.GoalY)
        self.Fringe = []
        self.Explored = set()
        self.Path = []

    def _backtrace(self, parent):
        """ Calculates the found path from start to goal."""
        path = [self.Goal]
        while path[-1] != self.Start:
            path.append(parent[path[-1]])
        path.reverse()
        return tuple(path)

    def _expand(self, node):
        """ Returns N, E, S, W coordinates as list."""
        x, y = node[0], node[1]
        return ((x, y+1), (x+1, y), (x, y-1), (x-1, y))

    def search(self):
        """ Finds the path from start to goal."""
        # TODO: Check water
        parent = {}     # Keeps track of node to parent
        self.Fringe.append(self.Start)  # Start the search
        while self.Fringe:
            node = self.Fringe.pop(0)   # Pop from front: queue
            if node == self.Goal:       # Found goal
                self.Explored.add(node) # Save explored nodes
                self.Path = self._backtrace(parent)     # Find path
                break
            for adjacent in self._expand(node):
                if (adjacent[0] < self.Size[0] and  # Check if valid
                        adjacent[1] < self.Size[1] and
                        adjacent[0] >= 0 and
                        adjacent[1] >= 0 and
                        adjacent not in self.Explored):
                    self.Explored.add(adjacent)     # Save explored nodes
                    parent[adjacent] = node         # Save path
                    self.Fringe.append(adjacent)    # Add adjacent nodes

def print_path(search):
    print(search.Path)

def parser():
    """ This is the option parser."""
    # TODO: Add type of search option
    parser = argparse.ArgumentParser(description='Find a path.')
    parser.add_argument('--map', dest='input_map', default='map.txt',
            help='Path to input map file.')
    parser.add_argument('--path', default='path.txt',
            help='Path to output map file of found path.')
    parser.add_argument('--explored', default='explored.txt',
            help='Path to output map file of all explored options.')
    return parser

def main():
    # Parse arguments and store in Args
    Args = parser().parse_args()
    # Parse input map and store data in Map
    Map = Input(Args.input_map)
    # Create Search object from Map
    Search = BreadFirst(Map)

    # Execture search and print results
    Search.search()
    print_path(Search)

if __name__ == "__main__":
   sys.exit(main())
