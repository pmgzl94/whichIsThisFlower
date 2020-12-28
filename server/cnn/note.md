### learning algorithm used

SGD

## handle different size image

link: https://arxiv.org/pdf/1406.4729.pdf
I used spatial pyramid pooling

for the specified architecture there was 5 conv layers in the last conv layer instead of using a max pooling, we use spp.
spp take 3 times the feature map and slice by 1x1, 2x2, 4x4 by taking each time the biggest element 
that same feature map has 256 filters we get: 1x1x256, 2x2x256, 4x4x256
then all of these element are concatenated like that: 4x4x256 ++ 2x2x256 ++ 1x1x256
then we get a 1x1x4096 input for the classifier.

## sliding window to get feature map

I used numpy.lib.strides_tricks.as_strided
link: https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html

each numpy array has a stride for example an array of shape (4, 3) as a stride of (24, 8), 8 because for moving an element to another and 24 to get to the next row.

then I use the dot product between the filter and the sliced image.

## track input of the choosen element during pooling

...

### note worthy

see: max poling, relu, softmax, padding

read: visualizing cnn, and deep learning book, about soft max and cross entropy in neuralnetwork and deeplearning

training algorithm:
it takes 60000 pics to train and 10000 pics to test

pooling layer:

layers in a model looks as follow:
- image input
- convlayer
- nonlinearity(relu)
- pooling layer

more here https://machinelearningmastery.com/pooling-layers-for-convolutional-neural-networks/


## To note

error rate is measured like that: $(y - a)^2$

## TODO

backprop cnn browser's marknotes
visualizing cnn (notes)
spp (notes)
resnet to reco plante 
softmax => have to find the derivative

read deep learning book

add multiple filter according to the depth of the feature map

add saveNet to tensorfile manager
add cross entropy 
add SaveModel to tensorfile manager