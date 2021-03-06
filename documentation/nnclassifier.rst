*************************
Neural Network Classifier
*************************

##################
##################
.. contents::
  :local:
  :depth: 8

==========================
Overview
==========================
Neural networks are computing systems that are modeled after the brains of living animals. They consist of neurons that are all connected to create a network. These systems "learn" from data that is provided to them. By providing neural networks with enough data, they are capable of making accurate predictions by training and learning from the data.

==========================
The Basics
==========================
The function of neural networks is fairly straightforward and basic. An input is provided to the network, and after some calculations are made, an output is returned. For example, if we wanted to have a program that could determine if there is a dog in a picture then the input to the neural network would be a picture, and the output would be true or false based on whether the network thinks the picture contains a dog or not.

In order for neural networks to be able to make these predictions, they must be given data to train. Training a neural network involves providing a large amount of input data and it's corresponding output data. Neural networks are able to make calculations to infer relationships between the inputs and outputs, and create a system for accurately being able to predict an outcome when only given an input.

============================
Convolutional Neural Network
============================
The architecture that is behind neural networks is always fairly straightforward. While there are many different types of architectures 
that are used for getting more accurate predictions in specific scenarios, they all involve input nodes and an output node, or "neuron". The input neurons take data about a scenario, and multiple layers on the "inside" of the network calculate what the outcome will be. What makes a neural network "deep" is when there are more than a single layer of neurons between the input and output neurons, as can be seen below. 

For more information on the process of the Convolutional Neural Network (CNN) see [8] https://adventuresinmachinelearning.com/convolutional-neural-networks-tutorial-in-pytorch/


===========================================
Code for a Simple Neural Network Classifier
===========================================
To begin writing code with the PyTorch library, it is important to ensure that you have imported torch at the beginning of your python program. In the following code snippet, we import torch neural network library as well as an optimizer for the neural network which will be explained in further detail in step 6. 

.. code:: python

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim

For this particular example, we will need to import the torchvision library for the data set as well.
The dataset consists of classes airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck. The images in CIFAR-10 are of size 3x32x32 . i.e. 3-channel color images of 32x32 pixels in size.

.. code:: python

    import torchvision
    import torchvision.transforms as transforms
    
In addition to the dataset we will need to import matplotlib and numpy to plot the images as well as use numpy for some computation.

.. code:: python
    
    import matplotlib.pyplot as plt
    import numpy as np

--------------------------------
Step 1: Data - CIFAR10
--------------------------------
Load and Nomralize CIFAR10 dataset. 

The following line creates a transforms variable used to create training sets and data sets, it is a list of transforms which is created by transforms.Compose() function. The output of the torchivision dataset we are using in this example are PIL images of range [0, 1]. We use transforms.Compose() as a function to compose several image transformations together. Within the parameters of the Compose function, we state transforms.ToTensor() covert the PIL image to a tensor which is a generalization of vectors and matrices representing a multidimensional array which will be processed as the data input. transforms.Normalize() takes in Tensor image size (C, H, W) as a parameter and normalizes a tensor image with mean and standard deviation.

.. code:: python

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])
    
Now we define training set and a test set with the CIFAR10 dataset. There are many data sets that could be used using the torchvision library such as MNIST, Flickr, USPS, KMNIST, and many more. For this example we use the CIFAR10 dataset explained earlier on this page. The parameters are root, train, transform, and download. Using these, we will define a training set of data and a test set of data. \

**root** is just the root directory of dataset which we use './data' \

**train** is a parameter if set True, creates a dataset from training set otherwise it creates from the test set.\

**transform** is a function/transform that takes a PIL image as input and outputs a transformed version which we defined above. \

**download** is a parameter if set True, downloads the dataset from the internet and puts it in the root directory.\

.. code:: python
    
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    
    testset = torchvision.datasets.CIFAR10(root='./data', train = False, download=True, transform=transform)
    
Now we will actually "load" the dataset. Using the PyTorch utility for data loading, torch.utils.data.DataLoader() represents a Python iterable over a dataset that supports map-style and iterable-style datasets, custom data loading order, automatic batching, single/multi-process data loading, and automatic memory pinning. See [5] https://pytorch.org/docs/stable/data.html for more information on how to utilize this DataLoader class. For now and our purposes we will manipulate the dataset, batch_size, shuffle, and num_workers parameters. We will create a loader for the training set and the testing set. \

**dataset** indicates a dataset object to load data from. For our case, it is the trainset and the testset we created previously and we will load data for training and testing. \

**batch_size** indicates how many samples per batch to load, we will set 4 but if you wanted to see more images, you may increase this number the default is 1.\

**shuffle** defines the strategy to draw samples from the dataset set it True or False. We set it to be True in the training set and false in the testset \

**num_workers** indicates how many subprocesses to use for data loading. So 0 means that the data will be loaded in the main process.\



.. code:: python
    
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,shuffle=True, num_workers=2)
    
    testloader = torch.utils.data.DataLoader(testset, batch_size=4,shuffle=False, num_workers=2)


