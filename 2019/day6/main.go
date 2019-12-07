package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func loadOrbits(filename string) (map[string][]string, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	data := strings.TrimSpace(string(bytes))
	orbits := make(map[string][]string)
	for _, line := range strings.Split(data, "\n") {
		planets := strings.Split(line, ")")
		//fmt.Printf("%s ) %s\n", planets[0], planets[1])
		orbits[planets[0]] = append(orbits[planets[0]], planets[1])
	}
	return orbits, nil
}

func countOrbits(orbits map[string][]string, planet string, sum *int) int {
	children := orbits[planet]
	count := len(children)
	for _, c := range children {
		count += countOrbits(orbits, c, sum)
	}
	// fmt.Printf("Count for %s = %d\n", planet, count)
	*sum += count
	return count
}

func part1(puzzleInput string) error {
	orbits, err := loadOrbits(puzzleInput)
	if err != nil {
		return err
	}
	sum := 0
	countOrbits(orbits, "COM", &sum)
	fmt.Printf("Part 1: %d\n", sum)
	return nil
}

func pathToPlanet(orbits map[string][]string, planet string, target string) []string {
	children := orbits[planet]
	for _, c := range children {
		if c == target {
			return []string{planet}
		}
		path := pathToPlanet(orbits, c, target)
		if path != nil {
			return append(path, planet)
		}
	}
	// target was not found
	return nil
}

func part2(puzzleInput string) error {
	orbits, err := loadOrbits(puzzleInput)
	if err != nil {
		return err
	}
	youPath := pathToPlanet(orbits, "COM", "YOU")
	// fmt.Printf("%s\n", youPath)
	dist := make(map[string]int)
	for i, p := range youPath {
		dist[p] = i
	}
	sanPath := pathToPlanet(orbits, "COM", "SAN")
	for i, p := range sanPath {
		d, ok := dist[p]
		if ok {
			// fmt.Printf("Common ancestor is %s\n", p)
			fmt.Printf("Part 2: %d", d+i)
			return nil
		}
	}
	fmt.Printf("Part 2: No answer found\n")
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
