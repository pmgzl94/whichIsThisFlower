
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
        self.learning_rate = learning_rate
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
    def compute(self, input, learn=False):
        x = input
        i = 1
        
        for layer in self.layercontainer:
            # print(x.shape)
            # if i == 1:
            #     print(f"input={x}")
            #     TensorFileManager().save("input_image", x)
            x = layer.compute(x, learn)

            # print(f"output = {x[2]}")
            # print(x.shape)

            # if i == 1:
            #     print(f"output {x}")
            #     TensorFileManager().save("output", x)
            i += 1
        return x

    def soft_learn(self):
        data = dataloader.load_some_flowers(crop_size=(0, 0, 150, 150))
        data = list(data)
        data = data[:10]
        success = 0
        
        for input, expec in data:

            self.compute(input, learn=True)
            
            success += self.layercontainer[-1].learn(expec)
            delta = self.layercontainer[-1].getLastDelta()
            
            #backpropagate the delta
            for i in range(2, len(self.layercontainer) + 1, 1):
                print(f"layer number = {-i}, len = {len(self.layercontainer) - 1}")
                self.layercontainer[-i].learn(delta)
                delta = self.layercontainer[-i].getLastDelta()
        # print(f"error rate = {success / len(data)}")
        # for i in range(0, len(self.layercontainer)):
        #     self.layercontainer[i].modify_weights(learning_rate=self.learning_rate, batch_size=10)

    def test_learn(self, epoch=10):
        data = dataloader.load_some_flowers(crop_size=(0, 0, 150, 150))
        data = list(data)
        data = data[:128]
        success = 0
        
        response_from_net = []
        for i in range(0, epoch):
            success = 0
            res = []
            for input, expec in data:

                res.append(self.compute(input, learn=True))

                success += self.layercontainer[-1].learn(expec)
                delta = self.layercontainer[-1].getLastDelta()
                
                #backpropagate the delta
                for i in range(2, len(self.layercontainer) + 1, 1):
                    # print(f"layer number = {-i}, len = {len(self.layercontainer) - 1}")
                    self.layercontainer[-i].learn(delta)
                    delta = self.layercontainer[-i].getLastDelta()
            print(f"error rate = {success / len(data)}")
            for i in range(0, len(self.layercontainer)):
                self.layercontainer[i].modify_weights(learning_rate=self.learning_rate, batch_size=10)
            response_from_net.append(res)
        # print(f'response net = {response_from_net}')

    #number of flowers = 4323
    def learn(self):
        #for now the classifier is the last layer
        print("learning")
        # data = dataloader.load_flowers()
        data = dataloader.load_some_flowers()
        data = list(data)

        print(f"len of data = {len(data)}")

        #for now it will be sgd learning algorithm
        # each layer should be able to give us the delta in order to backpropagate the learning
        # data = random.shuffle(data)

        batch = random.sample(data, len(data))
        batch_size = 10
        print(len(data)/10)

        # print(f"shape = {batch[0][0].shape}")
        # print(f"shape = {len(batch)}")
        
        # number_of_epoch = 10
        # for i in range(0, number_of_epoch):
        #     batch = random.sample(data, len(data))
        #     for input, expec in range(0, batch):
        #         self.compute(input, learn=True)
        #         #get delta from the classifier
        #         success = self.layercontainer[-1].learn(expec)
        #         delta = self.layercontainer[-1].getLastDelta()
        #         #backpropagate the delta
        #         cnt = 1
        #         for i in range(2, len(self.layercontainer) - 1, 1):
        #             print(f"layer number = {-i}, len = {len(self.layercontainer) - 1}")
        #             # if cnt == 2:
        #             #     return
        #             # print("within the loop")
        #             self.layercontainer[-i].learn(delta)
        #             delta = self.layercontainer[-i].getLastDelta()
        #             # cnt += 1
        #             # print(f"delta shape = {delta.shape}")
            
    
    # def loadModel(filenames): #must of forma
    def saveLayers(self, layersName=[]):  #must of format ["conv1", "conv2" ...]
        for i in range(0, len(self.layercontainer)):
            self.layercontainer[i].save(layersName[i])
        return layersName