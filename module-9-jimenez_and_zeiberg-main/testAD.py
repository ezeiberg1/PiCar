from picar import PiCar
import time
car = PiCar(mock_car=True)
print(f'AD output from pin 0: {car.adc.read_adc(0)}')
