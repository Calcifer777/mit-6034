# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    """
    Args:
        graph (Graph)
        start (str)
        goal (str)
    """
    queue = [start]
    step = 0
    logging.info("BFS START: %s" % start)
    logging.info("BFS GOAL: %s" % goal)
    while len(queue) > 0 and queue[0][-1] != goal:
        logging.info("BFS step: %s" % step)
        logging.info("Queue: [%s]" % ", ".join(queue))
        head_path = queue.pop(0)
        logging.info("Tail node: [%s]" % head_path[-1])
        connected_nodes = graph.get_connected_nodes(head_path[-1])
        logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
        new_paths = [head_path + node for node in
                     connected_nodes if node not in head_path]
        # queue += new_paths
        queue.extend(new_paths)
        step += 1
    logging.info("Path found: %s" % queue[0])
    return queue[0]

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    queue = [start]
    step = 0
    logging.info("\n\n\nDFS START: %s" % start)
    logging.info("DFS GOAL: %s" % goal)
    while len(queue) > 0 and queue[0][-1] != goal:
        logging.info("DFS step: %s" % step)
        logging.info("Queue: [%s]" % ", ".join(queue))
        head_path = queue.pop(0)
        logging.info("Current path: %s" % head_path)
        logging.info("Tail node: [%s]" % head_path[-1])
        connected_nodes = graph.get_connected_nodes(head_path[-1])
        logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
        new_paths = [head_path + node for node in
                     connected_nodes if node not in head_path]
        queue = new_paths + queue
        step += 1
    logging.info("Path found: %s" % queue[0])
    return queue[0]


## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    queue = [start]
    step = 0
    logging.info("Hill Climbing START: %s" % start)
    logging.info("Hill Climbing GOAL: %s" % goal)
    
    def hill_sort(nodes):
        if len(nodes) <= 1:
            return nodes
        n0 = nodes[0]
        h0 = graph.get_heuristic(n0, goal)
        closer = [n for n in nodes[1:] if graph.get_heuristic(n, goal) <= h0]
        further = [n for n in nodes[1:] if graph.get_heuristic(n, goal) > h0]
        return hill_sort(closer) + [n0] + hill_sort(further)

    while len(queue) > 0 and queue[0][-1] != goal:
        logging.info("Step: %s" % step)
        logging.info("Queue: [%s]" % ", ".join(queue))
        head_path = queue.pop(0)
        logging.info("Tail node: [%s]" % head_path[-1])
        connected_nodes = graph.get_connected_nodes(head_path[-1])
        logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
        sorted_connected_nodes = hill_sort(connected_nodes)
        logging.info("Sorted Connected nodes: [%s]" % ", ".join(sorted_connected_nodes))
        new_paths = [head_path + node for node in
                     sorted_connected_nodes if node not in head_path]
        queue = new_paths + queue
        step += 1
    logging.info("Path found: %s" % queue[0])
    return [n for n in queue[0]]  # WHY???

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    raise NotImplementedError

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    raise NotImplementedError


def branch_and_bound(graph, start, goal):
    raise NotImplementedError

def a_star(graph, start, goal):
    raise NotImplementedError


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
