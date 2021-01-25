class Building():
    def __init__(self):
        '''A building with ELLevator service (pun intended).

        Attributes:
             floor_list (list): floors in the building, from lowest to highest.
             self.cabins (list of instances of Cabin class): ELLevator cabins providing service in the building.
             potential_passengers (list of instances of Passenger class): people in the building.
             floors_up_pressed (list of items from floor_list): floors on which the button to go UP is pressed.
             floors_down_pressed (list of items from floor_list): floors on which the button to go DOWN is pressed.
        '''
        self.floor_list = range(1, 11)
        # self.floor_list = ['Basement', 1, 'Mezzanine', 2, 3, 4, 'Penthouse']
        self.cabins = []
        self.potential_passengers = []
        self.floors_up_pressed = []
        self.floors_down_pressed = []


class Cabin():
    def __init__(self, id, building, current_floor=1, passenger_max=8):
        '''An ELLevator cabin.

        Attributes:
            id (str): cabin identifier.
            building (instance of Building class): building serviced by the cabin.
            served_floors (list): building floors serviced by the cabin.
            current_floor (item from served_floors): which floor the cabin is currently on.
            passenger_max (int): maximum cabin occupancy.
            passengers (list of instances of Passenger class): passengers inside the cabin.
            is_going_up (bool or None): True if the cabin is moving up, False if moving down, None if not moving
            stop_queue (list of items from served_floors): floors the (dispatched) cabin will move to, in order.
            buttons_pressed (list of items from served_floors): pressed floor buttons inside the cabin.
        '''
        self.id = id
        self.building = building
        self.served_floors = self.building.floor_list
        self.current_floor = current_floor
        self.passenger_max = passenger_max
        self.passengers = []
        self.is_going_up = None
        self.stop_queue = []
        self.buttons_pressed = []
        self.building.cabins.append(self)

    def order_floors(self, floors_to_order, floor_order, lowest_to_highest):
        if lowest_to_highest:
            return [f for f in floor_order if f in floors_to_order]
        else:
            return [f for f in floor_order[::-1] if f in floors_to_order]

    def pick_direction(self, up_requests, down_requests):
        if len(up_requests + down_requests) == 0:
            return None
        elif len(down_requests) == 0:
            return True
        elif len(up_requests) == 0:
            return False
        else:
            return abs(self.served_floors.index(up_requests[0]) - self.served_floors.index(self.current_floor)) <= abs(
                self.served_floors.index(down_requests[0]) - self.served_floors.index(self.current_floor))

    def dispatch(self):
        while len(self.stop_queue) == 0:
            # Check for pick-up requests
            up_requests = self.order_floors(floors_to_order=self.building.floors_up_pressed,
                                            floor_order=self.served_floors,
                                            lowest_to_highest=True)

            down_requests = self.order_floors(floors_to_order=self.building.floors_down_pressed,
                                              floor_order=self.served_floors,
                                              lowest_to_highest=False)

            # Pick direction and create queue
            self.is_going_up = self.pick_direction(up_requests=up_requests, down_requests=down_requests)

            if self.is_going_up is None:
                print('\nCabin {} is standing by - no requests left to serve.\n'.format(self.id))
                break
            elif self.is_going_up:
                print('\nDispatching cabin {} to travel up.'.format(self.id))
                self.stop_queue.extend(up_requests)
            else:
                print('\nDispatching cabin {} to travel down.'.format(self.id))
                self.stop_queue.extend(down_requests)

            # Serve all stops in the queue
            while len(self.stop_queue) > 0:
                print('Floor(s) served next: {} --- Passengers: {}'.format(
                    self.stop_queue, [p.name for p in self.passengers]))

                # Move cabin to next stop
                stop = self.stop_queue[0]
                print('\nCabin {} goes to floor {}.'.format(self.id, stop))
                self.current_floor = stop

                # Remove stop from queue + reset pressed buttons (in cabin + on floor), if any
                self.stop_queue.remove(stop)

                if stop in self.buttons_pressed:
                    self.buttons_pressed.remove(stop)

                if self.is_going_up and stop in self.building.floors_up_pressed:
                    self.building.floors_up_pressed.remove(stop)
                elif not self.is_going_up and stop in self.building.floors_down_pressed:
                    self.building.floors_down_pressed.remove(stop)

                # Passengers exit
                passengers_to_exit = [p for p in self.passengers if p.destination_floor == stop]

                for p in passengers_to_exit:
                    p.exit_cabin()

                # Passengers enter
                passengers_to_enter = [p for p in self.building.potential_passengers if (
                        p.current_floor == stop
                        and p.destination_floor is not None
                        and p.destination_floor != p.current_floor
                        and p.destination_floor in self.served_floors
                        and p.is_going_up == self.is_going_up
                        and p.cabin is None
                )]

                for p in passengers_to_enter:
                    if len(self.passengers) < self.passenger_max:
                        p.enter_cabin(cabin=self)
                        p.select_floor()
                    else:
                        print('{} can not enter - cabin {} is full.'.format(p.name, self.id))
                        p.call_ellevator()

            else:
                print('Cabin {} is ready to serve more passengers.\n'.format(self.id))
                print('Next Floor(s): {} --- Passengers: {}'.format(self.stop_queue, [p.name for p in self.passengers]))
                continue


class Passenger():
    def __init__(self, name, building, current_floor, destination_floor):
        '''A person likely not thinking about ELLevator algorithms - yet!

        Attributes:
            name (str): the person's name.
            building (instance of Building class): building the person is in.
            current_floor (item from building.floor_list): floor the person is on while not in a cabin.
            destination_floor (item from building.floor_list or None): floor the person would like to go to.
            cabin (instance of Cabin class or None): ELLevator cabin the person is in.
            is_going_up (bool or None): True if the person is traveling up, False if down, None if not traveling
        '''
        self.name = name
        self.building = building
        self.current_floor = current_floor
        self.destination_floor = destination_floor
        self.cabin = None
        self.is_going_up = None
        self.building.potential_passengers.append(self)
        if self.current_floor != self.destination_floor and self.destination_floor is not None:
            self.call_ellevator()
        else:
            print('{} is already on the floor they want to be and not calling an ELLevator.'.format(self.name))

    def call_ellevator(self):  # TODO: add error handling of destination floor being empty
        self.is_going_up = self.building.floor_list.index(
            self.destination_floor) - self.building.floor_list.index(self.current_floor) > 0  # Bool
        if self.is_going_up:
            if self.current_floor not in self.building.floors_up_pressed:
                print('{} presses the UP button on floor {}.'.format(self.name, self.current_floor))
                self.building.floors_up_pressed.append(self.current_floor)
            else:
                print('{} sees the UP button on floor {} is already pressed.'.format(self.name, self.current_floor))
        else:
            if self.current_floor not in self.building.floors_down_pressed:
                print('{} presses the DOWN button on floor {}.'.format(self.name, self.current_floor))
                self.building.floors_down_pressed.append(self.current_floor)
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
                self.cabin.stop_queue = self.cabin.order_floors(floors_to_order=self.cabin.stop_queue,
                                                                floor_order=self.cabin.served_floors,
                                                                lowest_to_highest=self.cabin.is_going_up)

    def exit_cabin(self):
        print('{} exits.'.format(self.name))
        self.current_floor = self.cabin.current_floor
        self.cabin.passengers.remove(self)
        self.cabin = None
        self.destination_floor = None

# TODO: add class instance checks?