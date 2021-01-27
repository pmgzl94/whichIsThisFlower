
from layer import LayerInterface
import dataloader
import random
from tensor.Tensor import TensorFileManager
import numpy

from evaluation import evaluate_test_data, evaluate_test_flower_verbose

# import mnist

class Model():
    # learning must be supervised
    def __init__(self, learning_rate, dataset, layerContainer=[]):
        # self.learn = learn()
        #self.modeltype = modeltype
        self.learning_rate = learning_rate
        self.dataset = dataset
        self.layercontainer = layerContainer 
        self.nb_layers = len(self.layercontainer)

    #evaluation function
    evaluate_test_data = evaluate_test_data
    evaluate_test_flower_verbose = evaluate_test_flower_verbose

    def addLayer(self, newLayer):
        layercontainer.append(newlayer)
        self.nb_layers += 1

    def compute(self, input, learn=False):
        x = input
        
        for layer in self.layercontainer:
            x = layer.compute(x, learn)
        return x

    def soft_learn(self):
        data = dataloader.load_some_flowers(image_per_flower=3, crop_size=(0, 0, 150, 150))
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

    # def test_learn_mnist(self, epoch=50):
    #     training_data, vdata, test_data = mnist.mnist_loader.load_data_wrapper("./mnist/")


    #     training_data = list(training_data)
    #     test_data = list(test_data)
        
    #     n_training_data = len(training_data)
    #     batch_size = 10

    #     # print(f"Len = training_data = {len(training_data)}")
    #     # print(f"Len = test_data = {len(test_data)}")

    #     for ep in range(0, epoch):
    #         success = 0
    #         res = []
    #         data = random.sample(training_data, n_training_data)

    #         for b in range(0, n_training_data, batch_size):
    #             batch = data[b:b+batch_size]
    #             for input, expec in batch:
    #                 self.compute(input, learn=True)

    #                 success += self.layercontainer[-1].learn(expec)
                    
    #                 delta = self.layercontainer[-1].getLastDelta()

    #                 #We have only one layer so no need a backprop loop

    #             self.layercontainer[0].modify_weights(learning_rate=self.learning_rate, batch_size=batch_size)

    #         print(f"error rate = {success / len(training_data)}")
    #         result = self.evaluate_test_data(test_data)
    #         print(f"Epoch {ep}: {result}/{len(test_data)}")




    def test_learn(self, epoch=10):
        training_data, test_data = dataloader.load_some_flowers(500, 100, crop_size=(0, 0, 150, 150))
        

        training_data = list(training_data)
        test_data = list(test_data)

        print(f"len training data = {len(training_data)}")
        print(f"len test data = {len(test_data)}")
        # print(len(test_data))

        batch_size = 10
        
        # response_from_net = []
        for ep in range(0, epoch):
            success = 0
            res = []

            for b in range(0, 600, batch_size):

                training_data = random.sample(training_data, len(training_data))

                for input, expec in training_data[b:batch_size]:

                    res.append(self.compute(input, learn=True))

                    success += self.layercontainer[-1].learn(expec)
                    delta = self.layercontainer[-1].getLastDelta()
                    
                    #backpropagate the delta
                    for i in range(2, len(self.layercontainer) + 1, 1):
                        # print(f"layer number = {-i}, len = {len(self.layercontainer) - 1}")
                        self.layercontainer[-i].learn(delta)
                        delta = self.layercontainer[-i].getLastDelta()
                for i in range(0, len(self.layercontainer)):
                    self.layercontainer[i].modify_weights(learning_rate=self.learning_rate, batch_size=batch_size)
            print(f"error rate = {success / len(training_data)}")
            # result = self.evaluate_test_data(test_data)
            result = self.evaluate_test_flower_verbose(test_data)
            
            print(f"Epoch {ep}: {result}/{len(test_data)}")
                # response_from_net.append(res)
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