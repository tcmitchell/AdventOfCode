package main

import (
	"../intcode"
	"fmt"
	"log"
	"sync"
)

type Point struct {
	x, y int
}

func p1HandleOutput(wg *sync.WaitGroup, ch chan int, screen *map[Point]int) {
	// Output comes in groups of three
	for {
		xCoord, ok := <- ch
		if ! ok {
			break
		}
		yCoord, ok := <- ch
		if ! ok {
			break
		}
		tileId, ok := <- ch
		if ! ok {
			break
		}
		// Process the triple
		log.Printf("%d, %d gets %d\n", xCoord, yCoord, tileId)
		(*screen)[Point{xCoord, yCoord}] = tileId
	}
	log.Printf("Channel closed")
	wg.Done()
}

func part1(programFile string) {
	var wg sync.WaitGroup
	outChan := make(chan int)
	gameScreen := make(map[Point]int)
	interpreter, err := intcode.NewInterpreter(programFile, nil, outChan, "Part 1")
	if err != nil {
		log.Fatal(err)
	}
	wg.Add(1)
	go p1HandleOutput(&wg, outChan, &gameScreen)
	err = interpreter.Run()
	if err != nil {
		log.Fatal(err)
	}
	// Wait until all the output has been processed
	wg.Wait()
	log.Printf("Screen has %d tiles", len(gameScreen))
	blockCount := 0
	for _, v := range gameScreen {
		if v == 2 {
			blockCount += 1
		}
	}
	fmt.Printf("Part 1: %d\n", blockCount)
}

func main() {
	//fmt.Print("Hello, World!")
	part1("input.txt")
}
