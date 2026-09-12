class Good():
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Good):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)