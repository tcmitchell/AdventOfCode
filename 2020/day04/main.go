package main

import (
	"../aoc"
	"fmt"
	"log"
	"strings"
)

type Passport map[string]string

func (p Passport) String() string {
	elems := make([]string, len(p))
	i := 0
	for k, v := range p {
		elems[i] = fmt.Sprintf("%s=>%s", k, v)
		i++
	}
	return strings.Join(elems, " ")
}

func parsePassports(filename string) ([]Passport, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	result := make([]Passport, 0)
	passport := make(Passport)
	for i := 0; i < len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if line == "" {
			result = append(result, passport)
			passport = make(map[string]string)
			continue
		}
		fields := strings.Split(line, " ")
		for _, f := range fields {
			kv := strings.Split(f, ":")
			passport[kv[0]] = kv[1]
		}
	}
	// Add the passport we were working on
	result = append(result, passport)
	return result, nil
}

func validPassport(passport Passport) bool {
	requiredFields := []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
	for _, f := range requiredFields {
		_, ok := passport[f]
		if !ok {
			return false
		}
	}
	return true
}

func part1(filename string) (int, error) {
	passports, err := parsePassports(filename)
	if err != nil {
		return 0, err
	}
	//log.Printf("Loaded %d passports", len(passports))
	validCount := 0
	for _, p := range passports {
		//for k, v := range p {
		//	log.Printf("%s: %s\n", k, v)
		//}
		//log.Println()
		if validPassport(p) {
			validCount++
		}
	}
	// 212 is too low
	return validCount, nil
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
	return 0, nil
}
