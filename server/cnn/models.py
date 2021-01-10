import conv
import image_loader as iml
import model
import pool
import fcnetwork


rp_dataset = "./dataset/"

example1 = rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg"

def return_response(res):
    labels = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
    res = list(res)
    idx = res.index(max(res))
    return labels[idx]

def zf5model(path=example1):
    # from this architecture: 
    # https://www.researchgate.net/figure/Architecture-of-ZF-model-An-3-channels-image-with-224224-is-as-the-input-It-is_fig5_318577329
    
    # image = iml.ImageLoader.getOutputNpArray(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg", gray=True)
    # image = iml.ImageLoader.getCropedImage(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg")#.getOutputNpArray(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg")

    #it crops by 224x224 by default
    input = iml.ImageLoader.getOutputNpArray(path, crop=True)

    layerContainer = [
        #3, 224, 224
        conv.ConvLayer(padding=1, filtershape=(96, 3, 7, 7), stride_length=2, pool=pool.PoolLayer(pad=1, pool_size=(3, 3), stride_length=2), ishape=(3, 224, 224)),
        #96, 55, 55
        conv.ConvLayer(filtershape=(256, 96, 5, 5), stride_length=2, pool=pool.PoolLayer(pad=1, pool_size=(3, 3), stride_length=2), ishape=(96, 55, 55)),
        #256, 26, 26
        conv.ConvLayer(padding=1, filtershape=(384, 256, 3, 3), stride_length=1, ishape=(256, 26, 26)),
        
        #384, 13, 13
        conv.ConvLayer(padding=1, filtershape=(384, 384, 3, 3), stride_length=1, ishape=(384, 13, 13)),

        #384, 13, 13
        conv.ConvLayer(padding=1, filtershape=(256, 384, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(3, 3), stride_length=2), ishape=(384, 13, 13)),

        #do use he initialization here
        fcnetwork.FCLayer(arch=[9216, 4096, 4096, 5])
    ]

    zf5 = model.Model(learning_rate=None, dataset=None, layerContainer=layerContainer)

    output = zf5.compute(input)

    print(f"first output = {output}")

    zf5.saveLayers(["conv1", "conv2", "conv3", "conv4", "conv5", "classifier"])

    layerContainer = [
        #3, 224, 224
        conv.ConvLayer(load_path="conv1"),
        #96, 55, 55
        conv.ConvLayer(load_path="conv2"),
        #256, 26, 26
        conv.ConvLayer(load_path="conv3"),
        
        #384, 13, 13
        conv.ConvLayer(load_path="conv4"),

        #384, 13, 13
        conv.ConvLayer(load_path="conv5"),

        #do use he initialization here
        fcnetwork.FCLayer(arch=[9216, 4096, 4096, 5], load_path="classifier")
    ]

    zf5 = model.Model(learning_rate=None, dataset=None, layerContainer=layerContainer)

    output = zf5.compute(input)

    print(f"snd output = {output}")

    try:
        output = zf5.compute(input)
    except:
        print("error occured in zf5 mode")
        return "error"
    return return_response(output)

print(zf5model())