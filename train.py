class Train():
    def __init__(self, name, locomotive, cars):
        self.name = name
        self.locomotive = locomotive

        if not self._is_car_quantity_valid(cars):
            raise ValueError("Invalid number of cars")
        
        self.cars = cars
        self.owned_by = None
        self.stops = []
        self.current_city = None
        self.distance_on_connection = 0
        self.route = None
        self.current_connection_index = None

    def set_cars(self, quantity):
        if self._is_car_quantity_valid(quantity):
            self.cars = quantity
            return True
        else:
            return False

    def _is_car_quantity_valid(self, quantity):
        if 1 <= quantity <= self.locomotive.max_number_of_cars:
            return True
        else:
            return False

    def move(self):
        if self.route is None:
            return False

        if self.current_city in self.stops:
            return False

        if self.current_connection_index == len(self.route) - 1 and self.route[self.current_connection_index].distance == self.distance_on_connection:
            return False

        unused_distance = self.locomotive.speed
        while unused_distance > 0:
            connection_distance_left = self.route[self.current_connection_index].distance - self.distance_on_connection

            distance_to_move = min(unused_distance, connection_distance_left)

            self.distance_on_connection += distance_to_move
            unused_distance -= distance_to_move

            if self.distance_on_connection < self.route[self.current_connection_index].distance:
                return True
            else:
                if self.current_connection_index < len(self.route) - 1:
                    city = self.route[self.current_connection_index].end
                    self.current_connection_index += 1
                    self.distance_on_connection = 0
                    if city in self.stops:
                        self.current_city = city
                        return True
                    else:
                        continue
                else:
                    self.current_city = self.route[self.current_connection_index].end
                    return True
        return True

    def assign_route(self, route):
        if len(route) == 0:
            return False
        
        for i in range(len(route) - 1):
            end = route[i].end
            start = route[i + 1].start
            if end != start:
                return False

        self.route = route
        self.current_connection_index = 0
        self.distance_on_connection = 0
        return True

    def depart(self):
        self.current_city = None