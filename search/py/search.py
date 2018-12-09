#Yemane Berhane
# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
      Returns the start state for the search problem
      """
      util.raiseNotDefined()

    def isGoalState(self, state):
      """
      state: Search state

      Returns True if and only if the state is a valid goal state
      """
      util.raiseNotDefined()

    def getSuccessors(self, state):
      """
      state: Search state

      For a given state, this should return a list of triples,
      (successor, action, stepCost), where 'successor' is a
      successor to the current state, 'action' is the action
      required to get there, and 'stepCost' is the incremental
      cost of expanding to that successor
      """
      util.raiseNotDefined()

    def getCostOfActions(self, actions):
      """
      actions: A list of actions to take

      This method returns the total cost of a particular sequence of actions.  The sequence must
      be composed of legal moves
      """
      util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    openset = problem.getStartState()
    stack.push((openset, list(), list()))
    nex_state = util.Stack()
    actions = util.Stack()
    i = 1


    # print state
    # for i in problem.getSuccessors(state):
    #     print i
    #while not stack.isEmpty():
    while not stack.isEmpty():
      state, actions, closedset = stack.pop()
      if problem.isGoalState(state):
        actions+[action]
        for direction in actions:
          print(direction),
          while i==10:
            print
            i=0
          i+=1
        print
        return actions 
      for nex_state, action, cost in problem.getSuccessors(state):
        if not nex_state in closedset:
          stack.push((nex_state, actions + [action], closedset + [state] ))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    closedset = list()
    openset = problem.getStartState()
    queue.push((openset, list()))
    nex_state = util.Stack()
    actions = util.Stack()
    i = 1
    while not queue.isEmpty():
        state, actions = queue.pop()
        for nex_state, action, cost in problem.getSuccessors(state):
            if not nex_state in closedset:
                closedset.append(nex_state)
                if problem.isGoalState(nex_state):
                  actions+=[action]
                  for direction in actions:
                      print(direction),
                      while i==13:
                        print
                        i=0
                      i+=1
                  print
                  return actions 
                queue.push((nex_state, actions + [action]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    closedset = []
    openset = util.PriorityQueue()
    state = problem.getStartState()
    openset.push((state, list()), 0)
    nextActions = util.PriorityQueue();
    i =1
    while not openset.isEmpty():
        current_state, actions = openset.pop()
        if problem.isGoalState(current_state):
           for direction in nextActions:
              print(direction),
              while i==13:
                print
                i=0
              i+=1
           print
           return actions
        closedset.append(current_state)
        for currState, action, cost in problem.getSuccessors(current_state):
            if not currState in closedset:
                nextActions = actions + [action]
                openset.push((currState, nextActions), problem.getCostOfActions(nextActions))
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    closedset = []
    openset = util.PriorityQueue()
    start = problem.getStartState()
    openset.push((start, list()), heuristic(start, problem))
    i=1

    while not openset.isEmpty():
        state, actions = openset.pop()
        if problem.isGoalState(state):
           for direction in actions:
                print(direction),
                while i==13:
                  print
                  i=0
                i+=1
           print
           return actions
        closedset.append(state)
        for currState, action, cost in problem.getSuccessors(state):
            if not currState in closedset:
                nextActions = actions + [action]
                num = problem.getCostOfActions(nextActions) + heuristic(currState, problem)
                openset.push( (currState, nextActions), num)

    return []
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
