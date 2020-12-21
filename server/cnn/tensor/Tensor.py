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
    def loadNet(self, filename, nb_set_of_params):
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