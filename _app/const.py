class Const():
    def __init__(self):
        self.passthrough = 0        # no template tags
        self.singleton = 1          # lookup in the root of config and substution
        self.convert_to_array = 2   # lookup in a list
