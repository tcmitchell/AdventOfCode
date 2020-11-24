package main

import (
	"../intcode"
	"fmt"
	"log"
)

const (  // iota is reset to 0
	NORTH = iota  // NORTH == 0
	EAST = iota   // EAST == 1
	SOUTH = iota  // SOUTH == 2
	WEST = iota   // WEST == 3
)


type Point struct {
	x, y int
}

//type Tile struct {
//	Location Point
//	Color int
//	Painted bool
//}

//type Hull struct {
//	Tiles map[Point]Tile
//}

type Robot struct {
	Location Point
	// TODO: how to represent direction
	Direction int
}

func turnLeft(robot Robot) {
	switch robot.Direction {
	case NORTH:
		robot.Direction = WEST
	case EAST:
		robot.Direction = NORTH
	case SOUTH:
		robot.Direction = EAST
	case WEST:
		robot.Direction = SOUTH
	}
}

func turnRight(robot Robot) {
	switch robot.Direction {
	case NORTH:
		robot.Direction = EAST
	case EAST:
		robot.Direction = SOUTH
	case SOUTH:
		robot.Direction = WEST
	case WEST:
		robot.Direction = NORTH
	}
}

func moveForward(robot Robot, steps int) {
	switch robot.Direction {
	case NORTH:
		robot.Location.y -= 1
	case EAST:
		robot.Location.x += 1
	case SOUTH:
		robot.Location.y += 1
	case WEST:
		robot.Location.x -= 1
	}
}

// TODO: implement turnRobot
func turnRobot(robot Robot, direction int) {
	// 0 = turn left
	// 1 = turn right
	switch direction {
	case 0:
		turnLeft(robot)
	case 1;
		turnRight(robot)
	default:
		log.Fatalf("Unknown direction %d", direction)
	}
	// move forward 1 step
	moveForward(robot, 1)
}

func p1RunInterpreter(interpreter *intcode.Interpreter) {
	err := interpreter.Run()
	if err != nil {
		log.Fatal(err)
	}
}

// TODO: Connect input to robot's camera
func p1DummyInput(inChan chan int) {
	for {
		inChan <- 0
	}
}

func part1(progFile string) error {
	robot := Robot{}
	fmt.Printf("Robot: %d, %d; %d", robot.Location.x, robot.Location.y, robot.Direction)
	inChan := make(chan int)
	outChan := make(chan int)
	interpreter, err := intcode.NewInterpreter(progFile, inChan, outChan, "robot")
	if err != nil {
		return err
	}
	go p1DummyInput(inChan)
	go p1RunInterpreter(interpreter)
	for {
		paintColor, ok := <-outChan
		if ! ok {
			log.Println("No more output")
			break
		}
		log.Printf("Paint color: %d", paintColor)
		direction, ok := <-outChan
		if ! ok {
			log.Println("No more output (direction)")
			break
		}
		log.Printf("Direction: %d", direction)
	}
	return nil
}

func main() {
	fmt.Println("Hello, World!")
	fmt.Printf("North: %d\n", NORTH)
	err := part1("input.txt")
	if err != nil {
		log.Fatal(err)
	}
}
