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


class PathProblem(object):
    def __init__(self, input_):
        self._input_ = input_
        self._start = input_.start()
        self._goal = input_.goal()

    def input_(self): return self._input_
    def start(self): return self._start
    def goal(self): return self._goal

    def _is_valid(self, state, avoid=True):
        """ Test if node is valid: i.e. real, on map, not explored, not in
        fringe, and not impassable water."""
        x, y = state
        if avoid:
            print(state not in self.input_().explored())
            if (x < self.input_().width() and y < self.input_().height() and
                    x >= 0 and y >= 0 and
                    self.input_().costs()[self.input_().graph()[y][x]] and
                    state not in self.input_().explored()):
                return True
            else:
                return False
        else:
            if (x < self.input_().width() and y < self.input_().height() and
                    x >= 0 and y >= 0 and
                    self.input_().costs()[self.input_().graph()[y][x]]):
                return True
            else:
                return False

    def actions(self, state, avoid=True):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = state[0], state[1]
        actions = (
                ('N', (x, y-1)),
                ('S', (x, y+1)),
                ('E', (x+1, y)),
                ('W', (x-1, y)))
        for action in actions:
            if self._is_valid(action[1], avoid):
                result.append(action[0])
        return result

    def result(self, state, action):
        if action == 'N':
            return tuple(map(operator.add, state, (0, -1)))
        if action == 'S':
            return tuple(map(operator.add, state, (0, 1)))
        if action == 'E':
            return tuple(map(operator.add, state, (1, 0)))
        if action == 'W':
            return tuple(map(operator.add, state, (-1, 0)))
        print("Could not find action: {}".format(action))

    def goal_test(self, state):
        return state == self.goal()

    def path_cost(self, path_cost, state, action):
        x, y = self.result(state, action)
        return path_cost + self.input_().costs()[self.input_().graph()[y][x]]


class Node(object):
    """ Class object to represent graph node"""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self._depth = 0
        self._state = state
        self._parent = parent
        self._action = action
        self._path_cost = path_cost

        if parent:
            self._depth = parent.depth() + 1

    def depth(self): return self._depth
    def state(self): return self._state
    def parent(self): return self._parent
    def action(self): return self._action
    def path_cost(self): return self._path_cost

    def expand(self, problem, avoid=True):
        return [self.child_node(problem, action) for action in
                problem.actions(self.state(), avoid)]

    def child_node(self, problem, action):
        next_ = problem.result(self.state(), action)
        return Node(
                next_, self, action,
                problem.path_cost(self.path_cost(), self.state(), action))

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

    def _is_valid(self, state):
        """ Test if node is valid: i.e. real, on map, not explored, not in
        fringe, and not impassable water."""
        x, y = state
        if (x < self.width() and y < self.height() and
                x >= 0 and y >= 0 and
                self.costs()[self.graph()[y][x]]):
            return True
        else:
            return False

    def _expand(self, state):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = state[0], state[1]
        expanded = ((x, y+1), (x+1, y), (x, y-1), (x-1, y))
        for state in expanded:
            if self._is_valid(state):
                result.append(state)
        return result

    def _node_cost(self, node):
        """ Returns the cost of a node."""
        x, y = node[0], node[1]
        return self.costs()[self.graph()[y][x]]

    def _sorted_expand(self, node, reverse=False):
        """ Returns expanded nodes in order from low to high cost."""
        expanded = self._expand(node) # Get adjacent nodes
        costs = {i: self._node_cost(i) for i in expanded} # Add costs
        ordered = OrderedDict(sorted(costs.items(), key=lambda x: x[1],
            reverse=reverse))
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

    def breadth_first(self):
        """Utilizes the breadth first search method to find the path"""
        self._fringe.append(self.start())  # Start the search
        while self.fringe():
            node = self._fringe.pop(0)   # Pop from front: queue
            self._explored.add(node)
            if node == self.goal():      # Found goal
                self._path = self._backtrace()     # Find path
                return True
            for adjacent in self._expand(node):
                if (adjacent not in self.explored()
                        and adjacent not in self.fringe()):
                    self._explored.add(adjacent)    # Save explored nodes
                    self._parent[adjacent] = node
                    self._fringe.append(adjacent)
        return False

    def lowest_cost(self):
        """Utilizes the breadth first search method coupled with sorted insert"""
        self._fringe.append(self.start())  # Start the search
        while self.fringe():
            node = self._fringe.pop(0)   # Pop from front: queue
            self._explored.add(node)
            if node == self.goal():      # Found goal
                self._path = self._backtrace()     # Find path
                return True
            for adjacent in self._sorted_expand(node):
                if (adjacent not in self.explored()
                        and adjacent not in self.fringe()):
                    self._explored.add(adjacent)    # Save explored nodes
                    self._parent[adjacent] = node
                    self._fringe.append(adjacent)
        return False

    def _depth_limited_search_by_cost(self, limit):
        """
        Uses stack instead of queue so is depth-first instead of breadth-first
        Uses sorted insert (reversed) for action cost accounting
        Depth limited: checks if depth has reached limit
        Avoids repeated states

        """
        self._fringe.append(self.start())
        depth = 0
        while self.fringe():
            if depth == limit:
                return False
            depth += 1
            node = self._fringe.pop()
            self._explored.add(node)
            if node == self.goal():
                self._path = self._backtrace()
                return True
            for adjacent in self._sorted_expand(node, reverse=True):
                if (adjacent not in self.explored()
                        and adjacent not in self.fringe()):
                    self._explored.add(adjacent)
                    self._parent[adjacent] = node
                    self._fringe.append(adjacent)
        return False

    def _depth_limited_search(self, problem, limit=50):
        def recursive_dls(node, problem, limit):
            if problem.goal_test(node.state()):
                return node
            elif node.depth() == limit:
                return 'cutoff'
            else:
                cutoff_occurred = False
                for child in node.expand(problem, avoid=False):
                    self._explored.add(child.state())
                    result = recursive_dls(child, problem, limit)
                    if result == 'cutoff':
                        cutoff_occurred = True
                    elif result is not None:
                        return result
                if cutoff_occurred:
                    return 'cutoff'
                else:
                    return None

        # Body of depth_limited_search:
        return recursive_dls(Node(problem.start()), problem, limit)

    def iterative_deepening(self):
        """ Repeatedly applies depth-limited search with an increasing limit."""
        problem = PathProblem(self)
        for depth in range(13):
            print(depth)
            result = self._depth_limited_search(problem, depth)
            if result != 'cutoff':
                if result is not None:
                    self._path = result.solution()
                return result
        return False

    def iterative_lengthening(self):
        """ Repeatedly applies depth-limited search with an increasing limit."""
        problem = PathProblem(self)
        for depth in range(13):
            print(depth)
            result = self._depth_limited_search(problem, depth)
            if result != 'cutoff':
                if result is not None:
                    self._path = result.solution()
                return result
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
            raise
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
