# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math
import sys

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    self.prior = util.Counter()
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
	#create dictionary of all features for each label
    dict = {}
    for feature in self.features:
		for label in self.legalLabels:
			dict[feature, label] = util.Counter()
			for i in [0,1]: #values of a counter from datum
				dict[(feature, label)][i] = 0
				#print str(feature) + str(label) + ' ' + str(dict[(feature, label)])
    labelCount = util.Counter()
    for i in range(len(trainingData)):
		#increment occurrences of each label found in the training data
		label = trainingLabels[i]
		labelCount[label] += 1
		for feature in trainingData[i]:
			#increment dictionary value by 1 when a feature label combination with a value is found
			dict[(feature, label)][trainingData[i][feature]] += 1
    #normalize labelCount to get P(y) for each label y, or the prior probability 
    self.prior = util.normalize(labelCount)
	
    bestk = 0
    bestcond = {}
    topguesses = 0
	#iterate through each k to find the best k
    for k in kgrid:
		#empty cond probs
		self.condprobs = {} 
		#smooth data
		for feature_label in dict:
			tmpcounter = dict[feature_label] 
			#print feature_label
			tmpcounter.incrementAll(tmpcounter.keys(), k)
			#set condprobs to cond probs with current k value
			self.condprobs[feature_label] = util.normalize(tmpcounter)
		guesses = self.classify(validationData)
		guesscorrect = 0
		#print[guesses]
		for i in range(len(guesses)):
			if guesses[i] == validationLabels[i]:
				guesscorrect += 1
		if guesscorrect > topguesses:
			print "Guess ",k ," is better than ",bestk
			topguesses = guesscorrect
			bestcond = self.condprobs
			bestk = k
    self.condprobs = bestcond
    self.k = bestk 	
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    "*** YOUR CODE HERE ***"
	#Adds log(P(y)) to calculate P(y|f1,f2...)
    for label in self.legalLabels:
		logJoint[label] += math.log(self.prior[label])
	#Adds log(P(f1|y)), log(P(f2|y))... to calculate P(y|f1, f2...)
    for key in datum:
		#if key == (7, 3):
			#print self.condprobs[key, 0]
		for label in self.legalLabels:
			#print str(key) + str(datum[key])
			logJoint[label] += math.log(self.condprobs[key, label][datum[key]])
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
