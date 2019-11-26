package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const maxX = uint(1000)
const maxY = uint(1000)

// ReadInputLines reads the input file line by line,
// passing each line to the given channel.
func ReadInputLines(infile string, c chan string) {
	f, err := os.Open(infile)
	if err != nil {
		panic("foo")
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		c <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	close(c)
}

func loadRules(c chan string) map[string]string {
	result := make(map[string]string)
	for rule := range c {
		// fmt.Println(rule)
		parts := strings.Split(rule, " => ")
		fmt.Printf("%s -> %s\n", parts[0], parts[1])
		result[parts[0]] = parts[1]
	}
	return result
}

func transformBoard(board string, xform []int) (string, error) {
	exploded := strings.Split(board, "")
	result := make([]string, len(exploded))
	for i := 0; i < len(xform); i++ {
		result[i] = exploded[xform[i]]
	}
	return strings.Join(result, ""), nil
}

func rotateBoard(board string) (string, error) {
	boardSize := boardSize(board)
	if boardSize == 2 {
		xform := []int{3, 0, 2, 4, 1}
		return transformBoard(board, xform)
	}
	if boardSize == 3 {
		xform := []int{8, 4, 0, 3, 9, 5, 1, 7, 10, 6, 2}
		return transformBoard(board, xform)
	}
	return "", fmt.Errorf("Unknown board size %d", boardSize)
}

func flipBoard(board string) (string, error) {
	boardSize := boardSize(board)
	if boardSize == 2 {
		xform := []int{3, 4, 2, 0, 1}
		return transformBoard(board, xform)
	}
	if boardSize == 3 {
		xform := []int{8, 9, 10, 3, 4, 5, 6, 7, 0, 1, 2}
		return transformBoard(board, xform)
	}
	return "", fmt.Errorf("Unknown board size %d", boardSize)
}

func permuteBoard(board string) ([]string, error) {
	var err error
	result := make([]string, 8)
	result[0] = board
	for i := 1; i < 4; i++ {
		result[i], err = rotateBoard(result[i-1])
	}
	result[4], err = flipBoard(board)
	if err != nil {
		return nil, err
	}
	for i := 5; i < 8; i++ {
		result[i], err = rotateBoard(result[i-1])
	}
	return result, nil
}

func lookUpBoard(rules map[string]string, board string) (string, error) {
	// Look up the board in the rules, rotating and flipping
	// the board as necessary to find the rule.
	newBoard, ok := rules[board]
	if ok {
		return newBoard, nil
	}
	// If the board as passed is not in the rules, permute
	// it, and try the permutations in turn. Skip the first
	// entry because it is the original board and we know
	// that's not in there.
	boards, err := permuteBoard(board)
	if err != nil {
		return "", err
	}
	for _, b := range boards[1:] {
		newBoard, ok := rules[b]
		if ok {
			return newBoard, nil
		}
	}
	return "", fmt.Errorf("No match for %s", board)
}

// Determine the size of a board
func boardSize(board string) int {
	return len([]rune(strings.Split(board, "/")[0]))
}

func part1() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	rules := loadRules(c)
	for rule := range rules {
		fmt.Printf("%s to %s\n", rule, rules[rule])
	}
	board := ".#./..#/###"
	board2, err := lookUpBoard(rules, board)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Board 2: %s\n", board2)
	fmt.Printf("Board 2 size: %d\n", boardSize(board2))
}

func main() {
	part1()
}
