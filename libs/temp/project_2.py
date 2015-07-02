#!/usr/bin env python

"""
Implementation of project 2, including
breadth-first search, compute connected components and compute resilience
"""

from collections import deque
from random import choice


def bfs_visited(ugraph, start_node):
    """
    Input:
        an undirected graph;
        the start node.
    Output:
        a set consisting of all nodes that are visited by BFS
        that starts at start_node.
    """
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)

    while len(queue) != 0:
        node_j = queue.popleft()
        for neighbor in ugraph[node_j]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited


def cc_visited(ugraph):
    """
    Input:
        an undirected graph
    Output:
        the connected components represented as [{CC0}, {CC1}, ...]
    """
    nodes = [node for node in ugraph.keys()]
    components = []

    while len(nodes) != 0:
        start_node = choice(nodes)
        visited = bfs_visited(ugraph, start_node)
        components.append(visited)
        for cc_node in visited:
            nodes.remove(cc_node)

    return components


def largest_cc_size(ugraph):
    """
    Input:
        an undirected graph
    Output:
        the size of the largest connected coponents in ugraph
    """
    components = cc_visited(ugraph)
    max_size = 0

    for size in components:
        if max_size < len(size):
            max_size = len(size)

    return max_size


def compute_resilience(ugraph, attack_order):
    """
    Input:
        an undirected graph
        a list of nodes attack_order
    Output:
        a list of connected components
    """
    components = []
    components.append(largest_cc_size(ugraph))
    for node in attack_order:
        if node in ugraph.keys():
            for edge in ugraph[node]:
                ugraph[edge].remove(node)
            ugraph.pop(node)
            components.append(largest_cc_size(ugraph))

    return components
