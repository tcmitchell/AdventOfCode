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
		fmt.Printf("%d: %s\n", idx, row)
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
	fmt.Printf("Loaded %d moons\n", len(moons))
	for _, moon := range moons {
		fmt.Printf("%s\n", moon)
	}
	iters := 1000
	for iter := 0; iter < iters; iter++ {
		for j := 0; j < len(moons)-1; j++ {
			for k := j + 1; k < len(moons); k++ {
				computeGravity(moons[j], moons[k])
			}
		}
		applyVelocity(moons)
		fmt.Printf("----- After iteration %d -----\n", iter+1)
		for _, moon := range moons {
			fmt.Printf("%s\n", moon)
		}
		fmt.Println()
	}
	energy := computeEnergy(moons)
	fmt.Printf("Energy = %d\n", energy)
	return nil
}

func part2(inputFile string) error {
	moons, err := parseInput(inputFile)
	if err != nil {
		return err
	}
	fmt.Printf("Loaded %d moons", len(moons))
	return nil
}

func main() {
	fmt.Println("Hello, World!")
	inputFile := "input.txt"
	//inputFile = "test-input2.txt"
	err := part1(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	err = part2(inputFile)
	if err != nil {
		log.Fatal(err)
	}
}
