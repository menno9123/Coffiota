# machine states

from state import State


class Splash_state(State):
    def __init__(self):
        print("Splash initiated")
        self.splash = True
        self.selection = False
        self.payment = False
        self.brewing = False
    def on_event(self, event):
        if event == "To selection":
            return Selection_state()
        elif event == "To splash":
            return Splash_state()
        return self


class Selection_state(State):
    
    def __init__(self):
        print("Selection initiated")
        self.splash = False
        self.selection = True
        self.payment = False
        self.brewing = False
    def on_event(self, event):
        if event == "To payment":
            return Payment_state()
        elif event == "To splash":
            return Splash_state() 
        return self
    
class Payment_state(State):
    
    def __init__(self):
        print("Payment initiated")
        self.payment = True
        self.selection = False
        self.splash = False
        self.brewing = False
    def on_event(self, event):
        if event == "To brewing":
            return Brewing_state()
        elif event == "To splash":
            return Splash_state()
        return self
    
class Brewing_state(State):
    
    def __init__(self):
        print("Brewing initiated")
        self.payment = False
        self.selection = False
        self.splash = False
        self.brewing = True

    def on_event(self, event):
        if event == "return home":
            return Selection_state()

        return self
    