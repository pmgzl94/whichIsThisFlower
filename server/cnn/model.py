
from layer import LayerInterface

# class Layer(): #layer can contain multiple layer
#     def __init__(self, shape, type):
#         #type: fc, featuremap, maxpooling


# class LayersContainer(): #or net
#     def __init__(): #for now there is now model

#     def addLayer():
        
#     def build:

class Model():
    #CNN, FCN, RNN ...
    def __init__(self, learning_rate, dataset, layerContainer=[], modeltype="FCN"):
        # self.learn = learn()
        self.modeltype = modeltype
        self.dataset = dataset
        self.layercontainer = layerContainer 
        self.nb_layers = len(self.layercontainer)
    def addLayer(self, newLayer):
        # type1 = layerContainer[-1].getType()
        # type2 = newLayer.getType()
        # if type1 == "FCN" and type2 == type1:
        #     type1 = 
        layercontainer.append(newlayer)
        self.nb_layers += 1
    def compute(self, input):
        x = input
        for layer in self.layercontainer:
            x = layer.compute()
        return x
    def learn():
        print("learning")

