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
        return numpy.load(self.dir + "/" + filename + ".npy")
