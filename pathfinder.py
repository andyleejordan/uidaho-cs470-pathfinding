#!/usr/bin/env python3

import argparse
import sys

class Input(object):
    """ Class that parses input."""
    def __init__(self, filename='map.txt'):
        self._Filename = filename
        self._Size = ()
        self._Start = ()
        self._Goal = ()
        self._Map = ()
        self._Costs = zip( ['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False])

    def Width(self): return self._Size[0]
    def Height(self): return self._Size[1]
    def Start(self): return self._Start
    def Goal(self): return self._Goal
    def Map(self): return self._Map
    def Costs(self): return self._Costs

    def _read_map(self, contents):
        """ Makes a tuple of tuple map from contents."""
        input_map = []
        for i in range(0, self.Height()):
            input_map.append(tuple(list(contents[i])[:self.Width()]))
        return tuple(input_map)

    def _read_contents(self):
        """ Opens map file and grabs size, start, goal, and map."""
        with open(self._Filename, 'r') as f:
            contents = f.readlines()

        self._Size = tuple([int(i) for i in contents[0].split()])
        self._Start = tuple([int(i) for i in contents[1].split()])
        self._Goal = tuple([int(i) for i in contents[2].split()])
        self._Map = self._read_map(contents[3:])

class Pathfinder(Input):
    def __init__(self, options):
        super().__init__(options.input_map)
        super()._read_contents()

        self._Options = options
        self._Fringe = []
        self._Explored = set()
        self._Path = []

    def Options(self): return self._Options
    def Fringe(self): return self._Fringe
    def Explored(self): return self._Explored
    def Path(self): return self._Path

    def _backtrace(self, parent):
        """ Calculates the found path from start to goal."""
        path = [self.Goal()]
        while path[-1] != self.Start():
            path.append(parent[path[-1]])
        path.reverse()
        return tuple(path)

    def _is_valid(self, node):
        """ Test if node is valid: i.e. real and on map."""
        x, y = node
        if (x < self.Width() and y < self.Height() and
                x >= 0 and y >= 0 and node not in self.Explored()):
            return True
        else:
            return False

    def _expand(self, node):
        """ Returns N, E, S, W coordinates as list."""
        x, y = node[0], node[1]
        return ((x, y), (x, y+1), (x+1, y), (x, y-1), (x-1, y))

    def print_explored(self):
        with open(self.Options().explored, 'w') as f:
            for y in range(0, self.Height()):
                for x in range(0, self.Width()):
                    if (x, y) == self.Start():
                        f.write('@')
                    elif (x, y) == self.Goal():
                        f.write('$')
                    elif (x, y) in self.Path():
                        f.write('*')
                    elif (x, y) in self.Explored():
                        f.write('#')
                    else:
                        f.write(self.Map()[y][x])
                f.write('\n')

    def print_path(self):
        with open(self.Options().path, 'w') as f:
            for y in range(0, self.Height()):
                for x in range(0, self.Width()):
                    if (x, y) == self.Start():
                        f.write('@')
                    elif (x, y) == self.Goal():
                        f.write('$')
                    elif (x, y) in self.Path():
                        f.write('*')
                    else:
                        f.write(self.Map()[y][x])
                f.write('\n')

    def breadth_first(self):
        """ Finds the path from start to goal."""
        parent = {}     # Keeps track of node to parent
        self._Fringe.append(self.Start())  # Start the search
        while self.Fringe():
            node = self._Fringe.pop(0)   # Pop from front: queue
            if node == self.Goal():      # Found goal
                self._Explored.add(node) # Save explored nodes
                self._Path = self._backtrace(parent)     # Find path
                break
            for adjacent in self._expand(node):
                if self._is_valid(adjacent):
                    self._Explored.add(adjacent)    # Save explored nodes
                    x, y = adjacent
                    if self.Map()[y][x] != 'W':     # Check if impassable water
                        parent[adjacent] = node
                        self._Fringe.append(adjacent)

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
    Options = parser().parse_args()
    # Create Search object from Map
    Search = Pathfinder(Options)

    # Execture search and print results
    Search.breadth_first()
    Search.print_explored()
    Search.print_path()

if __name__ == "__main__":
   sys.exit(main())