Now we define the variable classes for labeling purposes of the dataset images like so..

.. code:: python

    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


The following code block is a complete code block of this step. We will break it down further and explain each function and variable.

.. code:: python
    
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])
    
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    
    testset = torchvision.datasets.CIFAR10(root='./data', train = False, download=True, transform=transform)
    
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,shuffle=True, num_workers=2)
    
    testloader = torch.utils.data.DataLoader(testset, batch_size=4,shuffle=False, num_workers=2)
    
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    
Now run the program we have so far and you should be able to see this output.

.. code:: python

    #Output
    Downloading https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz to ./data/cifar-10-python.tar.gz
    Extracting ./data/cifar-10-python.tar.gz to ./data
    Files already downloaded and verified
    
    
    
The following code snippets will be functions that will get and plot some image files from the CIFAR10 dataset which we loaded in the code snippet shown above. In this snippet we will use numpy and matplotlib to show the images. To use different datasets in the torchvision library instead of CIFAR10 see [4] https://pytorch.org/docs/stable/torchvision/datasets.html#cifar .

.. code:: python

    def imshow(img):
        img = img / 2 + 0.5
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1,2,0)))
        plt.show()
    
    # obtain some random training images
    dataiter = iter(trainloader)
    images, labels = dataiter.next()
    
    # show images
    imshow(torchvision.utils.make_grid(images))
    # print labels
    print(' '.join('%5s' % classes[labels[j]] for j in range(4)))
    
    
The following images contain the console output if the code were to be run as of now.

.. figure:: ../_img/step1output.JPG

---------------------------------------------
Step 2: Define a Convolutional Neural Network
---------------------------------------------
Now that we have loaded and normalized our dataset, we will define our Neural Network Model. Our Convolutional Neural Network will take 3-channel images. This is where the torch.nn library will be used to define our neural network. For further reading, visit references [6] https://pytorch.org/tutorials/beginner/nn_tutorial.html and [7] https://pytorch.org/docs/stable/nn.html .

.. code:: python

    import torch
    import torch.nn as nn
    import torch.nn.functional as F

nn.Module is a PyTorch specific base class that we use to model our Neural Network.

For the convolution layer, the Conv2d function applies a 2 dimensional convolution over an input signal composed of several input planes. In this case, it takes in 3 parameters, in_channels(int), out_channels(int), and kernel_size(int). \

**in_channels** is the number of channels in the input image. \

**out_channels** is the number of channels produced by the convolution.\

**kernel_size** is the size of the convolving kernel.\

For the pooling layers, we use the MaxPool2d to apply max pooling over an input signal composed of several planes. In this case, it takes in the input of kernel_size height and weight (kH, kW).  

For the fc1, fc2, and fc3, which are fully-connected layers we define those using the nn.Linear function which applies a linear transformation to the incoming data given 2 parameters in this case. nn.Linear(in_features, out_features). Using these fully-connected layers, we "flatten" the deminesions of the output of our CNN. \

**in_features** is the size of each input sample \

**out_features** is the size of each output sample \

.. code:: python

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(3, 6, 5)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 5 * 5, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 10)
            
In this step, we will also define a forward propagation function within the neural network. This step describes the pooling process for the CNN using its properties we defined above. We take x, the input image, then pool using the relu function on its convolution stage and the fully connected layers to return an output.

.. code:: python

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = x.view(-1, 16 * 5 * 5)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x
            
Finally, create an instance of your neural network.

.. code:: python
            
    net = Net()
    
    

--------------------------------------------
Step 3: Define a Loss Function and Optimizer
--------------------------------------------
In this step we define a loss function and an optimizer. A loss function as discussed in Logistic Regression, Backpropagation, and the Gradient Descent section will map values of one or more variables into a real number representing a cost to an event. In this code snippet we will use the CrossEntropyLoss. This is a Loss function defined in PyTorch. There are several alternatives that include L1Loss, MSELoss, CTCLoss, NLLLoss, and many more see [9] https://pytorch.org/docs/stable/nn.html#torch.nn.CrossEntropyLoss for more details on Loss functions. CrossEntropyLoss measures the performance of a classification model which outputs a value between 0 and 1 useful in classification problem with various classes.

And we define it like so in a variable named criterion..

.. code:: python

    criterion = nn.CrossEntropyLoss()
    
When defining our optimizer which will attempt to minimize loss, this is where the torch.optim libary comes into play.

.. code:: python

    import torch.optim as optim

In this code snippet, we will use SGD which stands for Stochastic Gradient Descent. This optimizer object holds the current state and updates parameters based on the computed gradients. The simple update rule is weight = weight - learning_rate * gradient. For more information on SGD and other alternatives for optimizers see [10] https://pytorch.org/docs/stable/optim.html

And we define the optimizer like so in a variable named optimizer.. lr is the learning rate and momentum is the momentum factor. net.parameters() is our neural net attributes.

.. code:: python

    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    
  

