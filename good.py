class Good():
    def __init__(self, name, base_price):
        self._name = name

        if base_price <= 0:
            raise ValueError("Invalid price of good")
        self.base_price = base_price

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Good):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)