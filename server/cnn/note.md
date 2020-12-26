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
