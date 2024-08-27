# Controlling a Raspberry PiCar - 2022

This project uses various techniques involving different sensors installed on the PiCar to accomplish 3 main objectives. The first objective is control. This objective focuses on design- ing a control system for the PiCar motor. Another focus of this objective was to determine the response time, overshoot, and steady state error for the system trying to travel at 3 RPS. The AD converter plays a major role in determining the speed of the PiCar in “real time”. It observes a rotating wheel that’s composed of black and white sections to determine the rotations per seconds of the given system. The AD converter converts the analog system to a binary format that could be understood by the Raspberry i. A program was created to determine the rotations per seconds based on the transitions counted in the time interval.

The second objective was movement. This objective focuses on the Picar getting as close to a blue object without hitting it, starting from a distance of at least 20 feet. The other part of this objective is to get as close to the object within a certain time (less than 10 seconds). For this objective, an ultrasonic sensor was used, which helped determine the distance between the Picar and an object in front of the car. The other sensor used for this objective was the PiCamera, used to identify blue objects. This code also controlled the servo motors of the car to direct to the desired object.

The third objective was for the car to start at a specific point and travel to an object (we chose a blue recycling container) in a straight line with varying distance determined by the instructor. The car was objected with getting as close to the object without hitting it while traveling at a set speed.
