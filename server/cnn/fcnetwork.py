import numpy as np
from tensor.Tensor import TensorFileManager
import math
import os
# class Forward():

def sigmoid(z):
    # print(f"z = {z.shape}")
    return np.exp(z)/(1 + np.exp(z))

class FCNetwork():
    def __init__(self, arch, transfer_learning=None):
        #unused
        # if transfer_learning is None:
            #create random weight and biases
        # else:
        self.weights = []
        self.biases = []
        for i in range(0, len(arch) - 1):
            net = numpy.random.random([arch[i], archi[i+1]])
            weights.append(net)
            biases = numpy.random.random([1, arch[i]])
        self.inputshape = (1, arch[0])
        self.depth = len(arch)
    
    def __init__(self, depth, transfer_learning_file):
        dir = "./tensorfiles"
        if not os.path.exists(dir + "/" + transfer_learning_file + ".ws1.npy"):
            raise Exception("tensor file not exists")
        
        self.depth = depth
        
        tfm = TensorFileManager("./tensorfiles")
        self.weights, self.biases = tfm.loadNet(transfer_learning_file, depth)
        
        self.inputshape = (self.weights[0].shape[1],)

    def compute(self, input):
        if input.shape != self.inputshape:
            raise Exception("wrong input shape")
        return self.forward(input)

    def forward(self, input):
        x = input
        for i in range(0, self.depth):
            x = sigmoid(np.dot(x, self.weights[i].T) + self.biases[i])
            print(x)
        return x
