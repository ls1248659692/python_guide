class StateMachine(object):

    def __init__(self, init_state):
        self.current_state = init_state
        self.current_state.run()

    def step(self, action):
        self.current_state = self.current_state.next(action)
        self.current_state.run()


class State(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<State '%s'>" % self.name

    def next(self, action):
        if (self, action) in mapping:
            next_state = mapping[(self, action)]
        else:
            next_state = self
        print("%s + %s => %s" % (self, action, next_state))
        return next_state

    def run(self):
        print(self, "is current state")


class Action(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Action '%s'>" % self.name


State.Running = State("Running")
State.Stopped = State("Stopped")
State.Paused = State("Paused")

Action.start = Action("start")
Action.stop = Action("stop")
Action.pause = Action("pause")
Action.resume = Action("resume")


mapping = {
    (State.Stopped, Action.start): State.Running,
    (State.Running, Action.stop): State.Stopped,
    (State.Running, Action.pause): State.Paused,
    (State.Paused, Action.resume): State.Running,
    (State.Paused, Action.stop): State.Stopped,
}


if __name__ == '__main__':
    state_machine = StateMachine(State.Stopped)
    state_machine.step(Action.start)
    state_machine.step(Action.pause)
    state_machine.step(Action.resume)
    state_machine.step(Action.stop)
