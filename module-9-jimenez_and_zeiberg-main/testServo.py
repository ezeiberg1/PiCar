from picar import PiCar
from time import sleep
car = PiCar(mock_car = False)
#car.configure_swivel_servo_positions(-10, 0, 10)
car.set_swivel_servo(-10)
print("0")
sleep(3)
car.set_swivel_servo(0)
print("5")
sleep(3)
car.set_swivel_servo(10)
print("10")
sleep(3)
