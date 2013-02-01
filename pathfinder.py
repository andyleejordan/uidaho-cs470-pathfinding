#!/usr/bin/env python3

import argparse
import sys

class Input(object):
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
        input_map = []
        for i in range(0, self.Height):      # size[1] is height
            input_map.append(tuple(list(contents[i])[0:-1]))    # Remove \n
        return tuple(input_map)

    def _read_contents(self):
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
    def __init__(self, InputMap):
        self.Map = InputMap.InputMap
        self.Size = (InputMap.Width, InputMap.Height)
        self.Start = (InputMap.StartX, InputMap.StartY)
        self.Goal = (InputMap.GoalX, InputMap.GoalY)
        self.Fringe = []
        self.Explored = set()
        self.Path = []

        self._search()

    def _expand(self, node):
        """ Returns N, E, S, W coordinates as list."""
        x, y = node[0], node[1]
        return ((x, y+1), (x+1, y), (x, y-1), (x-1, y))

    def _search(self):
        self.Fringe.append(self.Start)
        while self.Fringe:
            node = self.Fringe.pop(0)
            if node == self.Goal:
                self.Explored.add(node)
                return self.Explored
            for adjacent in self._expand(node):
                if (adjacent[0] < self.Size[0] and
                        adjacent[1] < self.Size[1] and
                        adjacent[0] >= 0 and
                        adjacent[1] >= 0 and
                        adjacent not in self.Explored):
                    self.Explored.add(adjacent)
                    self.Fringe.append(adjacent)

def parser():
    parser = argparse.ArgumentParser(description='Find a path.')
    parser.add_argument('--map', dest='input_map', default='map.txt',
            help='Path to input map file.')
    parser.add_argument('--path', default='path.txt',
            help='Path to output map file of found path.')
    parser.add_argument('--explored', default='explored.txt',
            help='Path to output map file of all explored options.')
    return parser

def main():
    # Parse arguments and store in args
    Args = parser().parse_args()

    Map = Input(Args.input_map)
    Search = BreadFirst(Map)

if __name__ == "__main__":
   sys.exit(main())
