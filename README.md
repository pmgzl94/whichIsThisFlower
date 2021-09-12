# whatIsThisFlower

That project come from a kaggle challenge:
https://www.kaggle.com/alxmamaev/flowers-recognition

## Client

A mobile app build with flutter. We can save and take picture from that. Mainly this app is supposed to be in use for people who is asking themselves which kind of flower they've seen. By taking picture, the mobile app request our server from which we will get a response.

## Server

A web server build with python (flask), and **GraphQL** ! Handles requests from the client.
As described before the server will classify the received picture and gives a response to the client.

That server can only classify flowers among the following:
- daisy
- dandelion
- rose
- sunflower
- tulip

## Classifier

That server uses a deep learning model to classify flowers.
We first use a convolutional neural network to try to identify pattern from the given picture through a certain number of layer.
Then we flat the result and give it to a neural network (that plays the classifier role).
The last layer of that classifier is a softmax layer.
For training we use the adam optimizer and the cross entropy loss function.

The model is inspired to that kaggle challenge solution: https://www.kaggle.com/sachinsharma1123/flowers-fun

## Choices & Next release

For now that model is really slowly to train. Firstly because we choose to do not use any DL framework, and build our own model by hand with numpy. Secondly our model can only take an input at a time and not a batch of inputs. For next releases we will fix that.

## Ressources used to build the model

_every single ressource will be added soon_

## Dataset

| https://www.kaggle.com/alxmamaev/flowers-recognition

once dowloaded you have to move the dataset to a particular place within the repository otherwise you be won't able to train the model.
