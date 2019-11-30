package main

import (
	"bufio"
	"fmt"
	"os"
)

// ReadInputLines reads the input file line by line,
// passing each line to the given channel.
func ReadInputLines(infile string, c chan string) {
	f, err := os.Open(infile)
	if err != nil {
		panic("foo")
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		c <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	close(c)
}

func loadComponents(c chan string) ([]component, error) {
	result := make([]component, 0)
	for line := range c {
		cptr, err := makeComponent(line)
		if err != nil {
			return nil, err
		}
		result = append(result, *cptr)
	}
	return result, nil
}

func findComponents(components []component, p int) []int {
	result := make([]int, 0)
	for i, c := range components {
		if c.hasPort(p) {
			result = append(result, i)
		}
	}
	return result
}

func findComponent(components []component, c component) int {
	for i, aComponent := range components {
		if c == aComponent {
			return i
		}
	}
	return -1
}

func copyComponents(components []component) []component {
	result := make([]component, len(components))
	for i, c := range components {
		result[i] = c
	}
	return result
}

func removeItem(components []component, c component) []component {
	pos := findComponent(components, c)
	if pos == -1 {
		// Not found!
		panic("item not found")
	}
	if pos == 0 {
		return components[1:]
	}
	numComponents := len(components)
	// move the last item to the position of the component
	components[pos] = components[numComponents-1]
	return components[:numComponents-1]
}

func buildBridges(bridges []bridge) []bridge {
	result := make([]bridge, 0)
	for _, b := range bridges {
		if b.done {
			// fmt.Printf("Skipping bridge %q\n", b.components)
			result = append(result, b)
			continue
		}
		// fmt.Printf("Bridge %q is not done\n", b.components)
		matches := findComponents(b.stockpile, b.endPort)
		for _, idx := range matches {
			// fmt.Printf("Found %s for end port %d of %q\n", b.stockpile[idx], b.endPort, b.components)
			newBridge := *copyBridge(b)
			newBridge.addComponent(newBridge.stockpile[idx])
			// fmt.Printf("Adding new bridge %q\n", newBridge)
			result = append(result, newBridge)
		}
		b.done = true
		// fmt.Printf("Marked bridge %q done\n", b.components)
		result = append(result, b)
	}
	// fmt.Printf("Leaving buildBridges:\n")
	// for _, b := range result {
	// 	fmt.Printf("\t%s\n", b)
	// }
	return result
}

func part1(puzzleInput string) []bridge {
	c := make(chan string, 1)
	go ReadInputLines(puzzleInput, c)
	components, err := loadComponents(c)
	if err != nil {
		panic(err)
	}
	// fmt.Printf("Program size: %d\n", len(components))
	// for _, c := range components {
	// 	fmt.Println(c)
	// }
	matches := findComponents(components, 0)
	for _, idx := range matches {
		fmt.Printf("Has zero: %s\n", components[idx])
	}
	for _, idx := range matches[:len(matches)-1] {
		fmt.Printf("Match %d\n", idx)
	}
	fmt.Printf("Final match: %d\n", matches[len(matches)-1])
	bridges := make([]bridge, len(matches))
	for i, idx := range matches {
		stockpile := copyComponents(components)
		stockpile = removeItem(stockpile, components[idx])
		bridges[i] = *makeBridge(components[idx], stockpile)
	}
	for i, b := range bridges {
		fmt.Printf("Bridge %d: %s (%d)\n", i, b.components[0], b.endPort)
	}
	countBridges := len(bridges)
	fmt.Printf("Built %d bridges\n", countBridges)
	bridges = buildBridges(bridges)
	fmt.Printf("Now have %d bridges\n", len(bridges))
	fmt.Printf("\n--------------------------------------------------\n")
	for countBridges < len(bridges) {
		countBridges = len(bridges)
		fmt.Printf("Built %d bridges\n", countBridges)
		bridges = buildBridges(bridges)
		fmt.Printf("Now have %d bridges\n", len(bridges))
		// for _, b := range bridges {
		// 	fmt.Printf("\t%s\n", b)
		// }
		fmt.Printf("\n--------------------------------------------------\n")
	}
	strongest := 0
	for _, b := range bridges {
		strength := b.strength()
		if strength > strongest {
			strongest = strength
		}
	}
	fmt.Printf("Strongest bridge: %d\n", strongest)
	return bridges
}

func part2(bridges []bridge) {
	longest := 0
	strongest := 0
	for _, b := range bridges {
		bLen := len(b.components)
		if bLen > longest {
			longest = bLen
			strongest = b.strength()
			continue
		}
		if bLen == longest {
			if b.strength() > strongest {
				strongest = b.strength()
			}
			continue
		}
	}
	fmt.Printf("The longest bridge is %d; the strongest longest bridge is %d", longest, strongest)
}

func main() {
	bridges := part1("input.txt")
	part2(bridges)
}
