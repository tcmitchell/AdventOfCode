package main

import (
	"../intcode"
	"fmt"
	"log"
)

type Point struct {
	x, y int
}

type Cabinet struct {
	Score    int
	Screen   map[Point]int
	Ball     Point
	Paddle   Point
	Joystick int
}

func (cabinet *Cabinet) Init() {
	cabinet.Screen = make(map[Point]int)
}

func (cabinet *Cabinet) SetTile(x, y, t int) {
	if x == -1 && y == 0 {
		// Special location for the current score display
		cabinet.Score = t
	} else {
		cabinet.Screen[Point{x, y}] = t
		switch t {
		case 3:
			cabinet.Paddle = Point{x, y}
		case 4:
			// Record the ball position for paddle movement
			cabinet.Ball = Point{x, y}
		}
	}
}

func (cabinet *Cabinet) PrintScreen() {
	for y := 0; y < 20; y++ {
		for x := 0; x < 44; x++ {
			switch cabinet.Screen[Point{x, y}] {
			case 0:
				fmt.Print(" ")
			case 1:
				fmt.Print("|")
			case 2:
				fmt.Print("B")
			case 3:
				fmt.Print("-")
			case 4:
				fmt.Print("*")
			}
		}
		fmt.Println()
	}
}

// Given the new ball position set the joystick to move the paddle
func (cabinet *Cabinet) SetJoystick(x, y int) {
	// Compute intercept with paddle row
	// Move paddle as needed
	if y > cabinet.Ball.y {
		// Ball is descending
		stepsToPaddle := cabinet.Paddle.y - y - 1
		paddleIntercept := 0
		if x < cabinet.Ball.x {
			paddleIntercept = x - stepsToPaddle
			if paddleIntercept < 1 {
				paddleIntercept = 1
			}
		} else {
			paddleIntercept = x + stepsToPaddle
			if paddleIntercept > 43 {
				paddleIntercept = 43
			}
		}
		log.Printf("Intercept = %d", paddleIntercept)
		// Now move towards intercept
		if cabinet.Paddle.x < paddleIntercept {
			cabinet.Joystick = 1
		} else if cabinet.Paddle.x > paddleIntercept {
			cabinet.Joystick = -1
		} else {
			cabinet.Joystick = 0
		}
	} else {
		// Ball is ascending, move towards ball
		if cabinet.Paddle.x < x {
			cabinet.Joystick = 1
		} else if cabinet.Paddle.x > x {
			cabinet.Joystick = -1
		} else {
			cabinet.Joystick = 0
		}
	}
}

func p1HandleOutput(ch chan int, cabinet *Cabinet) {
	// Output comes in groups of three
	for {
		xCoord, ok := <-ch
		if !ok {
			break
		}
		yCoord, ok := <-ch
		if !ok {
			break
		}
		tileId, ok := <-ch
		if !ok {
			break
		}
		// Process the triple
		log.Printf("%d, %d gets %d\n", xCoord, yCoord, tileId)
		cabinet.SetTile(xCoord, yCoord, tileId)
	}
	log.Printf("Channel closed")
}

func runInterpreter(interpreter *intcode.Interpreter) {
	err := interpreter.Run()
	if err != nil {
		log.Fatal(err)
	}
}

func part1(programFile string) {
	var cabinet Cabinet
	cabinet.Init()
	outChan := make(chan int)
	interpreter, err := intcode.NewInterpreter(programFile, nil, outChan, "Part 1")
	if err != nil {
		log.Fatal(err)
	}
	go runInterpreter(interpreter)
	p1HandleOutput(outChan, &cabinet)
	log.Printf("Screen has %d tiles", len(cabinet.Screen))
	blockCount := 0
	for _, v := range cabinet.Screen {
		if v == 2 {
			blockCount += 1
		}
	}
	fmt.Printf("Part 1: %d\n", blockCount)
	cabinet.PrintScreen()
}

func p2DrainOutput(ch chan int, cabinet *Cabinet) bool {
	// Output comes in groups of three
	for {
		select {
		case xCoord, ok := <-ch:
			if ok {
				yCoord, ok := <-ch
				if !ok {
					break
				}
				tileId, ok := <-ch
				if !ok {
					break
				}
				log.Printf("%d, %d gets %d\n", xCoord, yCoord, tileId)
				if tileId == 4 {
					cabinet.SetJoystick(xCoord, yCoord)
				}
				// Process the triple
				cabinet.SetTile(xCoord, yCoord, tileId)
			} else {
				log.Printf("Output channel closed")
				return false
			}
		default:
			fmt.Println("Nothing on out channel")
			return true
		}
	}
}

func p2ProvideInput(inChan, outChan chan int, cabinet *Cabinet) {
	ok := p2DrainOutput(outChan, cabinet)
	if !ok {
		return
	}
	cabinet.PrintScreen()
	log.Printf("Sending joystick %d", cabinet.Joystick)
	inChan <- cabinet.Joystick
}

func part2(programFile string) {
	var cabinet Cabinet
	cabinet.Init()
	outChan := make(chan int, 5000)
	inChan := make(chan int, 1)
	interpreter, err := intcode.NewInterpreter(programFile, inChan, outChan, "Part 1")
	if err != nil {
		log.Fatal(err)
	}
	// Insert 2 quarters
	interpreter.SetMemoryLocation(0, 2)
	interpreter.SetInputFunction(func(ch chan int) {
		p2ProvideInput(ch, outChan, &cabinet)
	})
	runInterpreter(interpreter)
	p2DrainOutput(outChan, &cabinet)
	cabinet.PrintScreen()
	fmt.Printf("Part 2: %d\n", cabinet.Score)
}

func main() {
	//fmt.Print("Hello, World!")
	programFile := "input.txt"
	part1(programFile)
	part2(programFile)
}
