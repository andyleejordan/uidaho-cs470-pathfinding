uidaho-cs470-pathfinding
========================

Repo for University of Idaho's CS470 Artificial Intelligence, Project #1: Pathfinding

Original Assignment
-------------------

Pathfinding is a search problem commonly encountered in computer strategy games. The goal in pathfinding is to find the least cost path between two points on a map. The map is divided into a discrete cells, usually squares or hexagons. Typically there is cost associated with moving into a cell, which depends on the terrain in a cell. E.g. moving into a forest square costs more than moving into a field. (You might consider why the cost is associated with moving into, rather than out of, a cell.)

In games pathfinding is typically an informed search; the agent knows approximately where the goal is and can calculate heuristics like the straight line distance from any point to the goal. In games the pathfinding environment is usually treated as fully observable. If parts of the map are unknown the agent may only plan a route to the edge of the observed region. If there are hidden obstacles, the agent typically picks a route ignoring them and must replan after finding them. (In some cases computer agents may be allowed to 'cheat' and observe more of the map than a human player would be allowed to.)

Although games are the most obvious application of pathfinding there are many other problems that require pathfinding. For example, determining the flow of water or oil between underground pools may require pathfinding with different types of soil and rock impeding the flow to a greater or lessor extent.

### Project: ###
Test a number of different search strategies for pathfinding.

#### Algorithms ####
You will need to test the following algorithms:

* Breadth first.
* Lowest cost.
* Iterative deeping by cost with and without avoiding repeated states.
* A\* with at least two different heuristics.

#### Experiments ####
For each algorithm you will need to do the following:

* Show that the algorithm works. In particular you should show, with an actual figure, both the cells explored by the algorithm and the route that the algorithm finds. Make sure that the figure clearly shows that the algorithm works. For example, if there is a mountain range that impedes movement show that the algorithm searches for paths around it.
* Try different map sizes (or different distances from start cell to goal cell) and measure either the time required to find a solution, the number of cells explored, or both for each algorithm. Plot the results.
* Try different map sizes (or different distances from start cell to goal cell) and measure either the time required to find a solution, the number of cells explored, or both for each algorithm. Plot the results.
* Other Requirements: For this problem the map will use a rectangular grid. Agents will be able to move in four directions (up, down, left, right), but not diagonally.

Your program should be able to read a map file in the following format.

* Width Height
* StartX StartY
* GoalX GoalY
* map

Where the map is an array of characters. Width and Height define the width and height of the map. StartX, StartY, GoalX, and GoalY define the start and goal locations respectively. Note as a C++ programmer I have defined these positions starting from 0, so 0,0 is in the top left-hand corner of the map. Here is a sample map file. The characters are interpreted as follows:

    Character   Meaning Movement Cost
    R   road    1
    f   field   2
    F   forest  4
    h   hills   5
    r   river   7
    M   mountains   10
    W   water   can't be entered

After a successful search the program should be capable of the following:

* Draw the path on the map.
* Denote all of the explored squares on the map.
* Report the number of explored squares.

This does not require a graphical output (although that's probably best). You could draw a text version of the map (as in the sample file) and underline explored squares and highlight squares on the successful path.

#### Write-up ####
Write your results as a paper. Plan on 5-10 pages, including figures and graphs. The paper should include the following:

* An abstract summarizing what you did and what the results were.
* An introduction describing the pathfinding problem in general, and your specific version of it (e.g. the movement costs, etc.).
* An algorithms section that explains, in detail, the algorithms you used. Don't just say you used uniform cost search - explain how it works. Remember to explain your A\* heuristics.
* A results section that uses figures and graphs to show that the algorithms work and that presents the graphs comparing the different algorithms' efficiency on different sized problems and results from the supplied maps.
* A conclusion section that discuss the advantages and weaknesses of the algorithms and heuristics you tried. You may also want to discuss variations that were not tried, e.g. how would allowing diagonal movements (possibly at a slightly higher cost) effect the results, what about hexagonal cells?
* When you write this paper assume that you are writing for an uniformed audience - say CS120 or CS121 students. E.g. explain the problem, explain the movement costs, explain how the algorithms work, etc.
