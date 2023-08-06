import time
from random import randint
layertypes = ["fullcon", "endlayer", "2Dpool", "noise", "loss", "boost", "SmartBoost", "twoDtooneD", "dropout", "recurrent"]


'''
This class calulates the time in hours, minutes and seconds
'''


class timer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.type = "time"
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.settime()
    

    '''
    Converts 60 seconds to 1 minute and 60 minutes to 1 hour
    '''


    def settime(self):
        while self.seconds >= 60:
            self.minutes += 1
            self.seconds -= 60
        while self.minutes >= 60:
            self.hours += 1
            self.minutes -= 60

    def time(self):
        return str(self.hours) + " Hours, " + str(self.minutes) + " Minutes, " + str(round(self.seconds, 2)) + " Seconds"


'''
This is the network class
This will takes layers as an input
It will store the layers
It will then use the layers to run the network
'''

class network:
    def __init__(self, layers):
        self.layers = layers
        self.prevcost = []

    def __str__(self):
        return "This is the network class\nThis will takes layers as an input\nIt will store the layers\nIt will then use the layers to run the network"


    '''
    This functions runs the network through training
    It will run the set amount of epochs and then stop
    '''


    def runnet(self, alpha, epochs, inputs, outputs, storedata=None, regularization=None, momentum=None, printevery=None, batchsize=1):
        inputs = inputs
        outputs = outputs
        totalcost = 0
        start = 0
        if momentum is not None: # Checks if momentum has been assigned
            for layer in self.layers: # Goes through the layers and applies the momentum class to all the fullcon layers
                if layer.type == "fullcon":
                    layer.applymomentum(momentum)
        else:
            for layer in self.layers: # If no momentum has been assigned it will apply None to the momentum of all the fullcon layers
                if layer.type == "fullcon":
                    layer.applymomentum(None)
        for layer in self.layers: # Makes sure that the learning rate starts at the right amount
            if layer.type == "loss":
                alpha += alpha - layer.newrate(alpha)
        for i in range(epochs * batchsize):
            chosen = randint(0, len(inputs) - 1) # Randomly chooses a input to run the network on
            chosenin = inputs[chosen]
            chosenout = outputs[chosen]
            inc = 0
            for layer in self.layers: # Loops through layers performing their functions
                try:
                    try:
                        if layer.type == "fullcon":
                            chosenin = layer.forwardpass(chosenin)
                        elif layer.type == "endlayer":
                            predout, cost = layer.out(chosenin, chosenout)
                        elif layer.type == "loss":
                            alpha = layer.newrate(alpha)
                        elif layer.type == "boost":
                            alpha = layer.boost(i, alpha)
                        elif layer.type == "SmartBoost":
                            alpha = layer.boost(i, alpha, epochs)
                        elif layer.type == "twoDtooneD":
                            chosenin = layer.changeoneD(chosenin)
                        elif layer.type == "dropout":
                            chosenin = layer.drop(chosenin)
                            self.layer[inc-1].changeouts(chosenin)
                        elif layer.type == "recurrent":
                            chosenin = layer.forwardpass(chosenin)
                    except AttributeError:
                        raise RuntimeError("The object is not a valid layer")
                except AttributeError:
                    raise RuntimeError("The object is not a valid layer")
                inc += 1
            if storedata is not None: # Checks if storedata has been assigned
                try:
                    storedata.learning(alpha) # Saves the current data
                    storedata.cost(cost)
                except AttributeError:
                    raise RuntimeError("The object is not a valid storedata class")
            if i != 0 and i % batchsize == 0: # Checks if the network has completed the batch
                cost = [i / batchsize for i in totalcost] # Gets the average of the costs
                for t in range(len(self.layers) - 1, 0, -1): # Goes backwards through the network
                    if self.layers[t - 1].type == "fullcon" or self.layers[t - 1].type == "recurrent":
                        try:
                            cost = self.layers[t - 1].backprop(cost, alpha) # Works out the new costs
                            self.layers[t - 1].update()
                        except AttributeError:
                            raise RuntimeError("The object is not a valid layer")
                    elif self.layers[t - 1] == "changeoneD":
                        self.layers[t - 1].changetwoD(cost) # Changes the costs dimensions
                    elif self.layers[t - 1] == "2Dpool":
                        cost = self.layers[t - 1].backprop(cost, alpha) # Works out the new costs
                        self.layers[t - 1].update()
                totalcost = [0 for i in range(len(cost))]
            elif i == 0:
                totalcost = cost
            else:
                totalcost = [cost[i] + totalcost[i] for i in range(len(totalcost))] # If the network has not completed the batch it will add the cost to the network
            if printevery is not None: # Checks if printevery has been assigned
                if i % (printevery * batchsize) == 0: # Checks if the set amount of epochs has been compleated
                    if i != 0: # Checks if it is not the first epoch
                        print("\n\nEpoch No. " + str(int(i / batchsize)) + "\nPast " + str(printevery) + " epochs took: " + timer(seconds=(round(time.time() - start, 3))).time() + "\nEstimated time: " + timer(seconds=(round(time.time() - start, 3)*(epochs*batchsize-i)/(printevery*batchsize))).time())
                        start = time.time()
                    else:
                        print("\n\nCurrent epoch is: " + str(int(i / batchsize)))
                        start = time.time()

        if storedata is not None: # Checks if storedata has been assigned
            return storedata


    '''
    This functions works out the output of the network based on the input
    It will also work out the cost of the network and output it
    This will also return the outputs
    '''


    def predwithout(self, inputs, outputs):
        av = [0 for _ in range(len(outputs[0]))]
        outputlist = []
        for i in range(len(inputs)):
            chosenin = inputs[i]
            chosenout = outputs[i]
            for layer in self.layers: # Runs through the layers
                if layer.type == "fullcon":
                    try:
                        chosenin = layer.forwardpass(chosenin)
                    except AttributeError:
                            raise RuntimeError(f"The object is not a valid layer")
                elif layer.type == "endlayer":
                    try:
                        predout, cost = layer.out(chosenin, chosenout) # Predicts the final output of the network
                    except AttributeError:
                            raise RuntimeError(f"The object is not a valid layer")
                    av = [cost[i] + av[i] for i in range(len(cost))] # Adds to the average cost
                    print(f"Input was: {str(inputs[i])}, target output was: {str(outputs[i])}, predicted output was: {str([float(s) for s in predout])}") # Prints the output and cost
                    outputlist.append([inputs[i], outputs[i], predout])
        print("Average cost was: " + str([float(i / len(inputs)) for i in av])) # Prints the average cost
        return outputlist


    '''
    This function works out the output of the network based on the input
    This does not work out the cost and will return the outputs
    '''


    def pred(self, inputs):
        outputlist = []
        for i in range(len(inputs)):
            chosenin = inputs[i]
            for layer in self.layers: # Runs through layers
                try:
                    if layer.type == "fullcon":
                        chosenin = layer.forwardpass(chosenin)
                    elif layer.type == "endlayer":
                        predout = layer.pred(chosenin) # Predicts the final output of the network
                        outputlist.append([inputs[i], predout]) 
                except AttributeError:
                        raise RuntimeError(f"The object is not a valid layer")
        return outputlist


    '''
    This function will apply weights and biases to the network
    '''


    def applywb(self, wb):
        curwb = 0
        for layer in self.layers: # Runs through the layers
            try:
                if layer.type == "fullcon" or layer.type == "recurrent":
                    layer.loadwb(wb[curwb]) # Applies weights
            except AttributeError:
                raise RuntimeError(f"The object is not a valid layer")
            curwb += 1


    '''
    This function will return the weights and biases of the netwokr
    '''


    def returnwb(self):
        wb = []
        for layer in self.layers: # Runs through layers
            if layer.type == "fullcon" or layer.type == "recurrent":
                try:
                    wb.append(layer.returnwb()) # Appends the weights and biases
                except AttributeError:
                    raise RuntimeError(f"The object is not a valid layer")
        return wb


