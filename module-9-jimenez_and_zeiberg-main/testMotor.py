from picar import PiCar
from time import sleep
car = PiCar(mock_car=True)
car.set_motor(30)
print("30")
sleep(2)
car.set_motor(70)
print("70")
sleep(2)
car.set_motor(0)
