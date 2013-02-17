#!/usr/bin/env python3

import argparse
import sys


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


class Search(Input):
    """ Class object to find path using assorted search methods."""
    def __init__(self, options, name=None):
        super().__init__(options.input_map)
        super()._read_contents()

        self._options = options
        self._name = name

        self._fringe = []
        self._closed = set()
        self._path = {}

    def options(self): return self._options
    def name(self): return self._name
    def count(self): return len(self.closed())
    def path(self): return self._path

    def fringe(self): return self._fringe
    def closed(self): return self._closed
    def goal_test(self, state): return state == self.goal()

    def clear_lists(self):
        self._fringe = []
        self._closed = set()
        self._path = {}

    def add_fringe(self, state, cost=None):
        if cost is not None:
            self._fringe.append((state, cost))
        else:
            self._fringe.append(state)

    def add_closed(self, state):
        self._closed.add(state)

    def remove_closed(self, state):
        try:
            self._closed.remove(state)
        except KeyError:
            pass

    def remove_fringe(self, i):
        self._fringe.pop(self._fringe.index(i))

    def get_next_front(self):
        return self._fringe.pop(0)

    def get_next_end(self):
        return self._fringe.pop()

    def is_not_explored(self, state):
        return (state not in self.fringe() and
                state not in self.closed())

    def record_path(self, parent, child):
        self._path[child] = parent

    def get_path(self):
        path = [self.goal()]
        while path[-1] != self.start():
            path.append(self._path[path[-1]])
        path.reverse()
        return tuple(path)

    def state_cost(self, state):
        x, y = state
        return self.costs()[self.graph()[y][x]]

    def sort_fringe(self, reverse=False, tuple_=False):
        if not tuple_:
            self._fringe.sort(key=lambda state: self.state_cost(state))
        else:
            self._fringe.sort(key=lambda node: node[1])
        if reverse:
            self._fringe.reverse()

    def state_not_in_fringe(self, state):
        for i in self.fringe():
            if state == i[0]:
                return False
        return True

    def fringe_higher(self, state, cost, append=True):
        for i in self._fringe:
            if state == i[0]:
                if i[1] > cost:
                    self.remove_fringe(i)
                    if append:
                        self.add_fringe(state, cost)
                    return True
                if i[1] == cost:
                    return True
                else:
                    return False

    def _is_valid(self, state):
        """ Test if node is valid: i.e. real, on map, not explored, not in fringe, and not impassable water."""
        x, y = state
        if (x >= 0 and
            y >= 0 and
            x < self.width() and
            y < self.height() and
            self.graph()[y][x] != 'W'):
            return True
        else:
            return False

    def expand(self, state):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = state
        neighbors = (
                    (x+1, y),
                    (x-1, y),
                    (x, y-1),
                    (x, y+1))
        for neighbor in neighbors:
            if self._is_valid(neighbor):
                result.append(neighbor)
        return result

    def breadth_first(self):
        self.add_fringe(self.start())
        while self.fringe():
            parent = self.get_next_front()
            if self.goal_test(parent):
                return parent
            for child in self.expand(parent):
                if self.is_not_explored(child):
                    self.record_path(parent, child)
                    self.add_fringe(child)
            self.add_closed(parent)
        return None

    def uniform_cost(self):
        self.add_fringe(self.start(), 0)
        while self.fringe():
            parent, path_cost = self.get_next_front()
            if self.goal_test(parent):
                return parent
            self.add_closed(parent)
            for child in self.expand(parent):
                child_path_cost = path_cost + self.state_cost(child)
                if child not in self.closed():
                    if self.state_not_in_fringe(child):
                        self.record_path(parent, child)
                        self.add_fringe(child, child_path_cost)
                    elif self.fringe_higher(child, child_path_cost):
                        self.record_path(parent, child)
                        self.remove_closed(child)
            self.sort_fringe(tuple_=True)
        return None

    def depth_first(self):
        self.add_fringe(self.start())
        while self.fringe():
            parent = self.get_next_end()
            if self.goal_test(parent):
                return parent
            self.add_closed(parent)
            for child in self.expand(parent):
                if self.is_not_explored(child):
                    self.record_path(parent, child)
                    self.add_fringe(child)
        return None


    def depth_limited(self, limit=5000):
        self.add_fringe(self.start(), 0)
        while self.fringe():
            parent, depth = self.get_next_end()
            if depth >= limit:
                continue # HOLY FUCKING SHIT THIS IS IMPORTANT
            if self.goal_test(parent):
                return parent
            self.add_closed(parent)
            for child in self.expand(parent):
                if child not in self.closed():
                    if self.state_not_in_fringe(child):
                        self.record_path(parent, child)
                        self.add_fringe(child, depth+1)
                if not self.state_not_in_fringe(child):
                    if self.fringe_higher(child, depth+1):
                        self.record_path(parent, child)
                        self.remove_closed(child)
        return None

    def iterative_deepening_depth_limited(self):
        for limit in range(0, sys.maxsize):
            self.clear_lists()
            result = self.depth_limited(limit)
            if result is not None:
                print("IDDL reached depth: {}".format(limit))
                return result

    def depth_limited_recursive(self, limit=5000):
        def depth_first_visit(parent, depth, limit):
            if depth >= limit:
                return 'cutoff'
            self.add_fringe(parent, depth)
            if self.goal_test(parent):
                return parent
            cutoff = False
            for child in self.expand(parent):
                if (self.state_not_in_fringe(child) or
                        self.fringe_higher(child, depth+1, append=False)):
                    result = depth_first_visit(child, depth+1, limit)
                    self.record_path(parent, child)
                    if result == 'cutoff':
                        cutoff = True
                    if result is not None:
                        return result
            self.remove_fringe((parent, depth))
            if cutoff:
                return 'cutoff'
            return None

        return depth_first_visit(self.start(), 0, limit)

    def iterative_deepening_depth_limited_recursive(self):
        for limit in range(0, sys.maxsize):
            self.clear_lists()
            result = self.depth_limited_recursive(limit)
            if result != 'cutoff':
                print("IDDL reached depth: {}".format(limit))
                return result

    def depth_first_cost_limited(self, limit=5000):
        self.add_fringe(self.start(), 0)
        while self.fringe():
            parent, path_cost = self.get_next_end()
            if path_cost >= limit:
                continue # HOLY FUCKING SHIT THIS IS IMPORTANT
            if self.goal_test(parent):
                return parent
            self.add_closed(parent)
            for child in self.expand(parent):
                child_path_cost = path_cost + self.state_cost(child)
                if child not in self.closed():
                    if self.state_not_in_fringe(child):
                        self.record_path(parent, child)
                        self.add_fringe(child, child_path_cost)
                if not self.state_not_in_fringe(child):
                    if self.fringe_higher(child, child_path_cost):
                        self.record_path(parent, child)
                        self.remove_closed(child)
        return None

    def iterative_deepening_cost_limited(self):
        for limit in range(0, sys.maxsize):
            self.clear_lists()
            result = self.depth_first_cost_limited(limit)
            if result is not None:
                print("IDCL reached cost: {}".format(limit))
                return result

    def depth_first_recursive(self):
        gray = set()

        def depth_first_visit(parent):
            if self.goal_test(parent):
                return parent
            gray.add(parent)
            found = False
            for child in self.expand(parent):
                if child not in gray and child not in self.closed():
                    self.record_path(parent, child)
                    result = depth_first_visit(child)
                    if result is not None:
                        found = True
            gray.remove(parent)
            self.add_closed(parent)
            if found:
                return result
            return None

        for x in range(0, self.width()):
            for y in range(0, self.height()):
                state = x, y
                if state not in gray and state not in self.closed():
                    result = depth_first_visit(state)
                    if result is not None:
                        return result
        return None



    def finish(self):
        """ Prints maps and resets lists."""
        self._print_explored()
        self._print_path()

    def _safe_filename(self, suffix):
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
                    elif (x, y) in self.closed():
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
        Search(options, 'breadth_first'),
        Search(options, 'uniform_cost'),
        Search(options, 'depth_first'),
        Search(options, 'depth_first_depth_limited'),
        Search(options, 'iterative_deepening_depth_limited'),
        Search(options, 'depth_first_cost_limited'),
        Search(options, 'iterative_deepening_cost_limited'),
        Search(options, 'depth_first_recursive'),
        #Search(options, 'a_star_1'),
        #Search(options, 'a_star_2')
        )

    success_string = "{} method found path from ({}, {}) to ({}, {}),"
    success_string += " exploring {} nodes."
    fail_string = "{} method failed to find path."

    for search in searches:
        try:
            result = getattr(search, search.name())()
        except AttributeError:
            print("Could not find method '{}'".format(search.name()))
        else:
            if result is not None:
                search._path = search.get_path()
                print(success_string.format(
                    search.name(), search.start()[0], search.start()[1],
                    search.goal()[0], search.goal()[1], search.count()))
                search.finish()
            else:
                print(fail_string.format(search.name()))

if __name__ == "__main__":
   sys.exit(main())








