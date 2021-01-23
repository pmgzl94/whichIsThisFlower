import numpy

class LayerInterface():
    def compute(self, input):
        pass
    def getType(self):
        pass

# a = 
# a = [LayerInterface]
# a.append(FeatureMap((10, 10), (2, 2), 0))
# print(a[-1].getType())


# class PoolingLayer(LayerInterface):

