import genix


class UISlider(genix.UIContainer):
    """
    An component that will be implemented in a later version of Genix
    """
    def __init__(self):
        super().__init__()
        self.add_constraint(genix.RelativeWidth(0.1))
        self.add_constraint(genix.RelativeHeight(0.01))
        self.add_constraint(genix.CenterX())
        self.add_constraint(genix.CenterY())

    def slide_element(self):
        pass
