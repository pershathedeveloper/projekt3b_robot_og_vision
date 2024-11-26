# If example
import time
state = 0
counter = 0

while(True):
    if(state == 0):
        print("state:", state)
        counter = counter + 1
        if(counter >= 10):
            state = 1
        time.sleep(0.2)
    elif(state == 1):
        print("state:", state)
        break


# OOP Example
import statemachine
class counterState(statemachine.State):
    def Enter(self):
        print("state: Counter")
        self.counter = 0

    def Execute(self):
        self.counter = self.counter + 1
        print("counter:", self.counter)
        if(self.counter >= 10):
            self.stateMachine.ChangeState(doneState())
        time.sleep(0.2)

class doneState(statemachine.State):
    def Enter(self):
        print("state: Done")
        self.stateMachine.running = False

sm = statemachine.StateMachine(counterState())
sm.Run()