class recurrentnet(network):
    def runnet(self, alpha, epochs, inputs, outputs, storedata=None, regularization=None, momentum=None, printevery=None, batchsize=1):
        inputs = inputs
        outputs = outputs
        totalcost = 0
        start = 0
        if momentum is not None: # Checks if momentum has been assigned
            for layer in self.layers: # Goes through the layers and applies the momentum class to all the fullcon layers
                if layer.type == "fullcon":
                    layer.applymomentum(momentum)
        else:
            for layer in self.layers: # If no momentum has been assigned it will apply None to the momentum of all the fullcon layers
                if layer.type == "fullcon":
                    layer.applymomentum(None)
        for layer in self.layers: # Makes sure that the learning rate starts at the right amount
            if layer.type == "loss":
                alpha += alpha - layer.newrate(alpha)
        for i in range(epochs * batchsize):
            chosen = randint(0, len(inputs) - 1) # Randomly chooses a input to run the network on
            choseninput = inputs[chosen]
            chosenoutput = outputs[chosen]
            totcost = 0
            for t in range(len(chosenoutput)):
                inc = 0
                chosenout = [chosenoutput[t]]
                chosenin = [choseninput[t]]
                for layer in self.layers: # Loops through layers performing their functions
                    try:
                        try:
                            if layer.type == "fullcon":
                                chosenin = layer.forwardpass(chosenin)
                            elif layer.type == "endlayer":
                                predout, cost = layer.out(chosenin, chosenout)
                            elif layer.type == "loss":
                                alpha = layer.newrate(alpha)
                            elif layer.type == "boost":
                                alpha = layer.boost(i, alpha)
                            elif layer.type == "SmartBoost":
                                alpha = layer.boost(i, alpha, epochs)
                            elif layer.type == "twoDtooneD":
                                chosenin = layer.changeoneD(chosenin)
                            elif layer.type == "dropout":
                                chosenin = layer.drop(chosenin)
                                self.layer[inc-1].changeouts(chosenin)
                            elif layer.type == "recurrent":
                                chosenin = layer.forwardpass(chosenin)
                        except AttributeError:
                            raise RuntimeError("The object is not a valid layer")
                    except AttributeError:
                        raise RuntimeError("The object is not a valid layer")
                    inc += 1
                totcost += cost[0] / len(chosenoutput)
            for layer in self.layers:
                if layer.type == "recurrent":
                    layer.resetinps()
            cost = [totcost]
            if storedata is not None: # Checks if storedata has been assigned
                try:
                    storedata.learning(alpha) # Saves the current data
                    storedata.cost(cost)
                except AttributeError:
                    raise RuntimeError("The object is not a valid storedata class")
            if i != 0 and i % batchsize == 0: # Checks if the network has completed the batch
                cost = [i / batchsize for i in totalcost] # Gets the average of the costs
                for t in range(len(self.layers) - 1, 0, -1): # Goes backwards through the network
                    if self.layers[t - 1].type == "fullcon" or self.layers[t - 1].type == "recurrent":
                        try:
                            cost = self.layers[t - 1].backprop(cost, alpha) # Works out the new costs
                            self.layers[t - 1].update()
                        except AttributeError:
                            raise RuntimeError("The object is not a valid layer")
                    elif self.layers[t - 1] == "changeoneD":
                        self.layers[t - 1].changetwoD(cost) # Changes the costs dimensions
                    elif self.layers[t - 1] == "2Dpool":
                        cost = self.layers[t - 1].backprop(cost, alpha) # Works out the new costs
                        self.layers[t - 1].update()
                totalcost = [0 for i in range(len(cost))]
            elif i == 0:
                totalcost = cost
            else:
                totalcost = [cost[i] + totalcost[i] for i in range(len(totalcost))] # If the network has not completed the batch it will add the cost to the network
            if printevery is not None: # Checks if printevery has been assigned
                if i % (printevery * batchsize) == 0: # Checks if the set amount of epochs has been compleated
                    if i != 0: # Checks if it is not the first epoch
                        print("\n\nEpoch No. " + str(int(i / batchsize)) + "\nPast " + str(printevery) + " epochs took: " + timer(seconds=(round(time.time() - start, 3))).time() + "\nEstimated time: " + timer(seconds=(round(time.time() - start, 3)*(epochs*batchsize-i)/(printevery*batchsize))).time())
                        start = time.time()
                    else:
                        print("\n\nCurrent epoch is: " + str(int(i / batchsize)))
                        start = time.time()

        if storedata is not None: # Checks if storedata has been assigned
            return storedata

    def predwithout(self, inputs, outputs):
        av = [0 for _ in range(len(outputs[0]))]
        totalouts = []
        for i in range(len(inputs)):
            outputlist = []
            choseninput = inputs[i]
            chosenoutput = outputs[i]
            for t in range(len(chosenoutput)):
                chosenout = [chosenoutput[t]]
                chosenin = [choseninput[t]]
                for layer in self.layers: # Runs through the layers
                    if layer.type == "fullcon":
                        try:
                            chosenin = layer.forwardpass(chosenin)
                        except AttributeError:
                                raise RuntimeError(f"The object is not a valid layer")
                    elif layer.type == "endlayer":
                        try:
                            predout, cost = layer.out(chosenin, chosenout) # Predicts the final output of the network
                        except AttributeError:
                                raise RuntimeError(f"The object is not a valid layer")
                        av = [cost[i] + av[i] for i in range(len(cost))] # Adds to the average cost
                        print(f"Input was: {str(choseninput[t])}, target output was: {str(chosenoutput[t])}, predicted output was: {str([float(s) for s in predout])}") # Prints the output and cost
                        outputlist.append([choseninput[t], chosenoutput[t], predout])
                    elif layer.type == "recurrent":
                        chosenin = layer.forwardpass(chosenin)
                totalouts.append(outputlist)
        print("Average cost was: " + str([float(i / len(inputs)) for i in av])) # Prints the average cost
        return outputlist

    def pred(self, inputs):
        totalouts = []
        for i in range(len(inputs)):
            outputlist = []
            choseninput = inputs[i]
            for t in range(len(choseninput)):
                chosenin = [choseninput[t]]
                for layer in self.layers: # Runs through layers
                    try:
                        if layer.type == "fullcon":
                            chosenin = layer.forwardpass(chosenin)
                        elif layer.type == "endlayer":
                            predout = layer.pred(chosenin) # Predicts the final output of the network
                            outputlist.append([inputs[i], predout])
                    except AttributeError:
                            raise RuntimeError(f"The object is not a valid layer")
            totalouts.append(outputlist)
        return outputlist

