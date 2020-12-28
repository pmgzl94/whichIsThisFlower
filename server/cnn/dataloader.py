from mnist import mnist_loader
import image_loader as iml
import os
import numpy

def load_mnist():
    train_data, validation_data, testdata = mnist_loader.load_data_wrapper("./mnist/")
    return train_data


linker = {  "daisy": numpy.array([1, 0, 0, 0, 0]),
            "dandelion": numpy.array([0, 1, 0, 0, 0]), 
            "rose": numpy.array([0, 0, 1, 0, 0]),
            "sunflower": numpy.array([0, 0, 0, 1, 0]),
            "tulip": numpy.array([0, 0, 0, 0, 1]),
            }

def load_flowers(dirpath="./dataset"):
    subdirs = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
    # subdirs = ["daisy"]

    serialized_im = []
    expected_res = []

    for subdir in subdirs:
        path = "./dataset/" + subdir
        for f in os.listdir(path):
            nparray = iml.ImageLoader.getOutputNpArray(os.path.join(path, f))
            res = linker[subdir]
            serialized_im.append(nparray)
            expected_res.append(res)
    training_input = zip(serialized_im, expected_res)

    # print(os.listdir("./dataset/daisy"))
    return training_input

# a = load_flowers()
# b = list(a)

# print(b[0])

# a=load_mnist()
# b = list(a)

# print(b[0][1]) ##res