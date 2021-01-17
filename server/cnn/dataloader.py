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

def load_flowers(crop_size=(0, 0, 224, 224)):
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

    print(f"nb flower = {len(training_input)}")

    # print(os.listdir("./dataset/daisy"))
    return training_input

def load_some_flowers(image_per_flower=3, crop_size=(0, 0, 224, 224)):
    subdirs = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
    # subdirs = ["daisy"]

    serialized_im = []
    expected_res = []

    for subdir in subdirs:
        path = "./dataset/" + subdir
        i = 1
        for f in os.listdir(path):
            if i == image_per_flower:
                break
            # nparray = iml.ImageLoader.getOutputNpArray(os.path.join(path, f))
            nparray = iml.ImageLoader.getOutputNpArray(image_path=os.path.join(path, f), crop=True, crop_size=crop_size)
            res = linker[subdir]
            serialized_im.append(nparray)
            expected_res.append(res)
            i += 1
    training_input = zip(serialized_im, expected_res)

    # print(os.listdir("./dataset/daisy"))
    return training_input

# a = load_flowers()
# b = list(a)

# print(b[0])

# a=load_mnist()
# b = list(a)

# print(b[0][1]) ##res