'''
This function is for raising an invalid layer when other methods do not work
'''


def raiseinvalidlayer():
    raise RuntimeError("Layer is invalid")


'''
This function will create a network with error handling
'''


def describenet(func):
    def ex(*args, **kwargs):
        layertypes = ["fullcon", "endlayer", "2Dpool", "loss", "boost", "SmartBoost", "twoDtooneD", "dropout"]
        retdata = func(*args, **kwargs)
        layers = args[0]
        networkdesc = ""
        for layer in layers:
            if len(networkdesc) == 0:
                if layer.type == "fullcon":
                    networkdesc += "The network starts with fully connected " + str(layer.activationtype) + " layer with " + str(len(layer.weights)) + " neurons."
            else:
                if layer.type == "fullcon":
                    networkdesc += "\nThis then follows with a fully connected " + str(layer.activationtype) + " layer with " + str(len(layer.weights)) + " neurons."
        print(networkdesc)
        print("\n\n")
        return retdata
    return ex

@describenet
def create(layers, nettype="default"):
    if nettype == "default":
        return network([layer if any(layer.type == name for name in layertypes) else raiseinvalidlayer() for layer in layers])
    elif nettype == "recurrent":
        return recurrentnet([layer if any(layer.type == name for name in layertypes) else raiseinvalidlayer() for layer in layers])