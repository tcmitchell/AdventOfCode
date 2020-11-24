package main

import (
	"../intcode"
	"fmt"
	"log"
)

const ( // iota is reset to 0
	NORTH = iota // NORTH == 0
	EAST  = iota // EAST == 1
	SOUTH = iota // SOUTH == 2
	WEST  = iota // WEST == 3
)

type Point struct {
	x, y int
}

type Tile struct {
	Location Point
	Color    int
	Painted  bool
}

type Robot struct {
	Location Point
	// TODO: how to represent direction
	Direction       int
	inChan, outChan chan int
	Tiles           map[Point]*Tile
}

func turnLeft(robot *Robot) {
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

func turnRight(robot *Robot) {
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

func moveForward(robot *Robot, steps int) {
	switch robot.Direction {
	case NORTH:
		robot.Location.y -= steps
	case EAST:
		robot.Location.x += steps
	case SOUTH:
		robot.Location.y += steps
	case WEST:
		robot.Location.x -= steps
	}
}

// TODO: implement turnRobot
func turnRobot(robot *Robot, direction int) {
	// 0 = turn left
	// 1 = turn right
	switch direction {
	case 0:
		turnLeft(robot)
	case 1:
		turnRight(robot)
	default:
		log.Fatalf("Unknown direction %d", direction)
	}
	// move forward 1 step
	moveForward(robot, 1)
	log.Printf("Robot at %d, %d facing %d", robot.Location.x, robot.Location.y, robot.Direction)
}

// Paint the tile at the robot's current location with the given color.
func paintTile(robot *Robot, paintColor int) {
	if robot.Tiles == nil {
		robot.Tiles = make(map[Point]*Tile)
	}
	tile, ok := robot.Tiles[robot.Location]
	if !ok {
		tile = &Tile{robot.Location, 0, false}
		robot.Tiles[robot.Location] = tile
	}
	tile.Color = paintColor
	tile.Painted = true
	log.Printf("Painted %d, %d with %d", robot.Location.x, robot.Location.y, paintColor)
}

func currentTileColor(robot *Robot) int {
	if robot.Tiles == nil {
		robot.Tiles = make(map[Point]*Tile)
	}
	tile, ok := robot.Tiles[robot.Location]
	if !ok {
		tile = &Tile{robot.Location, 0, false}
		robot.Tiles[robot.Location] = tile
	}
	log.Printf("Tile %d, %d is %d", robot.Location.x, robot.Location.y, tile.Color)
	return tile.Color
}

func p1RunInterpreter(interpreter *intcode.Interpreter) {
	err := interpreter.Run()
	if err != nil {
		log.Fatal(err)
	}
}

// Connect input to robot's camera
func p1DummyInput(robot *Robot, ch chan int) {
	ok := p1DrainOutput(robot)
	if !ok {
		return
	}
	ch <- currentTileColor(robot)
	//select {
	//case ch <- currentTileColor(robot):
	////case ch <- 0:
	//default:
	//	//fmt.Println("Channel full. Discarding value")
	//}
}

// Read the output channel until it is drained, but not closed
func p1DrainOutput(robot *Robot) bool {
	for {
		select {
		case paintColor, ok := <-robot.outChan:
			if ok {
				log.Printf("Paint color: %d", paintColor)
				paintTile(robot, paintColor)
				direction, ok := <-robot.outChan
				if !ok {
					log.Println("No more output (direction)")
					break
				}
				log.Printf("Direction: %d", direction)
				turnRobot(robot, direction)
			} else {
				fmt.Println("Output channel closed!")
				return false
			}
		default:
			fmt.Println("Nothing on out channel")
			return true
		}
	}
}

func part1(progFile string) error {
	robot := Robot{}
	fmt.Printf("Robot: %d, %d; %d", robot.Location.x, robot.Location.y, robot.Direction)
	robot.inChan = make(chan int, 1)
	robot.outChan = make(chan int, 1000)
	interpreter, err := intcode.NewInterpreter(progFile, robot.inChan, robot.outChan, "robot")
	if err != nil {
		return err
	}
	interpreter.SetInputFunction(func (ch chan int) {
		p1DummyInput(&robot, ch)
	})
	//go p1DummyInput(&robot, robot.inChan)
	p1RunInterpreter(interpreter)
	p1DrainOutput(&robot)
	paintedCount := 0
	for _, tile := range robot.Tiles {
		if tile.Painted {
			paintedCount += 1
		}
	}
	// Correct answer is 2594
	fmt.Printf("Part 1: %d\n", paintedCount)
	return nil
}

func minInt(a, b int) int {
	if a < b {
		return a
	} else {
		return b
	}
}

func maxInt(a, b int) int {
	if a > b {
		return a
	} else {
		return b
	}
}

func p2PrintHull(robot *Robot) {
	var minX, maxX, minY, maxY int
	for _, tile := range robot.Tiles {
		fmt.Printf("Tile %d, %d\n", tile.Location.x, tile.Location.y)
		minX = minInt(tile.Location.x, minX)
		maxX = maxInt(tile.Location.x, maxX)
		minY = minInt(tile.Location.y, minY)
		maxY = maxInt(tile.Location.y, maxY)
	}
	fmt.Printf("Hull goes from %d -> %d and %d -> %d\n", minY, maxY, minX, maxX)
	for y := minY; y<=maxY; y++ {
		for x := minX; x<=maxX; x++ {
			pt := Point{x, y}
			tile, ok := robot.Tiles[pt]
			if ok {
				switch tile.Color {
				case 0:
					fmt.Print(".")
				case 1:
					fmt.Print("#")
				}
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println("")
	}
}

func part2(progFile string) error {
	robot := Robot{}
	fmt.Printf("Robot: %d, %d; %d", robot.Location.x, robot.Location.y, robot.Direction)
	robot.inChan = make(chan int, 1)
	robot.outChan = make(chan int, 1000)
	robot.Tiles = make(map[Point]*Tile)
	tile := &Tile{robot.Location, 1, false}
	robot.Tiles[robot.Location] = tile

	interpreter, err := intcode.NewInterpreter(progFile, robot.inChan, robot.outChan, "robot")
	if err != nil {
		return err
	}
	interpreter.SetInputFunction(func (ch chan int) {
		p1DummyInput(&robot, ch)
	})
	//go p1DummyInput(&robot, robot.inChan)
	p1RunInterpreter(interpreter)
	p1DrainOutput(&robot)
	paintedCount := 0
	for _, tile := range robot.Tiles {
		if tile.Painted {
			paintedCount += 1
		}
	}
	// Correct answer is AKERJFHK
	fmt.Printf("Part 2: %d\n", paintedCount)
	p2PrintHull(&robot)
	return nil
}

func main() {
	fmt.Println("Hello, World!")
	fmt.Printf("North: %d\n", NORTH)
	err := part1("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	err = part2("input.txt")
	if err != nil {
		log.Fatal(err)
	}
}
