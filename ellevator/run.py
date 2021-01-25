import random

from ellevator_parts import Building, Cabin, Passenger

floor_list_possibilities = [
    range(1, 11),
    [i for i in range(1, 51) if i != 13],
    ['A', 'B', 'C', 'D', 'E'],
    ['Basement', 1, 'Mezzanine', 2, 3, 4, 'Penthouse']
]

south_park = ['Cartman', 'Stan', 'Kyle', 'Kenny', 'Butters']
star_wars = ['Luke Skywalker', 'Han Solo', 'Princess Leia', 'Darth Vader', 'Jabba the Hut']


def main():
    characters = south_park

    building = Building(floor_list=random.choice(floor_list_possibilities))

    the_only_cabin = Cabin(id='ELL',
                           building=building,
                           current_floor=random.choice(building.floor_list),
                           passenger_max=5)

    passengers = [Passenger(name=character,
                            building=building,
                            current_floor=random.choice(building.floor_list),
                            destination_floor=random.choice(building.floor_list))
                  for character in characters]

    the_only_cabin.dispatch()

    # Manual Ellevator call
    passengers[-1].call_ellevator()


if __name__ == '__main__':
    main()
