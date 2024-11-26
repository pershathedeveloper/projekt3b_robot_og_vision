class Queue:
    data = []

    def printElements(self):
        print(self.data)

    def enqueue(self, value):
        self.data.append(value)

    def dequeue(self):
        returnValue = self.data.pop(0)
        return returnValue
    
    def getNext(self):
        return self.data[0]


mq = Queue()
mq.printElements()

mq.enqueue(4)
mq.enqueue(6)
mq.enqueue(8)
mq.printElements()

test1 = mq.getNext()
print(test1)
mq.printElements()

test2 = mq.dequeue()
print(test2)
mq.printElements()