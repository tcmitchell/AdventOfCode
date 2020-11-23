package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"strings"
)

// rads2degs converts an angle measured in radians to an
// angle measured in degrees.
func rads2degs(rads float64) float64 {
	return rads * 180.0 / math.Pi
}

type asteroid struct {
	x, y int
	// Angle from the radar station
	angle float64
	// Distance from the radar station
	distance float64
}

func (a *asteroid) String() string {
	return fmt.Sprintf("asteroid(%d, %d)", a.x, a.y)
}

// angle2asteroid finds the angle from vertical measuring clockwise
// between the asteroid and another asteroid.
func (a *asteroid) angle2asteroid(a2 *asteroid) float64 {
	v1x := float64(0)
	v1y := float64(a.y)
	v2x := float64(a2.x - a.x)
	v2y := float64(a2.y - a.y)
	num := v1x*v2x + v1y*v2y
	//log.Printf("Numerator: %e", num)
	denom := math.Sqrt(v1x*v1x+v1y*v1y) * math.Sqrt(v2x*v2x+v2y*v2y)
	//log.Printf("Denominator: %e", denom)
	angle := math.Acos(num / denom)
	//log.Printf("Angle = %e\n", angle)
	degs := rads2degs(angle)
	if a2.x < a.x {
		degs += 180
	} else {
		degs = 180 - degs
	}
	return degs
}

func (a *asteroid) dist2asteroid(a2 *asteroid) float64 {
	dx := a2.x - a.x
	dy := a2.y - a.y
	return math.Sqrt(math.Pow(float64(dx), 2) + math.Pow(float64(dy), 2))
}

// --------------------------------------------------
// asteroidMap
// --------------------------------------------------

// asteroidMap contains all the asteroids in the problem input.
//
// Field locations is an array of arrays of asteroids, indexed by
// y-position (outer array) and x-position (inner arrays).
//
// Field asteroids is an array of all asteroids.
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

func part1(aMap *asteroidMap) (*asteroid, int, error) {
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
	//fmt.Printf("Part 1: %d from %s\n", losCount, losAsteroid)
	return losAsteroid, losCount, nil
}

func part2(_ *asteroidMap, _ *asteroid) error {
	//fmt.Print(aMap)
	answer := 0
	fmt.Printf("Part 2: %d\n", answer)
	return nil
}

func main() {
	puzzleInput := "input.txt"
	aMap, err := loadAsteroidMap(puzzleInput)
	if err != nil {
		log.Fatal(err)
	}
	// fmt.Print(aMap)
	losAsteroid, losCount, err := part1(aMap)
	fmt.Printf("Part 1: %d\n", losCount)
	if err != nil {
		log.Fatal(err)
	}
	err = part2(aMap, losAsteroid)
	if err != nil {
		log.Fatal(err)
	}
}
