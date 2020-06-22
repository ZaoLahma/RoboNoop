from ..log.log import Log

class State:
    def __init__(self, state_name, state_func, ok_transition, fail_transition):
        self.state_name = state_name
        self.state_func = state_func
        self.ok_transition = ok_transition
        self.fail_transition = fail_transition

class StateHandler():
    def __init__(self, state_def, init_state):
        self.state_def = state_def
        self.transition_to(init_state)

    def get_state_func(self):
        return self.curr_state.state_func

    def transition_to(self, state_name):
        self.curr_state = None
        for state in self.state_def:
            if state.state_name == state_name:
                self.curr_state = state
                break
        if None == self.curr_state:
            Log.log("ERROR - Failed to look up next state: " + state_name)
        else:
            Log.log("State transition to " + self.curr_state.state_name)

    def transition(self, fail=False):
        next_state = self.curr_state.ok_transition
        if True == fail:
            next_state = self.curr_state.fail_transition
        self.transition_to(next_state)