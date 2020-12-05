package main

import (
	"../aoc"
	"fmt"
	"log"
)

type BoardingPass string

func passToRow(bp BoardingPass) int {
	rowLen := 7
	bpRow := bp[0:rowLen]
	//log.Printf("Row Indicator: %s", bpRow)
	row := 0
	for i := 0; i < rowLen; i++ {
		if bpRow[i] == 'B' {
			row = row + 1<<(rowLen-i-1)
		}
	}
	return row
}

func passToColumn(bp BoardingPass) int {
	colLen := 3
	bpColumn := bp[7 : 7+colLen]
	//log.Printf("Column Indicator: %s", bpColumn)
	column := 0
	for i := 0; i < colLen; i++ {
		if bpColumn[i] == 'R' {
			column = column + 1<<(colLen-i-1)
		}
	}
	return column
}

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	maxId := 0
	for _, line := range lines {
		row := passToRow(BoardingPass(line))
		//log.Printf("Row: %d", row)
		column := passToColumn(BoardingPass(line))
		//log.Printf("Column: %d", column)
		id := row*8 + column
		if id > maxId {
			maxId = id
		}
	}
	return maxId, nil
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

func part2(filename string) (int, error) {
	return 0, nil
}
