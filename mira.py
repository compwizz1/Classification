# mira.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# Mira implementation
import util
import random
PRINT = True

class MiraClassifier:
  """
  Mira classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mira"
    self.automaticTuning = False 
    self.C = 0.001
    self.legalLabels = legalLabels
    self.max_iterations = max_iterations
    self.initializeWeightsToZero()

  def initializeWeightsToZero(self):
    "Resets the weights of each label to zero vectors" 
    self.weights = {}
    for label in self.legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use
  
  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    "Outside shell to call your method. Do not modify this method."  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        Cgrid = [0.002, 0.004, 0.008]
    else:
        Cgrid = [self.C]
        
    return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
    """
    This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid, 
    then store the weights that give the best accuracy on the validationData.
    
    Use the provided self.weights[label] data structure so that 
    the classify method works correctly. Also, recall that a
    datum is a counter from features to values for those features
    representing a vector of values.
    """
    "*** YOUR CODE HERE ***"
    self.features = trainingData[0].keys() # could be useful later
	#initialize weight vectors
    #"""
    for label in self.legalLabels:
		for feature in self.features:
			self.weights[label][feature] = random.choice([-1, 1])
			self.weights[label]["Bias"] = random.choice([-1, 1])
    #"""
    originalweights = self.weights	
    bestC = 0
    bestGuesses = 0
    bestweights = {}
    for C in Cgrid:
		print "Testing C value ", C
		self.weights = originalweights
		for iteration in range(self.max_iterations):
			print "Starting iteration ", iteration, "..."
			for i in range(len(trainingData)):
				#Wrap trainingData in an array so self.weights[l] * multiplies all the features by all the weights
				guess = self.classify([trainingData[i]])
				if guess[0] != trainingLabels[i]:
					
					tau = min(
					C,
					(trainingData[i] * (self.weights[guess[0]] - self.weights[trainingLabels[i]])  + 1.0)/
					(2 * (trainingData[i] * trainingData[i]))
					)
					print tau
					update = trainingData[i].copy()
					update.multiplyAll(tau)
					self.weights[trainingLabels[i]] += update
					self.weights[trainingLabels[i]]["Bias"] += 1
					self.weights[guess[0]] -= update	
					self.weights[guess[0]]["Bias"] -= 1
		validationguesses = self.classify(validationData)
		guesscorrect = 0
		for i in range(len(validationguesses)):
			if validationguesses[i] == validationLabels[i]:
				guesscorrect += 1
		if guesscorrect > bestGuesses:
			print C, " is better than ", bestC
			bestC = C
			bestweights = self.weights
			bestGuesses = guesscorrect
    self.weights = bestweights
    self.C = bestC

  def classify(self, data ):
    """
    Classifies each datum as the label that most closely matches the prototype vector
    for that label.  See the project description for details.
    
    Recall that a datum is a util.counter... 
    """
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.weights[l] * datum
        vectors[l] += self.weights[l]["Bias"]
      guesses.append(vectors.argMax())
    return guesses

  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns a list of the 100 features with the greatest difference in feature values
                     w_label1 - w_label2

    """
    featuresOdds = []

    "*** YOUR CODE HERE ***"

    return featuresOdds

