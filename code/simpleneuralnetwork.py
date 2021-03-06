# -*- coding: utf-8 -*-
"""SimpleNeuralNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fceFEehlxPsE2xSvCo206v-tT097dbXx
"""

### This is a simple neural network that is able to predict how fast a person 
### can sprint based on their age and weight

import torch
import torch.nn as nn


# DATA
# ------

# Note: tensor = vector

X = torch.tensor(([22, 180], [30, 155], [21, 205], [27, 190], [25, 160]), dtype=torch.float) # 5 X 3 tensor
y = torch.tensor(([16], [12], [9], [14], [15]), dtype=torch.float) # 5 X 1 tensor

# The single input that we want to use to predict if they will get the job
# using parameters learned from the neural network
xPredicted = torch.tensor(([18, 165]), dtype=torch.float) # 1 X 3 tensor


# SCALING THE DATA
# ------------------

# Gets the maximum value in a tensor
X_max, _ = torch.max(X, 0)
xPredicted_max, _ = torch.max(xPredicted, 0)

# Function to divide two tensors
X = torch.div(X, X_max)
xPredicted = torch.div(xPredicted, xPredicted_max)
y = y / 20


# COMPUTATION MODEL
# ------------------

# Class header that says we are defining a neural network
class Neural_Network(nn.Module):

  # Performed upon creating instance of neural network
  def __init__(self, ):
      super(Neural_Network, self).__init__()
      # parameters
      self.inputSize = 2
      self.outputSize = 1
      self.hiddenSize = 3

      # weight matrices
      self.weight1 = torch.randn(self.inputSize, self.hiddenSize) 
      self.weight2 = torch.randn(self.hiddenSize, self.outputSize)

  # This is where data enters and is fed into computation graph
  #
  # Takes input X and performs matrix multiplication with weight1
  # The result is applied a SIGMOID (activation function)
  #
  # This result is multiplied with weight2
  # The result is applied a SIGMOID (activation function) again
  # = output of the neural network
  #
  # This is called a --FORWARD PASS--
  def forward(self, X):
    self.z = torch.matmul(X, self.weight1) 
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = torch.matmul(self.z2, self.weight2)
    o = self.sigmoid(self.z3) # final activation function
    return o

  # Backpropagation algorithm, used to optimize the weights when training
  #
  # We want to MINIMIZE loss with respect to our weights
  # 
  def backward(self, X, y, o):
    self.o_error = y - o # error in output
    self.o_delta = self.o_error * self.sigmoidPrime(o) 
    self.z2_error = torch.matmul(self.o_delta, torch.t(self.weight2))
    self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)
    self.weight1 += torch.matmul(torch.t(X), self.z2_delta)
    self.weight2 += torch.matmul(torch.t(self.z2), self.o_delta)


  # Sigmoid function
  def sigmoid(self, s):
    return 1 / (1 + torch.exp(-s))
    
  #Sigmoid prime
  def sigmoidPrime(self, s):
    return s * (1 - s)

  def train(self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)
        
  def saveWeights(self, model):
    torch.save(model, "NN")
        
  def predict(self):
    print ("Predicted data based on trained weights: ")
    print ("Input (scaled): \n" + str(xPredicted))
    # print ("Output: \n" + str(self.forward(xPredicted)))
    print ("Output: \n" + str(self.forward(xPredicted)[0] * 20))


# TRAIN
# ------
NN = Neural_Network()

# We will train the neural network 1000 times
for i in range(1000):  
    print ("#" + str(i) + " Loss: " + str(torch.mean((y - NN(X))**2).detach().item())) 
    NN.train(X, y)
NN.saveWeights(NN)
NN.predict()
