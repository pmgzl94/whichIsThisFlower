import numpy as np
from tensor.Tensor import TensorFileManager
import os
from layer import LayerInterface

# activation functions
def sigmoid(z):
    # print(f"z = {z.shape}")
    return np.exp(z)/(1 + np.exp(z))

def sigmoid_derivative(z):
    res = sigmoid(z)
    return res - np.power(res, 2)

#cost functions
def basic_cost_derivative(y, a): #where y is the expected result
    return a - y

#cross entropy


class FcLayer(LayerInterface):
    # def __init__(self, *args):
    #     if len(a) == 1:
    #         create_net(args)
    #     elif len(a) == 2:
    #         reload_net(args)
    def __init__(self, arch, transfer_learning_file=None):
        self.weights = []
        self.biases  = []

        self.nb_layer = len(arch)
        self.nb_set_of_params = self.nb_layer - 1

        if transfer_learning_file == None:
            for i in range(0, self.nb_set_of_params):
                set_of_weights = np.random.random((arch[i+1], arch[i]))
                self.weights.append(set_of_weights)
                self.biases.append(np.random.random((arch[i+1],)))
                # print(self.biases[-1].shape)
                # print(self.weights[-1].shape)
        else:
            self.reload_net(self.nb_layer, transfer_learning_file)
        self.inputshape = (self.weights[0].shape[1],)
        
        #learning vars: used for backpropagation
        self.a = []
        self.z = []

        self.sum_of_nabla_w = []
        self.sum_of_nabla_b = []

        self.lastDelta = None

        self.resetLearningVars()
    
    def reload_net(self, nb_layer, transfer_learning_file):
        dir = "./tensorfiles"
        if not os.path.exists(dir + "/" + transfer_learning_file + ".ws1.npy"):
            raise Exception("tensor file not exists")
        
        tfm = TensorFileManager("./tensorfiles")
        self.weights, self.biases = tfm.loadNet(transfer_learning_file, self.nb_set_of_params)
        
    def compute(self, input):
        if input.shape != self.inputshape:
            raise Exception("wrong input shape")
        return self.forward(input)

    def forward(self, input):
        self.a = []
        self.z = []
        
        x = input
        self.a = [x] #usefull for the backprop
        for i in range(0, self.nb_set_of_params):
            z = np.dot(x, self.weights[i].T) + self.biases[i]
            x = sigmoid(z)
            self.z.append(z)
            self.a.append(x)
        return x
    def getType(self):
        return "FCLayer"
    

    def learn(self, input, expected_res):
        self.forward(input)
        #first delta
        delta = basic_cost_derivative(expected_res, self.a[-1]) * sigmoid_derivative(self.z[-1])
        # print(delta.shape)
        nabla_w = [np.outer(delta, self.a[-2].T)]
        # print(nabla_w[0].shape)
        nabla_b = [delta]

        for idx_layer in range(self.nb_layer - 2, 0, -1): #-2 : -1 for index and -1 for the previous final layer
            index_set_param = idx_layer - 1
            delta = np.dot(delta, self.weights[index_set_param + 1]) * sigmoid_derivative(self.z[index_set_param])
            
            nabla_w.insert(0, np.outer(delta, self.a[index_set_param - 1].T))
            # print(nabla_w[0])
            nabla_b.insert(0, delta)
        self.lastDelta = delta
        self.sumUpNablas(nabla_w, nabla_b)
        #return error percentage

    def resetLearningVars(self):
        self.sum_of_nabla_w = []
        self.sum_of_nabla_b = []
        for i in range(0, self.nb_set_of_params):
            self.sum_of_nabla_w.append(np.zeros(self.weights[i].shape))
            self.sum_of_nabla_b.append(np.zeros(self.biases[i].shape))
            # print(f"les wei{self.weights[i].shape}")
            # print(f"les bias{self.biases[i].shape}")
        
        self.lastDelta = None
        self.a = []
        self.z = []
    
    #use for the sgd
    def sumUpNablas(self, nabla_w, nabla_b):
        for i in range(0, self.nb_set_of_params):
            # print(f'shapes {self.sum_of_nabla_w[i].shape}, {nabla_w[i].shape}')
            self.sum_of_nabla_w[i] + nabla_w[i]
            self.sum_of_nabla_w[i] = self.sum_of_nabla_w[i] + nabla_w[i]
            self.sum_of_nabla_b[i] = self.sum_of_nabla_b[i] + nabla_b[i]

a = FcLayer(arch=[2, 3, 2])

a.learn(np.array([1, 2]), np.array([1, 0]))