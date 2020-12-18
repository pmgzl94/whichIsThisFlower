import numpy as np
from tensor.Tensor import TensorFileManager
import math
import os
# class Forward():

def sigmoid(z):
    return math.exp(z)/(1 + math.exp(z))

class FCNetwork():
    def __init__(self, arch, transfer_learning=None):
        #load tensor
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
    
    def __init__(self, transfer_learning_file):
        # + .bs + .ws
        dir = "./tensorfiles"
        print(transfer_learning_file)
        if not os.path.exists(dir + "/" + transfer_learning_file + ".bs.npy"):
            raise Exception("tensor file not exists")
        self.weights = TensorFileManager("./tensorfiles").load(transfer_learning_file + ".ws")
        self.biases = TensorFileManager("./tensorfiles").load(transfer_learning_file + ".bs")

        print(self.weights[0].shape)
        print(self.weights)
        if len(self.weights.shape) != 1:
            self.inputshape = (1, self.weights[0].shape[0])
        else:
            self.inputshape = (1, self.weights.shape[0])
        print(self.inputshape)
        self.depth = len(self.weights) + 1


    def compute(self, input):
        # print(input.shape)
        if input.shape != self.inputshape:
            raise Exception("wrong input shape")
        return self.forward(input)

    def forward(self, input):
        x = input
        for i in range(0, self.depth-1):
            x = sigmoid(np.dot(self.weights[i], x) + self.biases[i])
        return x
