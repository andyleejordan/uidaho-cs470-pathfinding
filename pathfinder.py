#!/usr/bin/env python3

import argparse
import sys

from collections import OrderedDict

class Input(object):
    """ Class object to parse input."""
    def __init__(self, filename='map.txt'):
        self._filename = filename
        self._size = ()
        self._start = ()
        self._goal = ()
        self._map = ()
        self._costs = dict(zip(['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False]))

    def filename(self): return self._filename
    def width(self): return self._size[0]
    def height(self): return self._size[1]
    def start(self): return self._start
    def goal(self): return self._goal
    def map_(self): return self._map
    def costs(self): return self._costs

    def _read_map(self, contents):
        """ Makes a tuple of tuple map from contents."""
        input_map = []
        for i in range(0, self.height()):
            input_map.append(tuple(list(contents[i])[:self.width()]))
        return tuple(input_map)

    def _read_contents(self):
        """ Opens map file and grabs size, start, goal, and map."""
        with open(self.filename(), 'r') as f:
            contents = f.readlines()

        self._size = tuple([int(i) for i in contents[0].split()])
        self._start = tuple([int(i) for i in contents[1].split()])
        self._goal = tuple([int(i) for i in contents[2].split()])
        self._map = self._read_map(contents[3:])

class Pathfinder(Input):
    """ Class object to find path using assorted search methods."""
    def __init__(self, options, name=None):
        super().__init__(options.input_map)
        super()._read_contents()

        self._options = options
        self._name = name
        self._fringe = []
        self._explored = set()
        self._parent = {}
        self._path = []

    def options(self): return self._options
    def name(self): return self._name
    def fringe(self): return self._fringe
    def explored(self): return self._explored
    def path(self): return self._path
    def count(self): return len(self._explored)

    def finish(self):
        """ Prints maps and resets lists."""
        self._print_explored()
        self._print_path()

    def _backtrace(self):
        """ Calculates the found path from start to goal."""
        path = [self.goal()]
        while path[-1] != self.start():
            path.append(self._parent[path[-1]])
        path.reverse()
        return tuple(path)

    def _is_valid(self, node):
        """ Test if node is valid: i.e. real, on map, not explored, not in
        fringe, and not impassable water."""
        x, y = node
        if (x < self.width() and y < self.height() and
                x >= 0 and y >= 0 and node not in self.explored()
                and node not in self.fringe()
                and self._node_cost(node)):
            return True
        else:
            return False

    def _expand(self, node):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = node[0], node[1]
        expanded = ((x, y+1), (x+1, y), (x, y-1), (x-1, y))
        for node in expanded:
            if self._is_valid(node):
                result.append(node)
        return result

    def _node_cost(self, node):
        """ Returns the cost of a node."""
        x, y = node[0], node[1]
        return self.costs()[self.map_()[y][x]]

    def _sorted_expand(self, node):
        """ Returns expanded nodes in order from low to high cost."""
        expanded = self._expand(node) # Get adjacent nodes
        costs = {i: self._node_cost(i) for i in expanded} # Add costs
        ordered = OrderedDict(sorted(costs.items(), key=lambda x: x[1]))
        return tuple(ordered.keys()) # Return nodes as tuple

    def _safe_filename(self, suffix):
        """ Appends name to suffix with underscore if name is set."""
        if self.name():
            return '_'.join((self.name(), suffix))
        else:
            return suffix

    def _print_explored(self):
        """ Prints an ASCII map of explored nodes."""
        filename = self._safe_filename(self.options().explored)
        with open(filename, 'w') as f:
            for y in range(0, self.height()):
                for x in range(0, self.width()):
                    if (x, y) == self.start():
                        f.write('@')
                    elif (x, y) == self.goal():
                        f.write('$')
                    elif (x, y) in self.path():
                        f.write('*')
                    elif (x, y) in self.explored():
                        f.write('#')
                    else:
                        f.write(self.map_()[y][x])
                f.write('\n')

    def _print_path(self):
        """ Prints an ASCII map of the found path from start to goal."""
        filename = self._safe_filename(self.options().path)
        with open(filename, 'w') as f:
            for y in range(0, self.height()):
                for x in range(0, self.width()):
                    if (x, y) == self.start():
                        f.write('@')
                    elif (x, y) == self.goal():
                        f.write('$')
                    elif (x, y) in self.path():
                        f.write('*')
                    else:
                        f.write(self.map_()[y][x])
                f.write('\n')

    def breadth_first(self):
        """ Utilizes the breadth first search method to find the path."""
        self._fringe.append(self.start())  # Start the search
        while self.fringe():
            node = self._fringe.pop(0)   # Pop from front: queue
            self._explored.add(node)
            if node == self.goal():      # Found goal
                self._path = self._backtrace()     # Find path
                return True
            for adjacent in self._expand(node):
                self._explored.add(adjacent)    # Save explored nodes
                x, y = adjacent
                self._parent[adjacent] = node
                self._fringe.append(adjacent)
        return False

    def lowest_cost(self):
        """ Utilizes the breadth first search method coupled with sorted insert."""
        self._fringe.append(self.start())  # Start the search
        while self.fringe():
            node = self._fringe.pop(0)   # Pop from front: queue
            self._explored.add(node)
            if node == self.goal():      # Found goal
                self._path = self._backtrace()     # Find path
                return True
            for adjacent in self._sorted_expand(node):
                self._explored.add(adjacent)    # Save explored nodes
                x, y = adjacent
                self._parent[adjacent] = node
                self._fringe.append(adjacent)
        return False

    def iterative_deepening(self):
        """ Repeatedly applies depth-limited search with an increasing limit."""
        return False

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
    options = parser().parse_args()
    # Create Search object from Map

    # Execute search and print results
    searches = (
        Pathfinder(options, 'breadth_first'),
        Pathfinder(options, 'lowest_cost'),
        Pathfinder(options, 'iterative_deepening'),
        Pathfinder(options, 'a_star_1'),
        Pathfinder(options, 'a_star_2'))

    success_string = "{} method found path from ({}, {}) to ({}, {}),"
    success_string += " exploring {} nodes."
    fail_string = "{} method failed to find path."

    for search in searches:
        try:
            result = getattr(search, search.name())()
        except AttributeError as e:
            print("Could not find method '{}'".format(search.name()))
        else:
            if result:
                print(success_string.format(
                    search.name(), search.start()[0], search.start()[1],
                    search.goal()[0], search.goal()[1], search.count()))
                search.finish()
            else:
                print(fail_string.format(search.name()))

if __name__ == "__main__":
   sys.exit(main())
