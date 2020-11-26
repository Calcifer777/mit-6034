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
import pdb

logger = logging.getLogger()


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
    queue = [ [start] ]
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
        logging.info("Queue: [%s]" % ", ".join((str(n) for n in queue)))
        head_path = queue.pop(0)
        logging.info("Tail node: [%s]" % head_path[-1])
        connected_nodes = graph.get_connected_nodes(head_path[-1])
        logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
        sorted_connected_nodes = hill_sort(connected_nodes)
        logging.info("Sorted Connected nodes: [%s]" % ", ".join(sorted_connected_nodes))
        new_paths = [head_path + [node] for node in
                     sorted_connected_nodes if node not in head_path]
        queue = new_paths + queue
        step += 1
    logging.info("Path found: %s" % str(queue[0]))
    return queue[0]  # WHY???

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):

    def heu_sort(path1, path2):
        h1 = graph.get_heuristic(path1[-1], goal)
        h2 = graph.get_heuristic(path2[-1], goal)
        return h1 - h2

    queue = { 0: [start] }
    step = -1
    logging.info("BEAM SEARCH START: %s" % start)
    logging.info("BEAM SEARCH GOAL: %s" % goal)
    logging.info("BEAM SEARCH WIDTH: %s" % beam_width)
    while all([ path[-1] != goal for path in queue[step+1] ]):
        step += 1
        logging.info("Step: %s" % step)
        paths_at_level = queue[step]
        if len(paths_at_level) == 0:
            return []
        next_step_paths = []
        # Look for paths of length step + 1
        while len(paths_at_level) > 0:
            logging.info("Queue: [%s]" % str(paths_at_level))
            head_path = paths_at_level.pop(0)
            logging.info("Tail node: [%s]" % head_path[-1])
            connected_nodes = graph.get_connected_nodes(head_path[-1])
            logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
            new_paths = [head_path + node for node in
                 connected_nodes if node not in head_path]
            next_step_paths.extend(new_paths)
        # Sort the best `beam_width` paths
        sorted_paths = sorted(next_step_paths, heu_sort)
        logging.info("Sorted step %s paths: %s" % (str(step), str(sorted_paths)))
        queue[step+1] = sorted_paths[:beam_width]
    logging.info("Path found: %s" % str(queue[step+1][0]))
    return list(queue[step+1][0])

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    def loop(graph, node_names, length):
        if len(node_names) <= 1:
            return 0
        else:
            edge_length = graph.get_edge(node_names[0], node_names[1]).length
            if len(node_names) == 2:
                return length + edge_length
            else:
                return loop(graph, node_names[1:], length+edge_length)
    return loop(graph, node_names, 0)


def branch_and_bound(graph, start, goal):
    logger.setLevel(logging.ERROR)
    queue = [ [start] ]
    step = 0
    logging.info("BB START: %s" % start)
    logging.info("BB GOAL: %s" % goal)
    
    def bb_sort(path1, path2):
        l1 = path_length(graph, path1)
        l2 = path_length(graph, path2)
        h1 = graph.get_heuristic(path1[-1], goal) if path1[-1] != goal else 0
        h2 = graph.get_heuristic(path2[-1], goal) if path2[-1] != goal else 0
        # logging.info("Distance %s %s: %s + %s = %s" % (path1[-1], goal, l1, h1, l1+h1))
        # logging.info("Distance %s %s: %s + %s = %s" % (path2[-1], goal, l2, h2, l2+h2))
        return l1+h1 - l2+h2

    while len(queue) > 0 and queue[0][-1] != goal:
        logging.info("Step: %s" % step)
        logging.info("Queue: [%s]" % ", ".join((str(n) for n in queue)))
        head_path = queue.pop(0)
        logging.info("Tail node: [%s]" % head_path[-1])
        connected_nodes = graph.get_connected_nodes(head_path[-1])
        logging.info("Connected nodes: [%s]" % ", ".join(connected_nodes))
        new_paths = [head_path + [node] for node in connected_nodes if node not in head_path]
        queue.extend(new_paths)
        queue.sort(bb_sort)
        # queue = sorted(queue, bb_sort)
        for path in queue:
            logging.info(
                "P: %s, L: %s, H: %s, D: %s" % (
                    str(path), 
                    path_length(graph, path),
                    graph.get_heuristic(path[-1], goal) if path[-1] != goal else 0,
                    path_length(graph, path) + \
                        (graph.get_heuristic(path[-1], goal) if path[-1] != goal else 0)
                )
            )
        step += 1
    logging.info("Path found: %s" % str(queue[0]))
    return queue[0]  # WHY???

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

HOW_MANY_HOURS_THIS_PSET_TOOK = 'Too many'
WHAT_I_FOUND_INTERESTING = 'WHAT'
WHAT_I_FOUND_BORING = 'WHAT'
