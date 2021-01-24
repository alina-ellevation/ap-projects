class Building():
    def __init__(self):
        self.floor_list = range(1, 11)  # list of existing floors, from lowest to highest TODO: PH, Basement
        self.potential_passengers = []
        self.floors_up_pressed = []
        self.floors_down_pressed = []


class Cabin():
    def __init__(self, id, building, floor_to_start=10, floors_not_served=None):
        self.id = id
        self.building = building  # should be instance of Building class
        self.current_floor = floor_to_start
        self.served_floors = [f for f in self.building.floor_list if f not in floors_not_served]
        self.passenger_max = 5  # maximum amount of passengers allowed in cabin at the same time
        self.passengers = []
        self.stop_queue = []
        self.buttons_pressed = []

    def order_queue(self, floors, is_going_up):
        if is_going_up:
            return [f for f in self.served_floors if f in floors]
        else:
            return [f for f in self.served_floors[::-1] if f in floors]

    def move(self):
        print('\nELLevator is ready for dispatch!'.format(self.id,))
        while len(self.stop_queue) == 0:
            # PICK DIRECTION
            # If there are no requests, halt cabin.
            # If only one direction has requests, go in that direction
            # Otherwise, pick direction for which first stop is closer to the cabin location (if equidistant, go up)
            up_requests = self.order_queue(floors=self.building.floors_up_pressed, is_going_up=True)
            down_requests = self.order_queue(floors=self.building.floors_down_pressed, is_going_up=False)

            if len(up_requests + down_requests) == 0:
                print('\nWaiting for new passengers.'.format(self.id))
                break
            elif len(down_requests) == 0:
                self.is_going_up = True
            elif len(up_requests) == 0:
                self.is_going_up = False
            else:
                self.is_going_up = abs(
                    self.served_floors.index(up_requests[0]) - self.served_floors.index(self.current_floor)) <= abs(
                    self.served_floors.index(down_requests[0]) - self.served_floors.index(self.current_floor))

            if self.is_going_up:
                self.stop_queue.extend(up_requests)
                print('\nCabin {} is going up.'.format(self.id))
            else:
                self.stop_queue.extend(down_requests)
                print('\nCabin {} is going down.'.format(self.id))

            # SERVE EACH STOP
            while len(self.stop_queue) > 0:
                print('Next up: {}'.format(self.stop_queue))  # TODO: For Troubleshooting, remove
                stop = self.stop_queue[0]  # Pick first stop in queue

                print('\nCabin {} goes to floor {}.'.format(self.id, stop))
                self.current_floor = stop  # Move cabin
                self.stop_queue.remove(stop)  # Remove stop from queue

                # Un-press floor button inside cabin
                if stop in self.buttons_pressed:
                    self.buttons_pressed.remove(stop)

                # Un-press UP/DOWN button on floor
                if self.is_going_up and stop in self.building.floors_up_pressed:
                    self.building.floors_up_pressed.remove(stop)
                elif not self.is_going_up and stop in self.building.floors_down_pressed:
                    self.building.floors_down_pressed.remove(stop)
                else:
                    pass

                # Passengers exit
                passengers_to_exit = [p for p in self.passengers if p.destination_floor == stop]
                for p in passengers_to_exit:
                    p.exit_cabin()

                # Passengers enter
                passengers_to_enter = [p for p in self.building.potential_passengers if (
                    p.current_floor == stop
                    and p.destination_floor in self.served_floors
                    and p.destination_floor != p.current_floor
                    and p.is_going_up == self.is_going_up
                    and p.cabin is None
                )]
                for p in passengers_to_enter:
                    if len(self.passengers) < self.passenger_max:
                        p.enter_cabin(cabin=self)
                        p.select_floor()
                        self.stop_queue = self.order_queue(floors=self.stop_queue, is_going_up=self.is_going_up)
                    else:
                        print('{} can not enter - cabin {} is full.'.format(p.name, self.id))  # TODO: call another Ellevator

            else:
                print('\nPassengers: {} - Stop Queue: {}'.format([p.name for p in self.passengers], self.stop_queue))
                print('Cabin {} is ready to serve more passengers.\n'.format(self.id))
                continue


class Passenger():
    cabin = None

    def __init__(self, name, building, orig_floor, destination_floor):
        self.name = name
        self.building = building
        self.building.potential_passengers.append(self)
        self.current_floor = orig_floor  # floor while not in cabin
        self.destination_floor = destination_floor
        self.cabin = None
        self.is_going_up = self.building.floor_list.index(
            self.destination_floor) - self.building.floor_list.index(self.current_floor) > 0  # Bool
        if self.current_floor != self.destination_floor:
            self.call_ellevator()

    def call_ellevator(
            self):  # TODO: change_mind_about_direction=False (self.is_traveling_up = not self.is_traveling_up)
        if self.is_going_up:
            if self.current_floor not in self.building.floors_up_pressed:
                self.building.floors_up_pressed.append(self.current_floor)
                print('{} has pressed the UP button on floor {}.'.format(self.name, self.current_floor))
            else:
                print('{} sees the UP button on floor {} is already pressed.'.format(self.name, self.current_floor))
        else:
            if self.current_floor not in self.building.floors_down_pressed:
                self.building.floors_down_pressed.append(self.current_floor)
                print('{} has pressed the DOWN button on floor {}.'.format(self.name, self.current_floor))
            else:
                print('{} sees the DOWN button on floor {} is already pressed.'.format(self.name, self.current_floor))

    def enter_cabin(self, cabin):
        print('{} enters.'.format(self.name))
        cabin.passengers.append(self)
        self.cabin = cabin
        if len(cabin.passengers) == cabin.passenger_max:
            print('Cabin {} is now full.'.format(cabin.id))

    def select_floor(self):
        if self.destination_floor in self.cabin.buttons_pressed:
            print('The floor {} button is already pressed.'.format(self.destination_floor))
        else:
            print('{} presses the floor {} button.'.format(self.name, self.destination_floor))
            self.cabin.buttons_pressed.append(self.destination_floor)
            if self.destination_floor not in self.cabin.stop_queue:
                self.cabin.stop_queue.append(self.destination_floor)

    def exit_cabin(self):
        print('{} exits.'.format(self.name))
        self.cabin.passengers.remove(self)
        self.current_floor = self.cabin.current_floor
        self.cabin = None

# TODO: add class instance checks?
