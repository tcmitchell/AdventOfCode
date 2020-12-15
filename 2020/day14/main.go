package main

import (
	"../aoc"
	"fmt"
	"log"
	"strconv"
	"strings"
)

func loadMasks(line string) (int64, int64) {
	var andMask, orMask int64
	for _, c := range line[7:] {
		switch c {
		case 'X':
			andMask = andMask<<1 + 1
			orMask = orMask<<1 + 0
		case '1':
			andMask = andMask<<1 + 1
			orMask = orMask<<1 + 1
		case '0':
			andMask = andMask<<1 + 0
			orMask = orMask<<1 + 0
		default:
			panic(fmt.Errorf("unknown mask line %s", line))
		}
	}
	//log.Printf("andMask: %d", andMask)
	//log.Printf(strconv.FormatInt(andMask, 2))
	//log.Printf("orMask: %d", orMask)
	//log.Printf(strconv.FormatInt(orMask, 2))
	return andMask, orMask
}

func loadMemSet(line string) (int64, int64, error) {
	parts := strings.Split(line, "] = ")
	locString := parts[0][4:]
	loc, err := strconv.Atoi(locString)
	if err != nil {
		return 0, 0, err
	}
	value, err := strconv.Atoi(parts[1])
	if err != nil {
		return 0, 0, err
	}
	return int64(loc), int64(value), nil
}

func setMemory(memory map[int64]int64, location, value, andMask, orMask int64) {
	//log.Printf("Start value: %s", strconv.FormatInt(value, 2))
	maskValue := value | orMask
	//log.Printf("after or mask: %s", strconv.FormatInt(maskValue, 2))
	maskValue = maskValue & andMask
	//log.Printf("after and mask: %s", strconv.FormatInt(maskValue, 2))
	//log.Printf("Set %d to %d (was %d)", location, maskValue, value)
	memory[location] = maskValue
	//log.Printf("Memory: %v", memory)
}

func part1(filename string) (int64, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	var andMask, orMask int64
	memory := make(map[int64]int64)
	for _, line := range lines {
		if line[0:4] == "mask" {
			//log.Printf("Mask: %s", line)
			andMask, orMask = loadMasks(line)
		} else {
			location, value, err := loadMemSet(line)
			if err != nil {
				return 0, err
			}
			setMemory(memory, location, value, andMask, orMask)
		}
	}
	var sum int64
	for _, v := range memory {
		sum += v
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
