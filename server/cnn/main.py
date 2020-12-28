import conv
import image_loader as iml

##to change

rp_dataset = "./dataset/"

# image = iml.ImageLoader().getOutputNpArray(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg", gray=True)
image = iml.ImageLoader().getOutputNpArray(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg")

print(image.shape)

convLayer = conv.ConvLayer(padding=0, filtershape=(2,2), stride_length=1)

slicedImage = convLayer.enhancedSlidingWindow(image[0])

print(slicedImage.shape)

output = convLayer.compute(image[0])

print(output.shape)