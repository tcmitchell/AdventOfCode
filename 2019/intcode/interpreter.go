package intcode

import (
	"log"
)

// Interpreter manages a running intcode program
type Interpreter struct {
	program   Program        // An intcode program
	ip        int            // The instruction pointer
	relBase   int            // The relative parameter base
	input     chan int       // The input channel
	output    chan int       // The output channel
	name      string         // The name of this interpreter for debugging
	inputFunc func(chan int) // A function to invoke for input
}

// NewInterpreter creates a new intcode interpreter
func NewInterpreter(filename string, input chan int, output chan int, name string) (*Interpreter, error) {
	i := new(Interpreter)
	err := i.Load(filename)
	if err != nil {
		return nil, err
	}
	i.input = input
	i.output = output
	i.name = name
	return i, nil
}

// Load reads a program from disk and resets the instruction pointer
func (i *Interpreter) Load(filename string) error {
	var err error
	i.program, err = Load(filename)
	if err != nil {
		return err
	}
	i.ip = 0
	return nil
}

// Run executes an intcode program
func (i *Interpreter) Run() error {
	var err error
	for {
		// log.Printf("%s executing instruction pointer %d\n", i.name, i.ip)
		i.ip, err = Execute(i)
		if err != nil {
			return err
		}
		if i.ip > len(i.program) {
			log.Printf("%s instruction pointer went out of range: %d of %d\n",
				i.name, i.ip, len(i.program))
		}
		if i.ip == EndOfProgram {
			if i.output != nil {
				// log.Printf("%s closing output channel\n", i.name)
				close(i.output)
			}
			return nil
		}
	}
}

func (i *Interpreter) SetInputFunction(f func(chan int)) {
	i.inputFunc = f
}

func (i *Interpreter) SetMemoryLocation(location, value int) {
	i.program[location] = value
}
