# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    from util import Stack

    st=Stack() # a Stack's object
    visited=set() # a set of visited nodes
    path=[] # here save the search path from start node to goal

    node=problem.getStartState()

    st.push((node,path)) # push the node and the path in to the Stack

    while True:
        if st.isEmpty():
            return []

        # when I pop one item from the Stack, I take the node and I add this in to the visited set
        node,path=st.pop()
        visited.add(node)

        if problem.isGoalState(node): # if the goal reached, return the search path
            return path

        childs=problem.getSuccessors(node) # take the successors/childs of the current node/state

        for c in childs: # c[0]:next_state  c[1]:action  c[2]:cost
            if c[0] not in visited: # check if the successor/child is not visited
                new_path=list(path) # copy old path list to a new path list
                new_path.append(c[1]) # add the new route to the new path list
                st.push((c[0],new_path)) # push the node and the path in to the Stack

    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue

    q=Queue() # a Queue's object 
    visited=set() # a set of visited nodes
    path=[] # here save the search path from start node to goal

    node=problem.getStartState()

    q.push((node,path))  # push the node and the path in to the Queue

    while True:
        if q.isEmpty():
            return []

        # when I pop one item from the Queue, I take the node and I add this in to the visited set
        node,path=q.pop()
        visited.add(node)

        if problem.isGoalState(node): # if the goal reached, return the search path
            return path

        childs=problem.getSuccessors(node) # take the successors/childs of the current node/state

        # c[0]:next_state  c[1]:action  c[2]:cost
        for c in childs: # check if the successor/child is non visited and is not in Queue
            if c[0] not in visited and c[0] not in (item[0] for item in q.list):
                new_path=list(path) # copy old path list to a new path list
                new_path.append(c[1]) # add the new route to the new path list
                q.push((c[0],new_path)) # push the node and the path in to the Queue


    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue

    pq=PriorityQueue() # a Priority Queue's object
    visited=set() # a set of visited nodes
    path=[] # here save the search path from start node to goal

    node=problem.getStartState()

    pq.push([node,path],problem.getCostOfActions(path)) # push the node, the path in to the Priority Queue and as priority, set the path cost

    while True:
        if pq.isEmpty():
            return []

        # when I pop one item from the Priority Queue, I take the node and I add this in to the visited set
        node,path=pq.pop()
        visited.add(node)

        if problem.isGoalState(node): # if the goal reached, return the search path
            return path

        childs=problem.getSuccessors(node) # take the successors/childs of the current node/state

        for c in childs: # c[0]:next_state  c[1]:action  c[2]:cost
            if c[0] not in visited and c[0] not in (item[2][0] for item in pq.heap): # check if the successor/child is not visited and is not in Priority Queue
                new_path=list(path)  # copy old path list to a new path list
                new_path.append(c[1]) # add the new route to the new path list
                pq.push([c[0],new_path],problem.getCostOfActions(new_path)) # push the node, the path in to the Priority Queue and as priority, set the path cost
            elif c[0] not in visited and c[0] in (item[2][0] for item in pq.heap): # check if the successor/child is not visited and is in Priority Queue
                new_path=list(path) # copy old path list to a new path list
                new_path.append(c[1]) # add the new route to the new path list
                for item in pq.heap:
                    if item[2][0]==c[0] and item[0]>problem.getCostOfActions(new_path): # check if the successor/child is already in the Priority Queue
                        item[2][1]=new_path                                             # check if the "new_path cost" (priority) is less than the item's cost in the Pr.Queue
                        pq.update([c[0],new_path],problem.getCostOfActions(new_path))   # If True, then update the path and the path cost of this item in Pr.Queue
                                                                                        # (path cost is the priority for the Priority Queue)


    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    pq=PriorityQueue() # a Priority Queue's object
    visited=set() # a set of visited nodes
    path=[] # here save the search path from start node to goal

    node=problem.getStartState()

    fn=problem.getCostOfActions(path)+heuristic(node,problem)  # f(n)= g(n) + h(n)
                                                               # g(n): cost from start node to "n" node
                                                               # h(n): heuristic cost estimation from a node to a goal
    pq.push((node,path),fn) # push the node, the path in to the Priority Queue and as priority, set the value of f(n)

    while True:
        if pq.isEmpty():
            return []

        node,path=pq.pop()

        if node in visited: # if this node is already visited, continue
            continue        # avoid to add multiple times the same node in to the PriorityQueue

        visited.add(node)

        # when I pop one item from the Priority Queue, I take the node and I add this in to the visited set
        if problem.isGoalState(node):
            return path

        childs=problem.getSuccessors(node) # take the successors/childs of the current node/state

        for c in childs:# c[0]:next_state  c[1]:action  c[2]:cost
            if c[0] not in visited:
                new_path=list(path) # copy old path list to a new path list
                new_path.append(c[1]) # add the new route to the new path list
                fn=problem.getCostOfActions(new_path)+heuristic(c[0],problem) # f(n)= g(n) + h(n)
                pq.push((c[0],new_path),fn) # push the node, the path in to the Priority Queue and as priority, set the value of f(n)

    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
