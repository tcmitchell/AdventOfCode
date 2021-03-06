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

func (resource *Resource) String() string {
	return fmt.Sprintf("#<%d of %s>", resource.Quantity, resource.Name)
}

type Rule struct {
	Product Resource
	Resources []Resource
}

func (rule *Rule) String() string {
	return fmt.Sprintf("#<Produce %d of %s>", rule.Product.Quantity, rule.Product.Name)
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
	rule := Rule{product, resources}
	return &rule, nil
}

func loadRules(ruleFile string) ([]*Rule, error) {
	bytes, err := ioutil.ReadFile(ruleFile)
	if err != nil {
		return nil, err
	}
	data := strings.TrimSpace(string(bytes))
	lines := strings.Split(data, "\n")
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

func makeResourceRuleMap(rules []*Rule) map[string]*Rule {
	result := make(map[string]*Rule)
	for _, rule := range rules {
		result[rule.Product.Name] = rule
	}
	return result
}

func produce(product Resource, rrm map[string]*Rule, warehouse *map[string]int) int {
	if product.Name == "ORE" {
		// Special case, we can use as much ORE as we want
		if (*warehouse)["ORE"] > product.Quantity {
			// There's already enough in the warehouse
			return 0
		} else {
			(*warehouse)["ORE"] += product.Quantity
			return product.Quantity
		}
	}
	oreUsed := 0
	// for each ingredient, ensure the warehouse has enough to produce the named resource
	rule := rrm[product.Name]
	for _, ingredient := range rule.Resources {
		// does the warehouse have enough of the resource?
		for ; ingredient.Quantity > (*warehouse)[ingredient.Name]; {
			oreUsed += produce(ingredient, rrm, warehouse)
		}
		// Now remove from the warehouse the amount required to produce `product`
		(*warehouse)[ingredient.Name] -= ingredient.Quantity
	}
	// Now add the product to the warehouse
	(*warehouse)[rule.Product.Name] += rule.Product.Quantity
	return oreUsed
}

func part1(ruleFile string) (int, error) {
	rules, err := loadRules(ruleFile)
	if err != nil {
		return 0, err
	}
	log.Printf("Loaded %d rules", len(rules))
	// Map of resource name to production rule for that resource
	rrm := makeResourceRuleMap(rules)
	// Hold stock of resources that can be used in production
	warehouse := make(map[string]int)
	oreUsed := produce(Resource{1, "FUEL"}, rrm, &warehouse)
	return oreUsed, nil
}

func main() {
	fmt.Print("Hello, World!\n")
	programFile := "input.txt"
	//programFile = "test-input1.txt"
	//programFile = "test-input5.txt"
	ore, err := part1(programFile)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d", ore)
	//part2(programFile)
}
