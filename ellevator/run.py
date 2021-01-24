from ellevator_parts import Building, Cabin, Passenger

tower = Building()

# TODO: random passenger creation

alina = Passenger('Alina', tower, 1, 10)
greg = Passenger('Greg', tower, 1, 5)
yiayia = Passenger('Yiayia', tower, 2, 4)
papou = Passenger('Papou', tower, 2, 3)
livy = Passenger('Livy', tower, 10, 5)
sophie = Passenger('Sophie', tower, 10, 7)

cabin_1 = Cabin(id='A', building=tower, floor_to_start=1, floors_not_served=[])
cabin_1.move()