# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu,
# and credit to Peter Plantinga and Prashant Serai for
# their work in modifying these for The Ohio State University.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - getAction
        - update

      Instance variables you have access to
        - self.alpha (learning rate)
        - self.discount (discount rate i.e. gamma)
        - self.epsilon (exploration prob)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.getQValue = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.getQValue[(state,action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        return self.getQValue(state, self.computeActionFromQValues(state))

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """

  # Initialize max variables
        maxValue = -float('inf')
        maxActions = []

  # Iterate over actions to find max
        for action in self.getLegalActions(state):
            value = self.getQValue(state, action)

      # If we have a new max, restart list
            if value > maxValue:
                maxValue = value
                maxActions = [action]

      # If we've tied the max, add it to the list
            elif value == maxValue:
                maxActions.append(action)

  # Return best action
        if len(maxActions) == 0:
            return None
        else:
            return random.choice(maxActions)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should update the Q-Value (in self.qValues) here

          Instance variables you have access to
          - self.alpha (learning rate)
          - self.discount (discount rate i.e. gamma)
          - self.epsilon (exploration prob)
        """
        "*** YOUR CODE HERE ***"
        nextLegalActions = self.getLegalActions(nextState)

        # get the highest Q-value of the next state with every of its legal actions
        nextMax = -99999
        for nextAction in nextLegalActions:
            nextQvalue = self.getQValue[(nextState, nextAction)]
            if nextQvalue > nextMax:
                nextMax = nextQvalue

        # if there are no legal actions, the (highest) Q-value should be 0
        if not nextLegalActions:
            nextMax = 0

        # calculate the sample
        sample = reward + self.discount * nextMax
        # and update the Q-value of the current state + action
        self.getQValue[(state, action)] = self.getQValue[(state, action)] + \
            self.alpha * (sample - self.getQValue[(state, action)])

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

       

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise (computeActionFromQValues).

          HINT: You might want to use util.flipCoin(prob)

          Instance variables you have access to
          - self.alpha (learning rate)
          - self.discount (discount rate i.e. gamma)
          - self.epsilon (exploration prob)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if(util.flipCoin(self.epsilon)):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

        return action

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        return self.weights * self.featExtractor.getFeatures(state, action)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
           
           You can obtain the List of Features using:
           self.featExtractor.getFeatures
           #eg. list_of_features = self.featExtractor.getFeatures(state, action)

           And the weights for each feature are stored here:
           self.weights
           #eg. self.weights[feature]
        """
        "*** YOUR CODE HERE ***"
        nextMax = -99999
        for nextAction in nextLegalActions:
            nextQvalue = self.getQValue(nextState, nextAction)
            if nextQvalue > nextMax:
                nextMax = nextQvalue

        if not nextLegalActions:
            nextMax = 0

        difference = (reward + self.discount * nextMax) - \
            self.getQValue(state, action)
        features = self.featExtractor.getFeatures(state, action)

        # update the weight of every feature of the Q-value
        for featureKey in features:
            # featureKey is the name of the feature
            # featureValue is the value of that feature
            featureValue = features[featureKey]
            self.weights[featureKey] = self.weights[featureKey] + \
                self.alpha * difference * featureValue

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
