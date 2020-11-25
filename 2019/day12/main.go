package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

var MoonNames = [...]string{"Io", "Europa", "Ganymede", "Callisto"}

type Point3D struct {
	x, y, z int
}

type Moon struct {
	Name     string
	Position Point3D
	Velocity Point3D
}

func (moon *Moon) String() string {
	return fmt.Sprintf("#<%s: P(%d, %d, %d) V(%d, %d, %d)>",
		moon.Name, moon.Position.x, moon.Position.y, moon.Position.z,
		moon.Velocity.x, moon.Velocity.y, moon.Velocity.z)
}

func MakeMoon(idx int, coords []int) *Moon {
	moon := Moon{}
	moon.Name = MoonNames[idx]
	moon.Position.x = coords[0]
	moon.Position.y = coords[1]
	moon.Position.z = coords[2]
	return &moon
}

func parseInput(inputFile string) ([]*Moon, error) {
	result := make([]*Moon, 0)
	bytes, err := ioutil.ReadFile(inputFile)
	if err != nil {
		return nil, err
	}
	rows := strings.Split(string(bytes), "\n")
	for idx, row := range rows {
		if len(row) == 0 {
			continue
		}
		row = strings.Trim(row, "<>")
		//log.Printf("%d: %s\n", idx, row)
		elems := strings.Split(row, ", ")
		coords := make([]int, len(elems))
		for j, e := range elems {
			items := strings.Split(e, "=")
			coords[j], err = strconv.Atoi(items[1])
			if err != nil {
				return nil, err
			}
		}
		result = append(result, MakeMoon(idx, coords))
	}
	return result, nil
}

func computeGravity(m1, m2 *Moon) {
	if m1.Position.x > m2.Position.x {
		m1.Velocity.x -= 1
		m2.Velocity.x += 1
	} else if m1.Position.x < m2.Position.x {
		m1.Velocity.x += 1
		m2.Velocity.x -= 1
	}
	if m1.Position.y > m2.Position.y {
		m1.Velocity.y -= 1
		m2.Velocity.y += 1
	} else if m1.Position.y < m2.Position.y {
		m1.Velocity.y += 1
		m2.Velocity.y -= 1
	}
	if m1.Position.z > m2.Position.z {
		m1.Velocity.z -= 1
		m2.Velocity.z += 1
	} else if m1.Position.z < m2.Position.z {
		m1.Velocity.z += 1
		m2.Velocity.z -= 1
	}
}

func applyVelocity(moons []*Moon) {
	for _, moon := range moons {
		moon.Position.x = moon.Position.x + moon.Velocity.x
		moon.Position.y = moon.Position.y + moon.Velocity.y
		moon.Position.z = moon.Position.z + moon.Velocity.z
	}
}

func absInt(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func absSum(p Point3D) int {
	return absInt(p.x) + absInt(p.y) + absInt(p.z)
}

func computeEnergy(moons []*Moon) int {
	energy := 0
	for _, m := range moons {
		p := absSum(m.Position)
		k := absSum(m.Velocity)
		energy += p * k
	}
	return energy
}

func part1(inputFile string) error {
	moons, err := parseInput(inputFile)
	if err != nil {
		return err
	}
	//log.Printf("Loaded %d moons\n", len(moons))
	//for _, moon := range moons {
	//	log.Printf("%s\n", moon)
	//}
	iters := 1000
	for iter := 0; iter < iters; iter++ {
		for j := 0; j < len(moons)-1; j++ {
			for k := j + 1; k < len(moons); k++ {
				computeGravity(moons[j], moons[k])
			}
		}
		applyVelocity(moons)
		//log.Printf("----- After iteration %d -----\n", iter+1)
		//for _, moon := range moons {
		//	log.Printf("%s\n", moon)
		//}
		//log.Println()
	}
	energy := computeEnergy(moons)
	fmt.Printf("Part 1: %d\n", energy)
	return nil
}

// ------------------------------------------------------------
// Part 2
// ------------------------------------------------------------

func p2ComputeGravity(p1, p2, v1, v2 int) (int, int) {
	if p1 > p2 {
		v1 -= 1
		v2 += 1
	} else if p1 < p2 {
		v1 += 1
		v2 -= 1
	}
	return v1, v2
}

func findCycle(p1, p2, p3, p4, limit int) (int, error) {
	s1, s2, s3, s4 := p1, p2, p3, p4
	var v1, v2, v3, v4 int
	//log.Printf("%d: %d, %d, %d, %d", 0, p1, p2, p3, p4)
	for i := 0; i < limit; i++ {
		// Compute velocity
		v1, v2 = p2ComputeGravity(p1, p2, v1, v2)
		v1, v3 = p2ComputeGravity(p1, p3, v1, v3)
		v1, v4 = p2ComputeGravity(p1, p4, v1, v4)
		v2, v3 = p2ComputeGravity(p2, p3, v2, v3)
		v2, v4 = p2ComputeGravity(p2, p4, v2, v4)
		v3, v4 = p2ComputeGravity(p3, p4, v3, v4)
		//log.Printf("Velocity %d: %d, %d, %d, %d", i+1, v1, v2, v3, v4)
		// Compute new position
		p1 += v1
		p2 += v2
		p3 += v3
		p4 += v4
		//log.Printf("%d: %d, %d, %d, %d", i+1, p1, p2, p3, p4)
		if p1 == s1 && p2 == s2 && p3 == s3 && p4 == s4 {
			// Add 2 to the iteration. 1 for the initial state
			// and 1 because we're done with the current iteration
			// and haven't incremented
			return i + 2, nil
		}
	}
	return 0, fmt.Errorf("no cycle found")
}

// greatest common divisor (GCD) via Euclidean algorithm
func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// find Least Common Multiple (LCM) via GCD
func LCM(a, b int, integers ...int) int {
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

func part2(inputFile string) error {
	//part2Logger := log.New(os.Stderr, "P2: ", log.Ldate|log.Ltime|log.Lshortfile)
	moons, err := parseInput(inputFile)
	if err != nil {
		return err
	}
	//part2Logger.Printf("Loaded %d moons", len(moons))
	limit := 1000000
	cycleX, err := findCycle(moons[0].Position.x, moons[1].Position.x,
		moons[2].Position.x, moons[3].Position.x, limit)
	if err != nil {
		return err
	}
	//part2Logger.Printf("X cycle: %d", cycleX)

	cycleY, err := findCycle(moons[0].Position.y, moons[1].Position.y,
		moons[2].Position.y, moons[3].Position.y, limit)
	if err != nil {
		return err
	}
	//part2Logger.Printf("Y cycle: %d", cycleY)

	cycleZ, err := findCycle(moons[0].Position.z, moons[1].Position.z,
		moons[2].Position.z, moons[3].Position.z, limit)
	if err != nil {
		return err
	}
	//part2Logger.Printf("Z cycle: %d", cycleZ)

	answer := LCM(cycleX, cycleY, cycleZ)
	fmt.Printf("Part 2: %d\n", answer)

	return nil
}

func main() {
	inputFile := "input.txt"
	//inputFile = "test-input1.txt"
	err := part1(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	err = part2(inputFile)
	if err != nil {
		log.Fatal(err)
	}
}
