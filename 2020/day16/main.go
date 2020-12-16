package main

import (
	"../aoc"
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

type Rules map[string]map[int]bool

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

func loadYourTicket(lines []string) ([]int, error) {
	position := 0
	for i := range lines {
		if lines[i] == "your ticket:" {
			position = i
			break
		}
	}
	if position == 0 {
		return nil, fmt.Errorf("did not find your ticket")
	}
	parts := strings.Split(lines[position+1], ",")
	nums, err := stringsToInts(parts)
	if err != nil {
		return nil, err
	}
	return nums, nil
}

func loadRules(lines []string) (map[string]map[int]bool, error) {
	result := make(map[string]map[int]bool)
	// Rules are at the top of the file
	for _, line := range lines {
		if line == "" {
			// Rules go to the first blank line
			return result, nil
		}
		name, lo1, hi1, lo2, hi2, err := parseRule(line)
		if err != nil {
			return nil, err
		}
		values := make(map[int]bool)
		for i := lo1; i <= hi1; i++ {
			values[i] = true
		}
		for i := lo2; i <= hi2; i++ {
			values[i] = true
		}
		result[name] = values
	}
	return result, nil
}

// Filter to valid tickets using rules and nearby tickets
// Maybe need to combine rules into a single map for easier ticket validation
//      gatherValidValues(rules) map[int]bool {

func gatherValidValues(rules map[string]map[int]bool) map[int]bool {
	result := make(map[int]bool)
	for _, rule := range rules {
		for k, v := range rule {
			result[k] = v
		}
	}
	return result
}

// Remove tickets that contain invalid values
func filterInvalidTickets(tickets [][]int, rules map[string]map[int]bool) [][]int {
	validValues := gatherValidValues(rules)
	result := make([][]int, 0)
	for _, ticket := range tickets {
		valid := true
		for _, value := range ticket {
			if !validValues[value] {
				valid = false
			}
		}
		if valid {
			result = append(result, ticket)
		}
	}
	return result
}

// Returns the one key in a map if there is only one key.
// Returns empty string otherwise.
func loneKey(possibleRules map[string]bool) string {
	if len(possibleRules) != 1 {
		return ""
	}
	for k := range possibleRules {
		return k
	}
	return ""
}

func eliminateKey(possibleRules []map[string]bool, loneKey string) {
	for _, pr := range possibleRules {
		delete(pr, loneKey)
	}
}

func deducePositions(rules Rules, tickets [][]int) map[string]int {
	numFields := len(rules)
	possibleRules := make([]map[string]bool, numFields)
	for i := 0; i < numFields; i++ {
		possibleRules[i] = make(map[string]bool)
		for rule := range rules {
			possibleRules[i][rule] = true
		}
		for _, ticket := range tickets {
			for r, validNums := range rules {
				if !validNums[ticket[i]] {
					delete(possibleRules[i], r)
				}
			}
		}
		//log.Printf("Field %d: %v", i, possibleRules[i])
	}
	// Now figure out which name goes with which column
	result := make(map[string]int)
	for len(result) < len(rules) {
		for i := 0; i < numFields; i++ {
			if len(possibleRules[i]) == 1 {
				loneKey := loneKey(possibleRules[i])
				if loneKey != "" {
					result[loneKey] = i
					eliminateKey(possibleRules, loneKey)
				}
			}
		}
	}
	//log.Printf("%v", result)
	return result
}

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	rules, err := loadRules(lines)
	if err != nil {
		return 0, err
	}
	//for k := range rules {
	//	log.Printf("Rule %s", k)
	//}
	nearbyTickets, err := loadNearbyTickets(lines)
	if err != nil {
		return 0, err
	}
	validTickets := filterInvalidTickets(nearbyTickets, rules)
	positions := deducePositions(rules, validTickets)
	desiredKey := "departure"
	yourTicket, err := loadYourTicket(lines)
	if err != nil {
		return 0, err
	}
	result := 1
	for p, idx := range positions {
		if len(p) > len(desiredKey) && p[0:len(desiredKey)] == desiredKey {
			//log.Printf("%s: %d", p, idx)
			result *= yourTicket[idx]
		}
	}
	return result, nil
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
