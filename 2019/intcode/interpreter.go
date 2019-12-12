package intcode

// Interpreter manages a running intcode program
type Interpreter struct {
	program Program  // An intcode program
	ip      int      // The instruction pointer
	input   chan int // The input channel
	output  chan int // The output channel
}

// NewInterpreter creates a new intcode interpreter
func NewInterpreter(filename string, input chan int, output chan int) (*Interpreter, error) {
	var i Interpreter
	err := i.Load(filename)
	if err != nil {
		return nil, err
	}
	i.input = input
	i.output = output
	return &i, nil
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
		i.ip, err = Execute(i.program, i.ip, i.input, i.output)
		if err != nil {
			return err
		}
		if i.ip == EndOfProgram {
			if i.output != nil {
				close(i.output)
			}
			return nil
		}
	}
}
