package main

import (
	"../aoc"
	"fmt"
	"log"
	"strconv"
	"strings"
)

var MemorySize = 1000

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

func paddedBits(input int64, bitCount int) string {
	bits := strconv.FormatInt(input, 2)
	if len(bits) < bitCount {
		// pad with zeroes to the left
		for len(bits) < bitCount {
			bits = "0" + bits
		}
	} else if len(bits) > bitCount {
		// trim leading bits
		for len(bits) > bitCount {
			bits = bits[1:]
		}
	}
	return bits
}

// Convert a number to its 36-bit representation
func bits36(input int64) string {
	return paddedBits(input, 36)
}

func parseMask(line string) string {
	return line[len("mask = "):]
}

func pow(base, expt int) int {
	result := 1
	for i := 0; i < expt; i++ {
		result *= base
	}
	return result
}

func indexesOf(s, substring string) []int {
	result := make([]int, 0)
	for i := 0; i < len(s)-len(substring)+1; i++ {
		if s[i:i+len(substring)] == substring {
			result = append(result, i)
		}
	}
	return result
}

// Given an memory index and a mask, return all the memory indices produced
func maskIndices(idx int64, mask string) ([]int64, error) {
	maskedIndex := make([]string, 36)
	index36 := bits36(idx)
	for i := range maskedIndex {
		switch mask[i] {
		case '0':
			maskedIndex[i] = string(index36[i])
		case '1':
			maskedIndex[i] = "1"
		case 'X':
			maskedIndex[i] = "X"
		}
	}
	//log.Printf("maskedIndex: %s", strings.Join(maskedIndex, ""))
	xIndexes := indexesOf(strings.Join(maskedIndex, ""), "X")
	//floatingCount := strings.Count(strings.Join(maskedIndex, ""), "X")
	//log.Printf("Found %d floating bits", xIndexes)
	result := make([]int64, 0)
	for i := 0; i < pow(2, len(xIndexes)); i++ {
		replacements := paddedBits(int64(i), len(xIndexes))
		//log.Printf("Replacement: %s", replacements)
		tmpMask := make([]string, len(maskedIndex))
		copy(tmpMask, maskedIndex)
		for j := 0; j < len(replacements); j++ {
			tmpMask[xIndexes[j]] = string(replacements[j])
		}
		//log.Printf("Replaced: %v", tmpMask)
		idx, err := strconv.ParseInt(strings.Join(tmpMask, ""), 2, 64)
		if err != nil {
			return nil, err
		}
		result = append(result, idx)
	}
	return result, nil
}

func p2SetMemory(memory map[int64]int64, mask string, line string) error {
	// parse the line for the location and variable
	loc, val, err := loadMemSet(line)
	if err != nil {
		return err
	}
	//log.Printf("Set %d to %d with mask %s", loc, val, mask)
	indices, err := maskIndices(loc, mask)
	if err != nil {
		return err
	}
	//log.Printf("Got %d indices", len(indices))
	for _, idx := range indices {
		//log.Printf("Index %d: %d", i, idx)
		memory[idx] = val
	}
	return nil
}

func part2(filename string) (int64, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	memory := make(map[int64]int64, MemorySize)
	var currentMask string
	for _, line := range lines {
		if line[0:4] == "mask" {
			currentMask = parseMask(line)
		} else {
			err := p2SetMemory(memory, currentMask, line)
			if err != nil {
				return 0, err
			}
		}
	}
	var sum int64
	for _, v := range memory {
		sum += v
	}
	return sum, nil
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
