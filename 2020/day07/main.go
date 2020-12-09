package main

import (
	"../aoc"
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

type Bags struct {
	Count int
	Color string
}

type Rule struct {
	Color string
	Bags  []Bags
}

var RHSregex = regexp.MustCompile(`\d+ \w+ \w+ bag`)

func parseRule(line string) (Rule, error) {
	var rule Rule
	parts := strings.Split(line, " bags contain ")
	rule.Color = parts[0]
	// Now parse the right hand side
	contains := RHSregex.FindAllString(parts[1], -1)
	bags := make([]Bags, len(contains))
	for i, bag := range contains {
		//log.Printf(bag)
		elems := strings.Split(bag, " ")
		count, err := strconv.Atoi(elems[0])
		if err != nil {
			return rule, err
		}
		bags[i].Count = count
		bags[i].Color = strings.Join(elems[1:3], " ")
	}
	rule.Bags = bags
	return rule, nil
}

func loadRules(filename string) ([]Rule, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	rules := make([]Rule, len(lines))
	for i, line := range lines {
		rule, err := parseRule(line)
		if err != nil {
			return nil, err
		}
		rules[i] = rule
	}
	return rules, nil
}

func chainForward(rules map[string][]string) map[string]bool {
	allFound := make(map[string]bool)
	found := make(map[string]bool)
	found["shiny gold"] = true
	for len(found) > 0 {
		newlyFound := make(map[string]bool)
		for k := range found {
			for _, color := range rules[k] {
				newlyFound[color] = true
			}
		}
		for k := range newlyFound {
			allFound[k] = true
		}
		//log.Printf("%d newly found colors", len(newlyFound))
		found = newlyFound
	}
	return allFound
}

func part1(filename string) (int, error) {
	rules, err := loadRules(filename)
	if err != nil {
		return 0, err
	}
	//for _, rule := range rules {
	//	log.Printf(rule.Color)
	//	for _, bag := range rule.Bags {
	//		log.Printf("\t%d %s", bag.Count, bag.Color)
	//	}
	//}
	forwardChain := make(map[string][]string)
	for _, rule := range rules {
		for _, bag := range rule.Bags {
			chain, ok := forwardChain[bag.Color]
			if !ok {
				chain := make([]string, 0)
				forwardChain[bag.Color] = chain
			}
			forwardChain[bag.Color] = append(chain, rule.Color)
		}
	}
	//log.Printf("%q", forwardChain["shiny gold"])
	colors := chainForward(forwardChain)
	return len(colors), nil
}

func computeBagSize(color string, rules map[string]Rule, sizes map[string]int) int {
	size, ok := sizes[color]
	if ok {
		return size
	}
	// Need to compute size of this color via the rule
	rule := rules[color]
	size = 0
	for _, bag := range rule.Bags {
		size += (computeBagSize(bag.Color, rules, sizes) + 1) * bag.Count
	}
	sizes[color] = size
	return size
}

func part2(filename string) (int, error) {
	rules, err := loadRules(filename)
	if err != nil {
		return 0, err
	}
	// Make a map of color -> rule
	ruleMap := make(map[string]Rule)
	for _, rule := range rules {
		ruleMap[rule.Color] = rule
	}
	bagSizes := make(map[string]int)
	shinyGoldSize := computeBagSize("shiny gold", ruleMap, bagSizes)
	return shinyGoldSize, nil
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
