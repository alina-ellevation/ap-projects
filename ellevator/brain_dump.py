def call_ellevator(self):
    if self.cabin is not None:
        print('{} can not call an ELLevator - already in one (cabin {}).'.format(self.name, self.cabin))

    elif self.current_floor == self.destination_floor:
        print('{} does not need to call an ELLevator - already on desired floor.'.format(self.name))


def enter_cabin(self, cabin):
    if self.cabin is not None:
        print('{} can not enter - already in cabin {}.'.format(self.name, self.cabin.id))

    elif self.current_floor == self.destination_floor:
        print('{} did not enter cabin {} - already on desired floor.'.format(self.name, cabin.id))

    elif self.current_floor != cabin.current_floor:
        print('{} is on floor {} - can not enter cabin {} on floor {}.'.format(
            self.name, self.current_floor, cabin.id, cabin.current_floor))

    elif self.destination_floor not in cabin.served_floors:
        print('{} did not enter - cabin {} does not serve floor {}.'.format(
            self.name, cabin.id, self.destination_floor))

    elif self.is_going_up != cabin.is_going_up:
        print('{} did not enter - cabin {} is going in the opposite direction.'.format(self.name, cabin.id))


def exit_cabin(self):
    if self.cabin == None:
        print('{} is not in a cabin at this time - can not exit.'.format(self.name))

    elif self.cabin.current_floor != self.destination_floor:
        print('{} has not reached floor {} yet - {} is staying in the Ellevator.'.format(
            self.cabin.id, self.destination_floor, self.name))