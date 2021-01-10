
from layer import LayerInterface
import dataloader
import random
from tensor.Tensor import TensorFileManager

class Model():
    # type = CNN, FCN, RNN ...
    # dataset must be supervised
    def __init__(self, learning_rate, dataset, layerContainer=[]):
        # self.learn = learn()
        #self.modeltype = modeltype
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
        i = 1
        for layer in self.layercontainer:
            # print(x.shape)
            # if i == 1:
            #     print(f"input={x}")
            #     TensorFileManager().save("input_image", x)
            x = layer.compute(x)
            # print(f"output = {x}")

            # if i == 1:
            #     print(f"output {x}")
            #     TensorFileManager().save("output", x)
            i += 1
        return x

    def learn(self, input):
        #for now the classifier is the last layer
        data = dataloader.load_flower()
        data = list(data)

        #for now it will be sgd learning algorithm
        print("learning")
        # each layer should be able to give us the delta in order to backpropagate the learning
        data = random.shuffle(data)
        batch = data[:10]
        
        for input, expec in batch:
            self.compute(input)
            
            #get delta from the classifier
            success = self.layercontainer[-1].learn(input, expec)
            delta = self.layercontainer[-1].getLastDelta()
            #backpropagate the delta
            for i in range(2, len(self.layercontainer), 1):
                self.layercontainer[-i].learn(delta)
                delta = self.layercontainer[-i].getLastDelta()
    
    # def loadModel(filenames): #must of forma
    def saveLayers(self, layersName=[]):  #must of format ["conv1", "conv2" ...]
        for i in range(0, len(self.layercontainer)):
            self.layercontainer[i].save(layersName[i])
        return layersName