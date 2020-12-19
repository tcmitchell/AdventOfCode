package main

import (
	"../aoc"
	"fmt"
	"log"
	"strconv"
	"strings"
)

type Token struct {
	Op  string
	Val int
}

func (t Token) String() string {
	return fmt.Sprintf("Token{Op: %s, Val: %d}", t.Op, t.Val)
}

func (t Token) IsOperator() bool {
	return t.Op == "+" || t.Op == "*"
}

func NewToken(t string) (Token, error) {
	switch t {
	case "(", ")", "+", "*":
		return Token{Op: t}, nil
	default:
		v, err := strconv.Atoi(t)
		if err != nil {
			return Token{}, err
		}
		return Token{Val: v}, nil
	}
}

func tokenize(expr string) ([]Token, error) {
	parts := strings.Split(expr, " ")
	result := make([]Token, 0)
	for _, p := range parts {
		for _, c := range strings.Split(p, "") {
			t, err := NewToken(c)
			if err != nil {
				return nil, err
			}
			result = append(result, t)
		}
	}
	return result, nil
}

func p1ShuntingYard(tokens []Token) ([]Token, error) {
	out := make([]Token, 0)
	opStack := make([]Token, 0)
	for _, t := range tokens {
		switch t.Op {
		case "":
			// token is a number
			out = append(out, t)
		case "+", "*":
			// Pop operators from the operator stack to the output queue
			for len(opStack) > 0 && opStack[len(opStack)-1].IsOperator() {
				out = append(out, opStack[len(opStack)-1])
				opStack = opStack[:len(opStack)-1]
			}
			// Add this operator to the operator queue
			opStack = append(opStack, t)
		case "(":
			opStack = append(opStack, t)
		case ")":
			// Pop operators from the operator stack to the output queue
			for len(opStack) > 0 && opStack[len(opStack)-1].Op != "(" {
				out = append(out, opStack[len(opStack)-1])
				opStack = opStack[:len(opStack)-1]
			}
			// if there is a left parenthesis at the top of the operator stack
			if opStack[len(opStack)-1].Op == "(" {
				// drop it
				opStack = opStack[:len(opStack)-1]
			}
		default:
			return nil, fmt.Errorf("unknown token %s", t)
		}
	}
	for len(opStack) > 0 {
		out = append(out, opStack[len(opStack)-1])
		opStack = opStack[:len(opStack)-1]
	}
	return out, nil
}

func p1EvalRpn(tokens []Token) (int, error) {
	args := make([]int, 0)
	for len(tokens) > 0 {
		//log.Printf("Args: %v", args)
		//log.Printf("Tokens: %v", tokens)
		if tokens[0].IsOperator() {
			switch tokens[0].Op {
			case "+":
				a1 := args[len(args)-1]
				a2 := args[len(args)-2]
				args = args[:len(args)-2]
				args = append(args, a1+a2)
				tokens = tokens[1:]
			case "*":
				a1 := args[len(args)-1]
				a2 := args[len(args)-2]
				args = args[:len(args)-2]
				args = append(args, a1*a2)
				tokens = tokens[1:]
			}
		} else {
			args = append(args, tokens[0].Val)
			tokens = tokens[1:]
		}
	}
	return args[0], nil
}

func p1EvalExpr(expr string) (int, error) {
	tokens, err := tokenize(expr)
	if err != nil {
		return 0, err
	}
	tokens, err = p1ShuntingYard(tokens)
	if err != nil {
		return 0, err
	}
	return p1EvalRpn(tokens)
}

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	sum := 0
	for _, line := range lines {
		value, err := p1EvalExpr(line)
		if err != nil {
			return 0, err
		}
		sum += value
	}
	return sum, nil
}

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	return len(lines), nil
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
