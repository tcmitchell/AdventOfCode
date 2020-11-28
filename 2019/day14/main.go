package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type Resource struct {
	Quantity int
	Name     string
}

type Rule struct {
	Product Resource
	Resources []Resource
}

func parseResource(s string) (Resource, error) {
	log.Printf("Parsing resource %s", s)
	parts := strings.Split(s, " ")
	qty, err := strconv.Atoi(strings.TrimSpace(parts[0]))
	if err != nil {
		return Resource{}, err
	}
	return Resource{qty, strings.TrimSpace(parts[1])}, nil
}

func parseRule(line string) (*Rule, error) {
	// Split the rule line into resources and product
	parts := strings.Split(line, "=>")
	// Parse LHS of resources
	resourceStrings := strings.Split(parts[0], ",")
	resources := make([]Resource, len(resourceStrings))
	for i, r := range resourceStrings {
		resource, err := parseResource(strings.TrimSpace(r))
		if err != nil {
			return nil, err
		}
		resources[i] = resource
	}
	// Parse RHS of product
	product, err := parseResource(strings.TrimSpace(parts[1]))
	if err != nil {
		return nil, err
	}
	// Make and return a rule
	rule := Rule{product, nil}
	return &rule, nil
}

func loadRules(ruleFile string) ([]*Rule, error) {
	bytes, err := ioutil.ReadFile(ruleFile)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(bytes), "\n")
	log.Printf("Loaded %d lines of rules", len(lines))
	rules := make([]*Rule, len(lines))
	for i, line := range lines {
		if line == "" {
			continue
		}
		rule, err := parseRule(line)
		if err != nil {
			return nil, err
		}
		rules[i] = rule
	}
	return rules, nil
}

func part1(ruleFile string) (int, error) {
	rules, err := loadRules(ruleFile)
	if err != nil {
		return 0, err
	}
	log.Printf("Loaded %d rules", len(rules))
	return 0, nil
}

func main() {
	fmt.Print("Hello, World!\n")
	programFile := "input.txt"
	programFile = "test-input1.txt"
	ore, err := part1(programFile)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d", ore)
	//part2(programFile)
}
