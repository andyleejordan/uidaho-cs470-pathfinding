#!/usr/bin/env python3

import argparse
import sys

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

if __name__ == "__main__":
   sys.exit(main())
