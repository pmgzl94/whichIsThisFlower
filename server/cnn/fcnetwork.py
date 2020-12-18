import numpy as np
from tensor.Tensor import TensorFileManager
import math
import os
# class Forward():

def sigmoid(z):
    print(f"z = {z.shape}")
    return np.exp(z)/(1 + np.exp(z))

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
    
    def __init__(self, depth, transfer_learning_file):
        # + .bs + .ws
        dir = "./tensorfiles"
        print(transfer_learning_file)
        if not os.path.exists(dir + "/" + transfer_learning_file + ".ws1.npy"):
            raise Exception("tensor file not exists")
        
        self.weights = []
        self.biases = []
        self.depth = depth
        for i in range(0, depth):
            pathw = f"{transfer_learning_file}.ws{i + 1}"
            pathb = f"{transfer_learning_file}.bs{i + 1}"
            w = TensorFileManager("./tensorfiles").load(pathw)
            b = TensorFileManager("./tensorfiles").load(pathb)
            self.weights.append(w)
            self.biases.append(w)
        self.inputshape = (self.weights[0].shape[1],)

    def compute(self, input):
        # print(input.shape)
        print(input.shape)
        print(self.inputshape)
        # print(len(input.shape))

        # if len(input.shape) == 1 and input.shape[0] == self.inputshape[1]:
        #     input = input.reshape(1, input.shape[0])
        if input.shape != self.inputshape:
            raise Exception("wrong input shape")
        print(f'input shape after checking = {input.shape}')
        print(f'b shape = {self.biases}')
        print(f'w shape = {self.weights}')
        return self.forward(input)

    def forward(self, input):
        x = input
        print(self.weights[0].shape)
        print(self.weights[1].shape)
        for i in range(0, self.depth):
            print("1st it")
            # print(self.weights[)
            # print(self.weights.)
            # x = sigmoid(np.dot(self.weights.T, x) + self.biases[i])
            x = sigmoid(np.dot(x, self.weights[i].T) + self.biases[i])
            print(x)
        return x
