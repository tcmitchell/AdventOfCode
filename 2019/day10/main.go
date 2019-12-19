package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strings"
)

type asteroid struct {
	x, y int
}

func (a *asteroid) String() string {
	return fmt.Sprintf("asteroid(%d, %d)", a.x, a.y)
}

type asteroidMap struct {
	locations [][]*asteroid
	asteroids []*asteroid
}

func (aMap *asteroidMap) String() string {
	var sb strings.Builder
	for _, row := range aMap.locations {
		for _, roid := range row {
			if roid == nil {
				sb.WriteString(".")
			} else {
				sb.WriteString("#")
			}
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func loadAsteroidMap(filename string) (*asteroidMap, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	result := new(asteroidMap)
	result.asteroids = make([]*asteroid, 0)
	rows := strings.Split(string(bytes), "\n")
	result.locations = make([][]*asteroid, len(rows))
	for y, row := range rows {
		result.locations[y] = make([]*asteroid, len(row))
		for x, loc := range row {
			if loc == '#' {
				roid := asteroid{x: x, y: y}
				result.locations[y][x] = &roid
				result.asteroids = append(result.asteroids, &roid)
			}
		}
	}
	return result, nil
}

func absInt(x int) int {
	return int(math.Abs(float64(x)))
}

func lineOfSight(a1, a2 *asteroid, aMap *asteroidMap) bool {
	// log.Printf("lineOfSight(%s, %s)\n", a1, a2)
	dx := a2.x - a1.x
	dy := a2.y - a1.y
	// log.Printf("dx = %d; dy = %d\n", dx, dy)
	gcd := gcd(absInt(dx), absInt(dy))
	// log.Printf("gcd = %d\n", gcd)
	if gcd == 1 {
		// No gcd means must have line of sight
		return true
	}
	stepx := dx / gcd
	stepy := dy / gcd
	// log.Printf("stepx = %d; stepy = %d\n", stepx, stepy)
	x := a1.x
	y := a1.y
	for x != a2.x || y != a2.y {
		x += stepx
		y += stepy
		roid := aMap.locations[y][x]
		// log.Printf("aMap.locations[%d][%d] = %s\n", x, y, roid)
		if roid != nil && roid != a2 {
			return false
		}
	}
	return true
}

func part1(puzzleInput string) error {
	aMap, err := loadAsteroidMap(puzzleInput)
	if err != nil {
		return err
	}
	// fmt.Print(aMap)
	var losCount int
	var losAsteroid *asteroid
	for _, roid1 := range aMap.asteroids {
		myCount := 0
		for _, roid2 := range aMap.asteroids {
			if roid1 == roid2 {
				continue
			}
			myLos := lineOfSight(roid1, roid2, aMap)
			// log.Printf("%s --los--> %s: %t", roid1, roid2, myLos)
			if myLos {
				myCount++
			}
			// fmt.Printf("%s los %s: %t\n", roid1, roid2, los)
		}
		if myCount > losCount {
			losCount = myCount
			losAsteroid = roid1
		}
	}
	fmt.Printf("Part 1: %d from %s\n", losCount, losAsteroid)
	return nil
}

func part2(puzzleInput string) error {
	answer := 0
	fmt.Printf("Part 2: %d\n", answer)
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	err = part2("input.txt")
	if err != nil {
		panic(err)
	}
}
