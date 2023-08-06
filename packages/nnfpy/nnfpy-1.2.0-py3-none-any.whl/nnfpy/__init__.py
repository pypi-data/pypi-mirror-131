import matplotlib.pyplot as plt
from pickle import dump, load


'''
This class stores the data of the network when it is training
'''


class StoreData:
    def __init__(self):
        self.costl = []
        self.learningl = []

    def __str__(self):
        return "This class stores the data of the network when it is training"


    '''
    This appends the cost to a list
    '''


    def cost(self, cost):
        self.costl.append(cost)


    '''
    This appends the learning rate to a list
    '''


    def learning(self, learning):
        self.learningl.append(learning)


    '''
    This returns the data stored in the class
    '''


    def returndata(self):
        return self.learningl, self.costl


    '''
    This plots the data stored in the class
    '''


    def plotdata(self):
        fig, axs = plt.subplots(nrows=2)
        axs[0].plot([i for i in range(len(self.costl))], [sum(i) for i in self.costl], color="blue")
        axs[1].plot(self.learningl, color="red")
        axs[0].set_title("Cost")
        axs[1].set_title("Learning")
        plt.show()


def storelist(chosenfile, wb):
    with open(chosenfile + ".list", "wb") as fp:
        dump(wb, fp)


def loadlist(chosenfile):
    with open(chosenfile + ".list", "rb") as fp:
        wb = load(fp)
    return wb