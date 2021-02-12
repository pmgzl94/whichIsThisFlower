from layer import LayerInterface

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
        arr = numpy.ones(inp.size)
        
        indices = numpy.random.choice(arr, size=int(nbneuron*self.p), replace=False, p=[1/nbneuron] * nbneuron)
        arr[indices] = 0
        
        arr = arr.reshape(self.ishape)
        self.derivative = arr

        return inp * arr
    
    def learn(self, delta):
        return delta * self.derivative