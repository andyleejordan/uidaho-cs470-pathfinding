#!/usr/bin/env python3

import argparse
import sys

class Input(object):
    """ Class that parses input."""
    def __init__(self, filename='map.txt'):
        self.Filename = filename
        self.Size = ()
        self.Start = ()
        self.Goal = ()
        self.Map = ()
        self.Costs = zip(
                ['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False])

        self._read_contents()

    def _read_map(self, contents):
        """ Makes a tuple of tuple map from contents."""
        input_map = []
        for i in range(0, self.Size[1]):      # size[1] is height
            input_map.append(tuple(list(contents[i])[:self.Size[0]]))
        return tuple(input_map)

    def _read_contents(self):
        """ Opens map file and grabs size, start, goal, and map."""
        with open(self.Filename, 'r') as f:
            contents = f.readlines()

        self.Size = tuple([int(i) for i in contents[0].split()])
        self.Start = tuple([int(i) for i in contents[1].split()])
        self.Goal = tuple([int(i) for i in contents[2].split()])
        self.Map = self._read_map(contents[3:])

class BreadFirst(Input):
    """ Class for bread first search method."""
    def __init__(self, options):
        super(BreadFirst, self).__init__(options.input_map)
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

    def _is_valid(self, node):
        if (node[0] < self.Size[0] and  # Check if valid
                node[1] < self.Size[1] and
                node[0] >= 0 and
                node[1] >= 0 and
                node not in self.Explored):
            return True
        else:
            return False

    def _expand(self, node):
        """ Returns N, E, S, W coordinates as list."""
        x, y = node[0], node[1]
        return ((x, y), (x, y+1), (x+1, y), (x, y-1), (x-1, y))

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
                if self._is_valid(adjacent):
                    self.Explored.add(adjacent)     # Save explored nodes
                    x, y = adjacent
                    if self.Map[y][x] != 'W':
                        parent[adjacent] = node
                        self.Fringe.append(adjacent)

def print_maps(search, options):
    with open(options.explored, 'w') as f:
        for y in range(0, search.Size[1]):
            for x in range(0, search.Size[0]):
                if (x, y) in search.Explored:
                    f.write('#')
                else:
                    f.write(search.Map[y][x])
            f.write('\n')

    with open(options.path, 'w') as f:
        for y in range(0, search.Size[1]):
            for x in range(0, search.Size[0]):
                if (x, y) is search.Start:
                    f.write('@')
                elif (x, y) is search.Goal:
                    f.write('$')
                elif (x, y) in search.Path:
                    f.write('*')
                else:
                    f.write(search.Map[y][x])
            f.write('\n')

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
    Search = BreadFirst(Options)

    # Execture search and print results
    Search.search()
    print_maps(Search, Options)

if __name__ == "__main__":
   sys.exit(main())
