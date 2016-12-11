#!/usr/bin/env python

import time

print 'Hello, World!'

with open('input.txt', 'rb') as f:
    data = f.read()

print len(data)

commands = data.split(',')
commands = [c.strip() for c in commands]
commands = [(c[0], int(c[1:])) for c in commands]
print len(commands)
for i in range(25):
    print commands[i]

class Direction(object):
    North = 0
    East = 1
    South = 2
    West = 3

class Robot(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.North

    def move(self, count):
        if self.direction == Direction.North:
            self.y += count
        elif self.direction == Direction.South:
            self.y -= count
        elif self.direction == Direction.East:
            self.x += count
        elif self.direction == Direction.West:
            self.x -= count
        else:
            raise Exception("Unknown Direction")

    def turn(self, direction):
        if direction == 'L':
            self.turnLeft()
        elif direction == 'R':
            self.turnRight()
        else:
            raise Exception("Turn unknown direction")

    def turnLeft(self):
        if self.direction == Direction.North:
            self.direction = Direction.West
        elif self.direction == Direction.South:
            self.direction = Direction.East
        elif self.direction == Direction.East:
            self.direction = Direction.North
        elif self.direction == Direction.West:
            self.direction = Direction.South
        else:
            raise Exception("turnLeft Unknown Direction")

    def turnRight(self):
        if self.direction == Direction.North:
            self.direction = Direction.East
        elif self.direction == Direction.South:
            self.direction = Direction.West
        elif self.direction == Direction.East:
            self.direction = Direction.South
        elif self.direction == Direction.West:
            self.direction = Direction.North
        else:
            raise Exception("turnLeft Unknown Direction")

robot = Robot()
for (direction, count) in commands:
    print direction, count
    robot.turn(direction)
    robot.move(count)
    print 'Robot:', robot.x, robot.y
    # time.sleep(1)
