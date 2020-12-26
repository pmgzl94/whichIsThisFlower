import conv

rp_dataset = "./dataset/"

input_img_size = (244, 244)
# input_img_size = (28, 28)
image = conv.ImageLoader().getOutputNpArray(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg")
# iL

print(image.shape)

convLayer = conv.ConvLayer(padding=0, filtershape=(2,2), stride_length=1)

slicedImage = convLayer.enhancedSlidingWindow(image[0])

print(slicedImage.shape)

output = convLayer.compute(image[0])

print(output.shape)