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

    input = iml.ImageLoader.getOutputNpArray(path, crop=True)


    layerContainer = [
        conv.ConvLayer(padding=1, filtershape=(96, 3, 7, 7), stride_length=2, pool=pool.PoolLayer(pad=1, pool_size=(3, 3), stride_length=2)),
        conv.ConvLayer(filtershape=(256, 96, 5, 5), stride_length=2, pool=pool.PoolLayer(pad=1, pool_size=(3, 3), stride_length=2)),
        
        conv.ConvLayer(padding=1, filtershape=(384, 256, 3, 3), stride_length=1),
        conv.ConvLayer(padding=1, filtershape=(384, 384, 3, 3), stride_length=1),


        conv.ConvLayer(padding=1, filtershape=(256, 384, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(3, 3), stride_length=2)),

        fcnetwork.FCLayer(arch=[9216, 4096, 5])
    ]

    zf5 = model.Model(learning_rate=None, dataset=None, layerContainer=layerContainer)

    try:
        output = zf5.compute(input)
    except:
        print("error occured in zf5 mode")
        return "error"
    return return_response(output)

