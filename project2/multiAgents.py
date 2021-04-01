# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodlist=currentGameState.getFood().asList()
        mindistance=float('inf') # the distance from successor state to the closest food

        for g in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos,g)<2):  # if ghost is close,
                return -float('inf')             # avoid it


        for f in foodlist:
            temp=manhattanDistance(newPos,f)
            if (temp<mindistance):
                mindistance=temp

        # set as "penalty" the distance from successor state to the closest food
        return successorGameState.getScore() - mindistance


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self,gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # minimax should find the best next move (with the best score) the from current state
        bestScore,bestNextMove=self.minimax(self.index,gameState)
        return bestNextMove


    def minimax(self,agent,gameState,depth=0):
        # Pacman agent is the maximizer (zero value)
        # Ghosts agents are minimizers (values greater than zero)
        bestAction=None
        if (depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return [self.evaluationFunction(gameState),bestAction]
        if (agent==0): # pacman agent
            return self.maxvalue(agent,gameState,depth)
        else:          # ghosts agents
            return self.minvalue(agent,gameState,depth)

    def maxvalue(self,maximizingPlayer,gameState,depth):
        bestAction=None
        best=-float('inf')
        for succ in gameState.getLegalActions(maximizingPlayer):
            temp=best
            value=self.minimax((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(maximizingPlayer,succ),depth+1)[0]
            best=max(best,value)
            if temp!=best:
                bestAction=succ
        return [best,bestAction]

    def minvalue(self,minimizingPlayer,gameState,depth):
        bestAction=None
        best=float('inf')
        for succ in gameState.getLegalActions(minimizingPlayer):
            temp=best
            value=self.minimax((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(minimizingPlayer,succ),depth+1)[0]
            best=min(best,value)
            if temp!=best:
                bestAction=succ
        return [best,bestAction]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # alpha-beta should find the best next move (with the best score) from the current state
        bestScore,bestNextMove=self.alphabeta(self.index,gameState)
        return bestNextMove
        # util.raiseNotDefined()

    def alphabeta(self,agent,gameState,alpha=-float("inf"),beta=float("inf"),depth=0):
        # Pacman agent is the maximizer (zero value)
        # Ghosts agents are minimizers (values greater than zero)
        bestAction=None
        if (depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return [self.evaluationFunction(gameState),bestAction]
        if (agent==0): # pacman agent
            return self.maxvalue(agent,gameState,alpha,beta,depth)
        else: # ghosts agents
            return self.minvalue(agent,gameState,alpha,beta,depth)


    def maxvalue(self,maximizingPlayer,gameState,alpha,beta,depth):
        bestAction=None
        best=-float('inf')
        for succ in gameState.getLegalActions(maximizingPlayer):
            temp=alpha
            value=self.alphabeta((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(maximizingPlayer,succ),alpha,beta,depth+1)[0]
            best=max(value,best)
            alpha=max(alpha,best)
            if alpha>beta: # alpha-beta pruning
                return [best,bestAction]

            if temp!=alpha:
                bestAction=succ
        return [best,bestAction]

    def minvalue(self,minimizingPlayer,gameState,alpha,beta,depth):
        bestAction=None
        best=float('inf')
        for succ in gameState.getLegalActions(minimizingPlayer):
            temp=beta
            value=self.alphabeta((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(minimizingPlayer,succ),alpha,beta,depth+1)[0]
            best=min(value,best)
            beta=min(beta,best)
            if beta<alpha: # alpha-beta pruning
                return [best,bestAction]

            if temp!=beta:
                bestAction=succ
        return [best,bestAction]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # expectiminimax should find the best next move (with the best score) from the current state
        # (the ghosts move randomly)
        bestScore,bestNextMove=self.expectiminimax(self.index,gameState,None)
        return bestNextMove
        # util.raiseNotDefined()



    def expectiminimax(self,agent,gameState,action,depth=0):
        # Pacman agent is the maximizer (zero value)
        # Ghosts agents are minimizers (values greater than zero)
        bestAction=None
        if (depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return [self.evaluationFunction(gameState),bestAction]
        if (agent==0): # pacman agent (maximizer)
            return self.maxvalue(agent,gameState,action,depth)
        else: # ghosts agents choosing uniformly at random from their legal moves
            return self.expvalue(agent,gameState,action,depth)

    def maxvalue(self,maximizingPlayer,gameState,action,depth):
         bestAction=None
         best=-float('inf')
         for succ in gameState.getLegalActions(maximizingPlayer):
             temp=best
             value=self.expectiminimax((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(maximizingPlayer,succ),succ,depth+1)[0]
             if value is None:
                 continue
             best=max(best,value)
             if temp!=best:
                 bestAction=succ
         return [best,bestAction]

    def expvalue(self,minimizingPlayer,gameState,action,depth):
         average=0
         prob=1/len(gameState.getLegalActions(minimizingPlayer)) # chance node (uniform probability of ghost's legal moves)
         for succ in gameState.getLegalActions(minimizingPlayer):
             bestAction=self.expectiminimax((depth+1) % gameState.getNumAgents(),gameState.generateSuccessor(minimizingPlayer,succ),action,depth+1)
             if bestAction[0] is None:
                 continue
             average=average+bestAction[0]*prob
         return [average,action] # action and the expected value of this (average)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score=currentGameState.getScore()
    newPos=currentGameState.getPacmanPosition()
    food=currentGameState.getFood().asList()

    minfood=float("inf") # the distance from the current state to the closest food
    closest_ghost=float("inf") # the distance from the current state to the closest ghost
    closest_capsule=float("inf") # the distance from the current state to the closest capsule

    capsules=len(currentGameState.getCapsules())
    foods=len(food)

    if currentGameState.isWin():
        float("inf")

    if currentGameState.isLose():
        -float("inf")

    for f in food:
        minfood=min(minfood,manhattanDistance(newPos,f))

    for c in currentGameState.getCapsules():
        closest_capsule=min(closest_capsule,manhattanDistance(newPos,c))

    for g in currentGameState.getGhostPositions():
        closest_ghost=min(closest_ghost,manhattanDistance(newPos,g))
        if manhattanDistance(newPos,g)==1:
            return -float("inf")


    # the estimate of utility of the pacman situation is related with:
    # 1) the closest ghost from the current state
    # 2) the closest food from the current state
    # 3) the closest capsule from the current state
    # 4) the number of the remaining capsules
    # 5) the number of the remaining foods
    # ("+1" to avoid division with zero)
    return score + closest_ghost/100 + 1/minfood + 1/(closest_capsule+1)*300 + 1/(capsules+1)*1000 +  1/(foods+1)*10000
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
