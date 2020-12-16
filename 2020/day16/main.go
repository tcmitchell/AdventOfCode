package main

import (
	"../aoc"
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

var RuleRegex = regexp.MustCompile(`^(\d+)-(\d+) or (\d+)-(\d+)$`)

func parseRule(line string) (string, int, int, int, int, error) {
	nameRange := strings.Split(line, ": ")
	name := nameRange[0]
	matches := RuleRegex.FindStringSubmatch(nameRange[1])
	if matches == nil {
		// Did not match
		return "", 0, 0, 0, 0, fmt.Errorf("unable to parse line %s", line)
	}
	lo1, err := strconv.Atoi(matches[1])
	if err != nil {
		return "", 0, 0, 0, 0, err
	}
	hi1, err := strconv.Atoi(matches[2])
	if err != nil {
		return "", 0, 0, 0, 0, err
	}
	lo2, err := strconv.Atoi(matches[3])
	if err != nil {
		return "", 0, 0, 0, 0, err
	}
	hi2, err := strconv.Atoi(matches[4])
	if err != nil {
		return "", 0, 0, 0, 0, err
	}
	return name, lo1, hi1, lo2, hi2, nil
}

func p1LoadRules(lines []string) ([]bool, error) {
	result := make([]bool, 1000)
	for _, line := range lines {
		if line == "" {
			// Rules go to the first blank line
			return result, nil
		}
		_, lo1, hi1, lo2, hi2, err := parseRule(line)
		if err != nil {
			return nil, err
		}
		for i := lo1; i <= hi1; i++ {
			result[i] = true
		}
		for i := lo2; i <= hi2; i++ {
			result[i] = true
		}
	}
	return nil, fmt.Errorf("did not recognize end of rules")
}

func stringsToInts(input []string) ([]int, error) {
	result := make([]int, len(input))
	for i, v := range input {
		n, err := strconv.Atoi(v)
		if err != nil {
			return nil, err
		}
		result[i] = n
	}
	return result, nil
}

func loadNearbyTickets(lines []string) ([][]int, error) {
	result := make([][]int, 0)
	nearbyTickets := 0
	for i := range lines {
		if lines[i] == "nearby tickets:" {
			nearbyTickets = i
			break
		}
	}
	if nearbyTickets == 0 {
		return nil, fmt.Errorf("did not find nearby tickets")
	}
	for i := nearbyTickets + 1; i < len(lines); i++ {
		parts := strings.Split(lines[i], ",")
		nums, err := stringsToInts(parts)
		if err != nil {
			return nil, err
		}
		result = append(result, nums)
	}
	return result, nil
}

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	rules, err := p1LoadRules(lines)
	if err != nil {
		return 0, err
	}
	for i, b := range rules {
		if b {
			log.Printf("%d = %v", i, b)
		}
	}
	tickets, err := loadNearbyTickets(lines)
	if err != nil {
		return 0, err
	}
	errorRate := 0
	for _, ticket := range tickets {
		for _, num := range ticket {
			if !rules[num] {
				errorRate += num
			}
		}
	}
	return errorRate, nil
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
