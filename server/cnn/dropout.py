from layer import LayerInterface
import numpy

class DropoutLayer(LayerInterface):
    # if you precise padding, you will only get a padding of 1

    def __init__(self, p=0.2, ishape=(10, 10, 10)):
        self.ishape = ishape
        self.p = p
        self.derivative = None
    
    def compute(self, inp, learn=False):
        if learn == False:
            return inp
        nbneuron = inp.size
        arr = numpy.ones(inp.size, dtype=numpy.int8)
        
        indices = numpy.random.choice(arr, size=int(nbneuron*self.p), replace=False, p=[1/nbneuron] * nbneuron)
        # print(indices)
        arr[indices] = 0
        
        arr = arr.reshape(self.ishape)
        self.derivative = arr

        # print(inp*arr)

        return inp*arr
    
    def learn(self, delta):
        d = delta
        if (delta.shape != self.ishape):
            d = d.reshape(self.ishape)
        self.lastDelta = d * self.derivative
        return self.lastDelta
    def getLastDelta(self):
        return self.lastDelta
    def modify_weights(self, learning_rate, batch_size):
        pass
    def save(self, filename):
        pass
