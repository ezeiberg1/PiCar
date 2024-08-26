from picar import PiCar
car = PiCar(mock_car=True)
print('getting reading')
print(f'Distance reading: {car.read_distance()}')
