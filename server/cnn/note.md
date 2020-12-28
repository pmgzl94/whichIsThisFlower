too slow sliding window from an image of 244x244load image from sliding window


fix image resize, see how to handle different size of image => see ssp on resnet

choose which learning algorithm must we use: sgd ?


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