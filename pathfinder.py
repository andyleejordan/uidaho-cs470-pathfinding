#!/usr/bin/env python3

import argparse
import collections
import sys

class InputMap(object):
    def __init__(self, filename='map.txt'):
        self.input_map_file = filename
        self.size = ()
        self.start = ()
        self.goal = ()
        self.input_map = ()
        self.costs = zip(
                ['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False])

    def _read_map(self, contents):
        print(contents)
        edges = collections.defaultdict(list)
        #for i in self.size[1]:      # size[1] is height
            #for j in self.size[0]   # size[0] is width


    def read_contents(self):
        with open(self.input_map_file, 'r') as f:
            contents = f.readlines()

        self.size = tuple(int(i) for i in contents[0].split())
        self.start = tuple(int(i) for i in contents[1].split())
        self.goal = tuple(int(i) for i in contents[2].split())
        self.input_map = self._read_map(contents[3:])

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
    args = parser().parse_args()

    print("Map: {}, path: {}, explored: {}".format(
        args.input_map, args.path, args.explored))

    input_map = InputMap(args.input_map)
    input_map.read_contents()

    print("Size: {}, start: {}, goal: {}".format(
        input_map.size, input_map.start, input_map.goal))
    print(input_map.input_map)

if __name__ == "__main__":
   sys.exit(main())