-------------------------------------
Step 4: Training the Network
-------------------------------------
At this point, we have defined our dataset, our Convolutional Neural Network, forward propagation, loss function, and optimizer. Now, we will train the neural network. \

An epoch is a complete presentation of the data set. As we iterate through the epoch, we will also iterate through the trainloader previous defined. We want to create an input and label variable of the data in trainloader and perform a zero_grad optimization which clears the gradients of all optimized tensors before performing backpropagation with the loss function since PyTorch accumulates the gradients on subsequent backward passes. Then we put the inputs through the neural net by net(inputs). \

We then perform the loss function by calling criterion on our outputs and labels. Then call loss.backward() which computes the loss for every parameter x which is then accumulated into the gradient. Then we apply the optimizer.step() method that updates the parameter that performs a single optimization step. Add the loss item into the running_loss variable.

.. code:: python

    for epoch in range(2):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
            if i % 2000 == 1999:
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0
    
    print('Finished Training')

In this code, we print the running_loss every 2000 iteration and reset to 0. The output should look something like this.. You should be able to see the loss decrease as the training iterations increase.

.. code:: python

    [1,  2000] loss: 2.211
    [1,  4000] loss: 1.824
    [1,  6000] loss: 1.649
    [1,  8000] loss: 1.560
    [1, 10000] loss: 1.500
    [1, 12000] loss: 1.460
    [2,  2000] loss: 1.376
    [2,  4000] loss: 1.370
    [2,  6000] loss: 1.333
    [2,  8000] loss: 1.300
    [2, 10000] loss: 1.321
    [2, 12000] loss: 1.272
    Finished Training

To move onto testing on testloader, save your trained Neural Network model like so.. PyTorch allows you to save and load Neural Network models.

.. code:: python

    PATH = './cifar_net.pth'
    torch.save(net.state_dict(), PATH)

-------------------------------------
Step 5: Test the Network on Test Data
-------------------------------------
Now we have trained our neural network, time to test it on some test data which we defined in step 1. In the following code snippet, we will display some images from the test set and label with the correct label of the images.

.. code:: python

    dataiter = iter(testloader)
    images, labels = dataiter.next()
    
    imshow(torchvision.utils.make_grid(images))
    print('GroundTrute: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))
    
    
Now let's create an instance of our Neural Network previously defined and load your saved Neural network. Put the images through the neural network and output its predictions using torch.max which returns the maximum value of all elements in the input tensor.
    
.. code:: python

    net = Net()
    net.load_state_dict(torch.load(PATH))
    
    outputs = net(images)
    
    _, predicted = torch.max(outputs, 1)
    print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(4)))
    
Running this code should provide the following output.

.. figure:: ../_img/step6output_a.JPG

You have just created a Neural Network Classifier. Now let's test on the whole dataset. \

We will calculate correctness on the entire data set as well as each class of images. Keep a variable count variable for correct and total. 

.. code:: python

    correct = 0
    total = 0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    
torch.no_grad() is a context manager that disables gradient calculation. It reduces memory consumption for computations that would otherwise have gradient requirements set to be true. 
    
.. code:: python

    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            c = (predicted == labels).squeeze()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1
            
    print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
    
    for i in range(10):
    print('Accuracy of %5s : %2d %%' % (classes[i], 100 * class_correct[i] / class_total[i]))




------------------------------------------
Step 6: Results
------------------------------------------
The output should look something like this..

.. figure:: ../_img/step6output.JPG


=============
References
=============
This tutorial was inspired by the tutorial provided at https://pytorch.org/docs/stable/torchvision/transforms.html created by 14 contributors, last contributed on October 13, 2019.  View contributors and contributions here: https://github.com/pytorch/tutorials/blob/master/beginner_source/blitz/cifar10_tutorial.py

Additional Supplementary References: 

[1] https://pytorch.org/docs/stable/torchvision/transforms.html \
[2] https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html#sphx-glr-beginner-blitz-neural-networks-tutorial-py \
[3] https://pytorch.org/docs/stable/torchvision/transforms.html \
[4] https://pytorch.org/docs/stable/torchvision/datasets.html#cifar \
[5] https://pytorch.org/docs/stable/data.html \
[6] https://pytorch.org/tutorials/beginner/nn_tutorial.html \
[7] https://pytorch.org/docs/stable/nn.html \
[8] https://adventuresinmachinelearning.com/convolutional-neural-networks-tutorial-in-pytorch/ \
[9] https://pytorch.org/docs/stable/nn.html#torch.nn.CrossEntropyLoss \
[10] https://pytorch.org/docs/stable/optim.html \

=============
Code
=============
.. _nnClassCode: ../code/NNclassifier.py
`Full Code Steps 1 - 4 <nnClassCode_>`_

.. _nnClassTest: ../code/NNclassifier_test.py
`Full Code Step 5 <nnClassTest_>`_

=============
Next Section
=============
.. _reg: regularization.rst
`Next Section: More on Deep Neural Networks: Regularization <reg_>`_ 
