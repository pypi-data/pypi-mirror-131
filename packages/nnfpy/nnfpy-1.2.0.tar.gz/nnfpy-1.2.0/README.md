# **NNFPY**

Welcome to a project I have been working on for a while and have decided to make this a public package

This package is used to create neural networks with 'ease'

### Aim

The aim of this program is not to just make neural networks quicker to make but easier to understand, the learning gap for a lot of stuff in programming **can** be massive, and this package (and hopefully more) should help

We hope to do this with indepth tutorials (eventually when most of the errors are fixed) and non cryptic error messages that you spend hours seaching stackoverflow for the solution, just to find you accidently had a variable containing a string rather than a integer

### Example

It compresses a whole neural network down to this:

```
net = onednet.create([denselayer("relu", 2, 64), denselayer("relu", 64, 2), endlayer("softmax"), timesloss(0.00001)])

data = net.runnet(0.1, 50000, X, y, storedata(), momentum=momentum(0.5), printevery=1000, batchsize=100)

outs = net.predwithout(X, y)
```

Just to basically describe what has happened in these lines of code:

The first line has created a network with one input layer taking two input values a hidden layer of 64 neurons and an output layer of 2 output

The second line has run the network a 50000 times

The third line shows the predictions and the average cost

## **Installing**

To install excecute the following command

>pip install nnfpy
