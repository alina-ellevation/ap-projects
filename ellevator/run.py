from ellevator_parts import Building, Cabin, Passenger

tower = Building()

cabin_1 = Cabin(id='A', building=tower, current_floor=5, passenger_max=4)

alina = Passenger('Alina', tower, 2, 5)
greg = Passenger('Greg', tower, 1, 10)
livy = Passenger('Livy', tower, 4, 8)
sophie = Passenger('Sophie', tower, 6, 2)
yiayia = Passenger('Yiayia', tower, 8, 2)

cabin_1.dispatch()