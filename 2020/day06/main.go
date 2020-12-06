package main

import (
	"../aoc"
	"fmt"
	"log"
	"strings"
)

type Group []string

func loadForms(filename string) ([]Group, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}

	result := make([]Group, 0)
	g := make(Group, 0)
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			result = append(result, g)
			g = make(Group, 0)
			continue
		}
		g = append(g, line)
	}
	// Add the last group
	result = append(result, g)
	return result, nil
}

func tallyGroups(groups []Group) []map[rune]int {
	result := make([]map[rune]int, 0)
	for _, g := range groups {
		tally := make(map[rune]int)
		for _, f := range g {
			for _, r := range f {
				tally[r] = tally[r] + 1
			}
		}
		result = append(result, tally)
	}
	return result
}

func part1(filename string) (int, error) {
	groups, err := loadForms(filename)
	if err != nil {
		return 0, err
	}
	tallies := tallyGroups(groups)
	total := 0
	for _, t := range tallies {
		total += len(t)
	}
	return total, nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
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

func p2TallyGroups(groups []Group) []map[rune]int {
	result := make([]map[rune]int, 0)
	for _, g := range groups {
		tally := make(map[rune]int)
		for _, f := range g {
			for _, r := range f {
				tally[r] = tally[r] + 1
			}
		}
		tally2 := make(map[rune]int)
		n := len(g)
		// Keep the questions to which everyone said yes
		for k, v := range tally {
			if v == n {
				tally2[k] = v
			}
		}
		result = append(result, tally2)
	}
	return result
}

func part2(filename string) (int, error) {
	groups, err := loadForms(filename)
	if err != nil {
		return 0, err
	}
	tallies := p2TallyGroups(groups)
	total := 0
	for _, t := range tallies {
		total += len(t)
	}
	return total, nil
}
