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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
    

    #python autograder.py -q q1 --no-graphics
    
    def evaluationFunction(self, currentGameState: GameState, action):
         # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newCapsules = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

       
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if len(foodDistances) > 0:
            closestFoodDistance = min(foodDistances)
        else:
            closestFoodDistance = 1

        ghost_distances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in successorGameState.getGhostStates()]
        ghostDistance = sum(ghost_distances) + len(ghost_distances)
        nearby = sum(1 for distance in ghost_distances if distance <= 1)

        capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in newCapsules]
        if len(capsuleDistances) > 0:
            closestCapsuleDistance = min(capsuleDistances)
        else:
            closestCapsuleDistance = 1

         # Increase score when close to capsule or if Ghost is scared
        if min(newScaredTimes) > 0 or closestCapsuleDistance <= 1:
            return successorGameState.getScore() + (1 / float(closestFoodDistance)) - (1 / float(ghostDistance)) - nearby + 10
        else:
            return successorGameState.getScore() + (1 / float(closestFoodDistance)) - (1 / float(ghostDistance)) - nearby

def scoreEvaluationFunction(currentGameState: GameState):
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
    #python autograder.py -q q2 --no-graphics
   
    def getAction(self, gameState: GameState):
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

        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:  #PacBoy
                return maxAgent(agentIndex, depth, gameState)
            else:  #GHOSTIES
                return minAgent(agentIndex, depth, gameState)

        def maxAgent(agentIndex, depth, gameState):
            legalActions = gameState.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(gameState)
            maxEval= float('-inf')
            for action in legalActions:
                nextState = gameState.generateSuccessor(agentIndex, action)
                maxEval = max(maxEval, minimax(agentIndex + 1, depth, nextState))

            return maxEval

        def minAgent(agentIndex, depth, gameState):
            legalActions = gameState.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(gameState)
            minEval = float('inf')
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth += 1

            for action in legalActions:
                nextState = gameState.generateSuccessor(agentIndex, action)
                minEval = min(minEval, minimax(nextAgent, depth, nextState))
            return minEval
        #Making sure there are legal actions, defaulating if not
        legalActions = gameState.getLegalActions()
        if legalActions:
            bestAction = legalActions[0]  
        else:
            bestAction = Directions.STOP  

        bestEval= float('-inf')
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            value = minimax(1, 0, nextState)
            if value > bestEval:
                bestEval = value
                bestAction = action

        return bestAction

       
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alpha_beta(agentIndex, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agentIndex == 0:  #PacBoy
                return maxAgent(agentIndex, depth, gameState, alpha, beta)
            else:  #GHOSTIES
                return minAgent(agentIndex, depth, gameState, alpha, beta)

        def maxAgent(agentIndex, depth, gameState, alpha, beta):
            maxEval = float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                maxEval = max(maxEval, alpha_beta(agentIndex + 1, depth, successor, alpha, beta))
                if maxEval > beta:
                    return maxEval
                alpha = max(alpha, maxEval)
            return maxEval

        def minAgent(agentIndex, depth, gameState, alpha, beta):
            minEval = float('inf')
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgentIndex == 0:
                depth += 1
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                minEval = min(minEval, alpha_beta(nextAgentIndex, depth, successor, alpha, beta))
                if minEval < alpha:
                    return minEval
                beta = min(beta, minEval)
            return minEval
        #Making sure there are legal actions, defaulating if not
        legalActions = gameState.getLegalActions()
        if legalActions:
            bestAction = legalActions[0]  
        else:
            bestAction = Directions.STOP  

        #intialize vales for pruning
        maxValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions():
            successor = gameState.generateSuccessor(0, action)
            value = alpha_beta(1, 0, successor, alpha, beta)
            if value > maxValue:
                maxValue = value
                bestAction = action
                alpha = max(alpha, maxValue)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agentIndex == 0: #Pacboy
                return maxAgent(agentIndex, depth, gameState)
            else: #GHOSTIES
                return expAgent(agentIndex, depth, gameState)

        def maxAgent(agentIndex, depth, gameState):
            legalActions = gameState.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(gameState)

            maxEval = float('-inf')
            for action in legalActions:
                nextState = gameState.generateSuccessor(agentIndex, action)
                maxEval = max(maxEval, expectimax(agentIndex + 1, depth, nextState))

            return maxEval

        def expAgent(agentIndex, depth, gameState):
            legalActions = gameState.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(gameState)
            expected = 0
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth += 1

            prob = 1 / len(legalActions)
            for action in legalActions:
                nextState = gameState.generateSuccessor(agentIndex, action)
                expected += prob * expectimax(nextAgent, depth, nextState)

            return expected

        #Making sure there are legal actions, defaulating if not
        legalActions = gameState.getLegalActions()
        if legalActions:
            bestAction = legalActions[0]  
        else:
            bestAction = Directions.STOP  

        bestVal = float('-inf')
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            value = expectimax(1, 0, nextState)
            if value > bestVal:
                bestVal = value
                bestAction = action

        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I adapeted my first function in order to fit the parameters of this better's input, adjusted weight values to be increased during Scared ghost or nearby Capsule>
    """
    # Useful information you can extract from a GameState (pacman.py)
  
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newCapsules =  currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
    if len(foodDistances) > 0:
        closestFoodDistance = min(foodDistances)
    else:
         closestFoodDistance = 1

    ghost_distances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in currentGameState.getGhostStates()]
    ghostDistance = sum(ghost_distances) + len(ghost_distances)
    nearby = sum(1 for distance in ghost_distances if distance <= 1)

    capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in newCapsules]
    if len(capsuleDistances) > 0:
        closestCapsuleDistance = min(capsuleDistances)
    else:
          closestCapsuleDistance = 1

        # Increase score when close to capsule or if Ghost is scared
    if min(newScaredTimes) > 0 or closestCapsuleDistance <= 1:
           return currentGameState.getScore() + (1 / float(closestFoodDistance)) - (1 / float(ghostDistance)) - nearby + 100
    else:
            return currentGameState.getScore() + (1 / float(closestFoodDistance)) - (1 / float(ghostDistance)) - nearby




# Abbreviation
better = betterEvaluationFunction

