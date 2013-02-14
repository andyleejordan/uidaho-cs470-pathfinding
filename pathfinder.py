#!/usr/bin/env python3

import argparse
import operator
import sys

from collections import OrderedDict


class Input(object):
    """ Class object to parse input."""
    def __init__(self, filename='map.txt'):
        self._filename = filename
        self._size = ()
        self._start = ()
        self._goal = ()
        self._graph = ()
        self._costs = dict(zip(['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False]))

    def filename(self): return self._filename
    def width(self): return self._size[0]
    def height(self): return self._size[1]
    def start(self): return self._start
    def goal(self): return self._goal
    def graph(self): return self._graph
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
        self._graph = self._read_map(contents[3:])


class Node(object):
    """ Class object to represent graph node"""
    def __init__(self, state, parent=None, path_cost=0):
        self._depth = 0
        self._state = state
        self._parent = parent
        self._path_cost = path_cost

        if parent:
            self._depth = parent.depth() + 1

    def depth(self): return self._depth
    def state(self): return self._state
    def parent(self): return self._parent
    def path_cost(self): return self._path_cost

    def make_child(self, next_state, move_cost=0):
        """Returns a child node with current_node as parent.
        Needs the next_state, and the new cost for that state)"""
        return Node(next_state, self, move_cost)

    def solution(self):
        return [node.state() for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent()
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state() == other.state()


class Pathfinder(Input):
    """ Class object to find path using assorted search methods."""
    def __init__(self, options, name=None):
        super().__init__(options.input_map)
        super()._read_contents()

        self._options = options
        self._name = name
        self._fringe = []
        self._path = []
        self._explored = set()

    def options(self): return self._options
    def name(self): return self._name
    def fringe(self): return self._fringe
    def path(self): return self._path
    def explored(self): return self._explored
    def count(self): return len(self._explored)
    def add_fringe(self, node): self._fringe.append(node)
    def add_closed(self, node): self._explored.add(node.state())
    def goal_test(self, node): return node.state() == self.goal()

    def path_cost(self, current, child):
        """Returns the new path cost. path_cost(current_node, child_node)"""
        x, y = child.state()
        return current.path_cost() + self.node_cost(child)

    def node_cost(self, node):
        """ Returns the cost of a node."""
        x, y = node.state()[0], node.state()[1]
        return self.costs()[self.graph()[y][x]]

    def sort_fringe(self):
        self._fringe.sort(lambda a, b: cmp(self.node_cost(a), self.node_cost(b)))

    def _is_valid(self, state):
        """ Test if node is valid: i.e. real, on map, not explored, not in
        fringe, and not impassable water."""
        x, y = state
        if (x < self.width() and y < self.height() and
                x >= 0 and y >= 0 and
                self.costs()[self.graph()[y][x]]):
            return True
        else:
            #print("State {}, {} was invalid.".format(x, y))
            return False

    def expand(self, node):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = node.state()[0], node.state()[1]
        actions = (
                ('N', (x, y-1)),
                ('S', (x, y+1)),
                ('E', (x+1, y)),
                ('W', (x-1, y)))
        for action in actions:
            if self._is_valid(action[1]):
                result.append(action[1])
        return result

    # NOTE: Deprecating this as it is BAD
    #def _sorted_expand(self, node, reverse=False):
        #""" Returns expanded nodes in order from low to high cost."""
        #expanded = self._expand(node) # Get adjacent nodes
        #costs = {i: self._node_cost(i) for i in expanded} # Add costs
        #ordered = OrderedDict(sorted(costs.items(), key=lambda x: x[1],
            #reverse=reverse))
        #return tuple(ordered.keys()) # Return nodes as tuple

    def breadth_first(self):
        """Utilizes the breadth first search method to find the path"""
        start_node = Node(self.start())
        self.add_fringe(start_node)
        while self.fringe():
            parent = self._fringe.pop(0)
            print(parent.state())
            if self.goal_test(parent):
                return parent
            for state in self.expand(parent):
                if state not in self.explored():
                    child = parent.make_child(state)
                    self.add_fringe(child)
            self.add_closed(parent)
        return None

    def uniform_cost_search(self):
        """Utilizes the breadth first search method coupled with sorted insert"""
        start_node = Node(self.start())
        self.add_fringe(start_node)
        while self.fringe():
            parent = self._fringe.pop(0)
            if self.goal_test(parent):
                return parent
            for state in self.expand(parent):
                if state not in self.explored():
                    child = parent.child_node(state)
                    self.add_fringe(child)
                    # This makes it a cost search, sort the fringe list
                    self.sort_fringe()
            self.add_closed(parent)
        return None


    def finish(self):
        """ Prints maps and resets lists."""
        self._print_explored()
        self._print_path()

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
                        f.write(self.graph()[y][x])
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
                        f.write(self.graph()[y][x])
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
    options = parser().parse_args()
    # Create Search object from Map

    # Execute search and print results
    searches = (
        Pathfinder(options, 'breadth_first'),
        Pathfinder(options, 'uniform_cost_search'),
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
                search._path = result.solution()
                print(success_string.format(
                    search.name(), search.start()[0], search.start()[1],
                    search.goal()[0], search.goal()[1], search.count()))
                search.finish()
            else:
                print(fail_string.format(search.name()))

if __name__ == "__main__":
   sys.exit(main())
