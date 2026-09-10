class City():
    def __init__(self, name):
        self.name = name
        self.inventory = {}

    def add_goods(self, good, quantity):
        if quantity <= 0:
            return False
        
        if good not in self.inventory:
            self.inventory[good] = quantity
            return True
        else:
            self.inventory[good] += quantity
            return True

    def remove_goods(self, good, quantity):
        if good not in self.inventory:
            return False

        if quantity <= 0:
            return False

        if quantity > self.inventory[good]:
            return False

        self.inventory[good] -= quantity
        if self.inventory[good] == 0:
            del self.inventory[good]
        return True