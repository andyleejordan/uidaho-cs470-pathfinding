#!/net/special/cs121_tools/python_env/bin/python
#!/usr/bin/env python2
# Use the appropriate interpretter path for your system. The first one works on Wormulon, the second one is standard on most Ubuntu installations.

import argparse
from subprocess import check_output
from random import randint

def gen_map(args):
    maze = [[None for _ in range(args.width)] for _ in range(args.height)]

    cdf = 0
    cdf_road = args.road
    cdf_field = cdf_road + args.field
    cdf_forest = cdf_field + args.forest
    cdf_hills = cdf_forest + args.hills
    cdf_river = cdf_hills + args.river
    cdf_mountains = cdf_river + args.mountains
    cdf_water = cdf_mountains + args.water
    cdf = cdf_water

    for w_dex in range(0, args.width):
        for h_dex in range(0, args.height):
            my_rand = randint(0, cdf - 1)
            if my_rand < cdf_road:
                terrain = 'R'
            elif my_rand < cdf_field:
                terrain = 'f'
            elif my_rand < cdf_forest:
                terrain = 'F'
            elif my_rand < cdf_hills:
                terrain = 'h'
            elif my_rand < cdf_river:
                terrain = 'r'
            elif my_rand < cdf_mountains:
                terrain = 'M'
            elif my_rand < cdf_water:
                terrain = 'W'
            else:
                raise Exception("cdf error")

            maze[h_dex][w_dex] = terrain

    with open(args.output, 'w') as outfile:
        print >> outfile, args.width, args.height
        while True:
            start_x, start_y = randint(0, args.width - 1), randint(0, args.height - 1)
            if maze[start_y][start_x] != 'W':
                break
        print >> outfile, start_x, start_y
        while True:
            goal_x, goal_y = randint(0, args.width - 1), randint(0, args.height - 1)
            if maze[goal_y][goal_x] != 'W' and (start_x != goal_x or start_y != goal_y):
                break
        print >> outfile, goal_x, goal_y
        for row in maze:
            print >> outfile, ''.join(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("CS 570 -- Project one -- maze generator\n"
                                                  "Author -- Logan Evans"))
    parser.add_argument("-o", "--output", type=str, default="new_maze.txt",
                        help="The output maze filename.")
    parser.add_argument("-B", "--width", type=int, default=0,
                        help="The maze width.")
    parser.add_argument("-H", "--height", type=int, default=0,
                        help="The maze height.")
    parser.add_argument("-R", "--road", type=int, default=1, help="Road weight")
    parser.add_argument("-f", "--field", type=int, default=1, help="Field weight")
    parser.add_argument("-F", "--forest", type=int, default=1, help="Forest weight")
    parser.add_argument("-l", "--hills", type=int, default=1, help="Hills weight")
    parser.add_argument("-r", "--river", type=int, default=1, help="River weight")
    parser.add_argument("-M", "--mountains", type=int, default=1, help="Mountains weight")
    parser.add_argument("-W", "--water", type=int, default=1, help="Water weight")

    args = parser.parse_args()

    if not args.width:
        args.width = int(check_output(['tput', 'cols']))
    if not args.height:
        args.height = int(check_output(['tput', 'lines'])) - 1

    gen_map(args)

