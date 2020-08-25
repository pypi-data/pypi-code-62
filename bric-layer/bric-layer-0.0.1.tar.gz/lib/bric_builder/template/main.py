# main calculation flow
class Main:
    def __init__(self, layer):
        self.layer = layer

        # These use lambdas, so that there's no infinite recursion problem if they call each other
        self.layer.current.consts = self.layer.current.BricConsts()
        self.layer.current.get_params = lambda: self.layer.current.BricParams(self.layer)
        self.layer.current.get_calculations = lambda: self.layer.current.BricCalculations(self.layer)
        self.layer.current.get_filters = lambda: self.layer.current.BricFilters(self.layer)

    def assemble(self):
        return
