package main

import (
	"../aoc"
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

var LineRegex = regexp.MustCompile(`^(\d+)-(\d+) (.): (.*)$`)

func parseLine(line string) (int, int, string, string, error) {
	matches := LineRegex.FindStringSubmatch(line)
	if matches == nil {
		// Did not match
		return 0, 0, "", "", fmt.Errorf("unable to parse line %s", line)
	}
	lo, err := strconv.Atoi(matches[1])
	if err != nil {
		return 0, 0, "", "", err
	}
	hi, err := strconv.Atoi(matches[2])
	if err != nil {
		return 0, 0, "", "", err
	}
	return lo, hi, matches[3], matches[4], nil
}

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	validPasswords := 0
	for _, line := range lines {
		lo, hi, char, password, err := parseLine(line)
		if err != nil {
			return 0, err
		}
		//log.Printf("%d-%d %s: %s", lo, hi, char, password)
		occurs := strings.Count(password, char)
		//log.Printf("Found %d occurrences of %s in %s", occurs, char, password)
		if lo <= occurs && occurs <= hi {
			//log.Printf("%s is a valid password", password)
			validPasswords++
		}
	}
	return validPasswords, nil
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

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	validPasswords := 0
	for _, line := range lines {
		lo, hi, char, password, err := parseLine(line)
		if err != nil {
			return 0, err
		}
		// Decrement so the indices are zero-based
		lo--
		hi--
		//log.Printf("%d-%d %s: %s", lo, hi, char, password)
		chr := char[0]
		if (password[lo] == chr && password[hi] != chr) ||
			(password[lo] != chr && password[hi] == chr) {
			//log.Printf("%s is a valid password", password)
			validPasswords++
		}
	}
	return validPasswords, nil
}
