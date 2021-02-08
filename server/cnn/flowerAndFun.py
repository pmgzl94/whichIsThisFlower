
import image_loader as iml
import pool
import fcnetwork
import softmax
import conv
import adam
import model

import signal
import sys

saveModel = None
rp_dataset = "./dataset/"

# path = rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg"
example1 = rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg"


def flowerAndFun2(path=example1):
    def signal_handler(sig, frame):
        # saveModel.saveLayers(["ff2c1", "ff2c2", "ff2c3", "ff2fcn1", "ff2softm"])
        pic = iml.ImageLoader.getOutputNpArray(example1, crop=True, crop_size=(0, 0, 150, 150))

        y = saveModel.compute(pic)
        saveModel.saveLayers(["ff2c1", "ff2c2", "ff2c3", "ff2fcn1", "ff2softm"])
        print(y)
        sys.exit(0)
    input = iml.ImageLoader.getOutputNpArray(path, crop=True, crop_size=(0, 0, 150, 150))

    # layerContainer = [
    #     #3, 150, 150
    #     conv.ConvLayer(optimizer=adam.AdamConv(), filtershape=(32, 3, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(3, 150, 150)),
        
    #     #32, 74, 74
    #     conv.ConvLayer(optimizer=adam.AdamConv(), filtershape=(64, 32, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(32, 74, 74)),
      
    #     #64, 36, 36
    #     conv.ConvLayer(optimizer=adam.AdamConv(), filtershape=(128, 64, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(64, 36, 36)),
        
    #     #128, 17, 17
    #     fcnetwork.FCLayer(optimizer=adam.AdamFC(), arch=[36992, 512, 128], activation_func="relu", is_classifier=False),
        
    #     softmax.SoftmaxLayer(optimizer=adam.AdamFC(), arch=[128, 5])
    # ]
    # # load net
    layerContainer = [
        #3, 150, 150
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c1", filtershape=(32, 3, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(3, 150, 150)),
        
        #32, 74, 74
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c2", filtershape=(64, 32, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(32, 74, 74)),
      
        #64, 36, 36
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c3", filtershape=(128, 64, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(64, 36, 36)),
        
        #128, 17, 17
        fcnetwork.FCLayer(optimizer=adam.AdamFC(), load_path="ff2fcn1", arch=[36992, 512, 128], activation_func="relu", is_classifier=False),
        
        softmax.SoftmaxLayer(optimizer=adam.AdamFC(), load_path="ff2softm", arch=[128, 5])
    ]
    signal.signal(signal.SIGINT, signal_handler)

    ## here learning rate is useless
    model_FAndF = model.Model(learning_rate=0.001, dataset=None, layerContainer=layerContainer)


    saveModel = model_FAndF
    # saveModel.saveLayers(["ff2c1", "ff2c2", "ff2c3", "ff2fcn1", "ff2softm"])


    model_FAndF.test_learn(epoch=50)

flowerAndFun2()

def test_learn():
    layerContainer = [
        #3, 150, 150
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c1", filtershape=(32, 3, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(3, 150, 150)),
        
        #32, 74, 74
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c2", filtershape=(64, 32, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(32, 74, 74)),
      
        #64, 36, 36
        conv.ConvLayer(optimizer=adam.AdamConv(), load_path="ff2c3", filtershape=(128, 64, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(64, 36, 36)),
        
        #128, 17, 17
        fcnetwork.FCLayer(optimizer=adam.AdamFC(), load_path="ff2fcn1", arch=[36992, 512, 128], activation_func="relu", is_classifier=False),
        
        softmax.SoftmaxLayer(optimizer=adam.AdamFC(), load_path="ff2softm", arch=[128, 5])
    ]
    # signal.signal(signal.SIGINT, signal_handler)

    ## here learning rate is useless
    model_FAndF = model.Model(learning_rate=0.001, dataset=None, layerContainer=layerContainer)

    pic = iml.ImageLoader.getOutputNpArray(example1, crop=True, crop_size=(0, 0, 150, 150))

    y = model_FAndF.compute(pic)
    print(y)

# test_learn()
