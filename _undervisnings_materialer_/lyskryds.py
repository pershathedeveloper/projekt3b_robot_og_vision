import statemachine
import time

class Red(statemachine.State):
    def Enter(self):
        print("Red")

    def Execute(self):
        time.sleep(2)
        self.stateMachine.ChangeState(RedYellow())

class RedYellow(statemachine.State):
    def Enter(self):
        print("RedYellow")
    
    def Execute(self):
        time.sleep(1)
        self.stateMachine.ChangeState(Green())

class Yellow(statemachine.State):
    def Enter(self):
        print("Yellow")

    def Execute(self):
        time.sleep(1)
        self.stateMachine.ChangeState(Red())

class Green(statemachine.State):
    def Enter(self):
        print("Green")

    def Execute(self):
        time.sleep(2)
        self.stateMachine.ChangeState(Yellow())

sm = statemachine.StateMachine(Red())
sm.Run()