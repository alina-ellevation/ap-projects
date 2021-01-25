import random

from ellevator_parts import Building, Cabin, Passenger

tower = Building()

the_only_cabin = Cabin(id='A', building=tower, current_floor=1, passenger_max=2)

south_park_characters = ['Cartman', 'Stan', 'Kyle', 'Kenny', 'Butters']
star_wars_characters = ['Luke Skywalker', 'Han Solo', 'R2D2', 'Darth Vader', 'Jabba the Hut']

passengers = [Passenger(character, tower, random.choice(tower.floor_list), random.choice(tower.floor_list))
              for character in south_park_characters]

the_only_cabin.dispatch()