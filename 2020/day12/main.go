package main

import (
	"../aoc"
	"fmt"
	"log"
	"strconv"
)

var East = 0
var South = 90
var West = 180
var North = 270

func intAbs(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

type Command struct {
	Cmd string
	Arg int
}

func (c Command) String() string {
	return fmt.Sprintf("%s%d", c.Cmd, c.Arg)
}

func NewCommand(line string) (Command, error) {
	cmd := line[0:1]
	arg, err := strconv.Atoi(line[1:])
	if err != nil {
		return Command{}, err
	}
	return Command{cmd, arg}, nil
}

type Interpreter func(s *Ship, command Command) error

type Ship struct {
	X, Y                 int
	Direction            int
	WaypointX, WaypointY int
}

func (s *Ship) String() string {
	return fmt.Sprintf("%d, %d / %d / Waypoint %d, %d", s.X, s.Y, s.Direction, s.WaypointX, s.WaypointY)
}

func (s *Ship) ManhattanDistance(x, y int) int {
	return intAbs(s.X-x) + intAbs(s.Y-y)
}

func (s *Ship) TurnLeft(amount int) {
	//log.Printf("TurnLeft from %d", s.Direction)
	d := s.Direction - amount
	// Keep direction in range 0 <= Direction <= 270
	for ; d < 0; d += 360 {
	}
	s.Direction = d
	//log.Printf("TurnLeft to %d", s.Direction)
}

func (s *Ship) TurnRight(amount int) {
	//log.Printf("TurnRight from %d by %d", s.Direction, amount)
	d := s.Direction + amount
	// Keep direction in range 0 <= Direction <= 270
	for ; d >= 360; d -= 360 {
	}
	s.Direction = d
	//log.Printf("TurnRight to %d", s.Direction)
}

func (s *Ship) MoveForward(amount int) {
	switch s.Direction {
	case East:
		s.X += amount
	case South:
		s.Y -= amount
	case West:
		s.X -= amount
	case North:
		s.Y += amount
	default:
		panic(fmt.Errorf("unknown direction %v", s.Direction))
	}
}

func (s *Ship) TurnWaypointLeft(amount int) {
	switch amount {
	case 90:
		s.WaypointX, s.WaypointY = -s.WaypointY, s.WaypointX
	case 180:
		s.WaypointX, s.WaypointY = -s.WaypointX, -s.WaypointY
	case 270:
		s.TurnWaypointRight(90)
	default:
		panic(fmt.Errorf("unknown turn amount %d", amount))
	}
}

func (s *Ship) TurnWaypointRight(amount int) {
	switch amount {
	case 90:
		s.WaypointX, s.WaypointY = s.WaypointY, -s.WaypointX
	case 180:
		s.WaypointX, s.WaypointY = -s.WaypointX, -s.WaypointY
	case 270:
		s.TurnWaypointLeft(90)
	default:
		panic(fmt.Errorf("unknown turn amount %d", amount))
	}
}

func (s *Ship) MoveTowardWaypoint(amount int) {
	s.X += amount * s.WaypointX
	s.Y += amount * s.WaypointY
}

func (s *Ship) Move(interpreter Interpreter, command Command) error {
	return interpreter(s, command)
}

func p1Interpreter(s *Ship, command Command) error {
	switch command.Cmd {
	case "N":
		s.Y += command.Arg
	case "S":
		s.Y -= command.Arg
	case "E":
		s.X += command.Arg
	case "W":
		s.X -= command.Arg
	case "L":
		s.TurnLeft(command.Arg)
	case "R":
		s.TurnRight(command.Arg)
	case "F":
		s.MoveForward(command.Arg)
	default:
		return fmt.Errorf("unknown command %s", command.Cmd)
	}
	return nil
}

func loadCommands(filename string) ([]Command, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	commands := make([]Command, len(lines))
	for i, line := range lines {
		cmd, err := NewCommand(line)
		if err != nil {
			return nil, err
		}
		commands[i] = cmd
	}
	return commands, nil
}

func part1(filename string) (int, error) {
	commands, err := loadCommands(filename)
	if err != nil {
		return 0, err
	}
	startX, startY := 0, 0
	s := Ship{X: startX, Y: startY, Direction: East}
	for _, cmd := range commands {
		err = s.Move(p1Interpreter, cmd)
		if err != nil {
			return 0, err
		}
	}
	return s.ManhattanDistance(startX, startY), nil
}

func p2Interpreter(s *Ship, command Command) error {
	switch command.Cmd {
	case "N":
		s.WaypointY += command.Arg
	case "S":
		s.WaypointY -= command.Arg
	case "E":
		s.WaypointX += command.Arg
	case "W":
		s.WaypointX -= command.Arg
	case "L":
		s.TurnWaypointLeft(command.Arg)
	case "R":
		s.TurnWaypointRight(command.Arg)
	case "F":
		s.MoveTowardWaypoint(command.Arg)
	default:
		return fmt.Errorf("unknown command %s", command.Cmd)
	}
	//log.Printf("After command %s", command)
	//log.Printf("Ship: %s", s)
	return nil
}

func part2(filename string) (int, error) {
	commands, err := loadCommands(filename)
	if err != nil {
		return 0, err
	}
	startX, startY := 0, 0
	s := Ship{X: startX, Y: startY, Direction: East, WaypointX: 10, WaypointY: 1}
	for _, cmd := range commands {
		err = s.Move(p2Interpreter, cmd)
		if err != nil {
			return 0, err
		}
	}
	return s.ManhattanDistance(startX, startY), nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	//filename = "test-input2.txt"
	p1, err := part1(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d\n", p1)
	p2, err := part2(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}
