# from mnist import mnist_loader
import image_loader as iml
import os
import numpy

# def load_mnist():
#     train_data, validation_data, testdata = mnist_loader.load_data_wrapper("./mnist/")
#     return train_data

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

def slice_dataset(exp_res, ser_images, ipftrain, ipftest):

    sertest = []
    sertrain = []

    expectest = []
    expectrain = []

    inc = ipftrain
    inc2 = ipftest

    for i in range(0, len(ser_images), inc + inc2):
        expectrain = expectrain + exp_res[i: i + inc]
        expectest = expectest + exp_res[i + inc: i + inc + inc2]
    
        sertrain = sertrain + ser_images[i: i + inc]
        sertest = sertest + ser_images[i + inc: i + inc + inc2]

    test_data = zip(sertest, expectest)
    training_input = zip(sertrain, expectrain)

    return training_input, test_data
    

def load_some_flowers(training_data_amount, test_data_amount, crop_size=(0, 0, 224, 224)):
    subdirs = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
    
    #around 4300 pictures
    #number of flowers = 4323
    if test_data_amount + training_data_amount > 4300:
        raise Exception("There is only 4300 pictures in the dataset")

    serialized_im = []
    expected_res = []
    
    image_per_flower = (test_data_amount + training_data_amount) // 5

    # print(image_per_flower)

    for subdir in subdirs:
        path = "./dataset/" + subdir
        i = 0
        for f in os.listdir(path):
            if i == image_per_flower:
                break
            # nparray = iml.ImageLoader.getOutputNpArray(os.path.join(path, f))
            nparray = iml.ImageLoader.getOutputNpArray(image_path=os.path.join(path, f), crop=True, crop_size=crop_size)
            res = linker[subdir]
            serialized_im.append(nparray)
            expected_res.append(res)
            i += 1
    
    ipftrain = training_data_amount // 5
    ipftest = test_data_amount // 5

    return slice_dataset(expected_res, serialized_im, ipftrain, ipftest)
