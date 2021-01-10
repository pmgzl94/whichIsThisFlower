import numpy
import os

class TensorFileManager():
    def __init__(self, dir="./tensorfiles"):
        self.dir = dir
        if not os.path.exists(dir):
            os.mkdir(dir)
    def save(self, filename, ndarr):
        numpy.save(self.dir + "/" + filename, ndarr)
    def load(self, filename):
        return numpy.load(self.dir + "/" + filename + ".npy", allow_pickle=True)
    def loadNet(self, filename, nb_set_of_params): #for fcn
        weights = []
        biases = []
        for i in range(0, nb_set_of_params):
            pathw = f"{filename}.ws{i + 1}"
            pathb = f"{filename}.bs{i + 1}"
            w = self.load(pathw)
            b = self.load(pathb)
            weights.append(w)
            biases.append(b)
        return weights, biases

    def saveNet(self, filename, w, b): #for fcn
        nb_set_of_params = len(w)
        for i in range(0, nb_set_of_params):
            self.save(filename + f".ws{i+1}", w[i])
            self.save(filename + f".bs{i+1}", b[i])

    # def saveLayer(filename, layer):
    #     t = layer.getType()
    #     if t == "Conv":
    #         print("layerSaved")
    #     if t == "Dense":


    #     # from ast import literal_eval as make_tuple
    #     layer = 
