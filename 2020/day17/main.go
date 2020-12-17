package main

import (
	"../aoc"
	"fmt"
	"log"
	"strings"
)

var Active = "#"
var Inactive = "."

type Point3D struct {
	x, y, z int
}

func (p Point3D) Neighbors() []Point3D {
	result := make([]Point3D, 0)
	for x := p.x - 1; x <= p.x+1; x++ {
		for y := p.y - 1; y <= p.y+1; y++ {
			for z := p.z - 1; z <= p.z+1; z++ {
				if x == p.x && y == p.y && z == p.z {
					continue
				}
				result = append(result, Point3D{x, y, z})
			}
		}
	}
	return result
}

type Grid struct {
	Points                             map[Point3D]string
	MinX, MaxX, MinY, MaxY, MinZ, MaxZ int
	Neighbors                          map[Point3D][]Point3D
}

func NewGrid() *Grid {
	var grid Grid
	grid.Points = make(map[Point3D]string)
	grid.Neighbors = make(map[Point3D][]Point3D)
	return &grid
}

func (g *Grid) GetNeighbors(p Point3D) []Point3D {
	n, ok := g.Neighbors[p]
	if !ok {
		// Not already in the map, so generate the neighbors
		n = p.Neighbors()
		g.Neighbors[p] = n
	}
	return n
}

func (g *Grid) CountActiveNeighbors(p Point3D) int {
	result := 0
	for _, n := range g.GetNeighbors(p) {
		if g.Points[n] == Active {
			result += 1
		}
	}
	return result
}

func (g *Grid) CountActiveCells() int {
	result := 0
	for _, s := range g.Points {
		if s == Active {
			result++
		}
	}
	return result
}

func loadGrid(filename string) (*Grid, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	grid := NewGrid()
	maxX := 0
	maxY := 0
	for y, line := range lines {
		if y > maxY {
			maxY = y
		}
		for x, state := range strings.Split(line, "") {
			point := Point3D{x, y, 0}
			grid.Points[point] = state
			if x > maxX {
				maxX = x
			}
		}
	}
	grid.MinX = 0
	grid.MaxX = maxX
	grid.MinY = 0
	grid.MaxY = maxY
	grid.MinZ = 0
	grid.MaxZ = 0
	return grid, nil
}

func RunCycle(grid *Grid) *Grid {
	result := NewGrid()
	result.MinX = grid.MinX - 1
	result.MaxX = grid.MaxX + 1
	result.MinY = grid.MinY - 1
	result.MaxY = grid.MaxY + 1
	result.MinZ = grid.MinZ - 1
	result.MaxZ = grid.MaxZ + 1
	result.Neighbors = grid.Neighbors
	for x := result.MinX; x <= result.MaxX; x++ {
		for y := result.MinY; y <= result.MaxY; y++ {
			for z := result.MinZ; z <= result.MaxZ; z++ {
				loc := Point3D{x, y, z}
				//log.Printf("%v: %s", loc, grid.Points[loc])
				activeNeighbors := grid.CountActiveNeighbors(loc)
				state := grid.Points[loc]
				if state == Active {
					if activeNeighbors == 2 || activeNeighbors == 3 {
						result.Points[loc] = Active
					} else {
						result.Points[loc] = Inactive
					}
				} else {
					if activeNeighbors == 3 {
						result.Points[loc] = Active
					} else {
						result.Points[loc] = Inactive
					}
				}
			}
		}
	}
	return result
}

func part1(filename string) (int, error) {
	grid, err := loadGrid(filename)
	if err != nil {
		return 0, err
	}
	//for point, state := range grid.Points {
	//	log.Printf("%v: %s", point, state)
	//}
	//for x := grid.MinX; x <= grid.MaxX; x++ {
	//	for y := grid.MinY; y <= grid.MaxY; y++ {
	//		for z := grid.MinZ; z <= grid.MaxZ; z++ {
	//			key := Point3D{x, y, z}
	//			log.Printf("%v: %s", key, grid.Points[key])
	//		}
	//	}
	//}
	for i := 0; i < 6; i++ {
		grid = RunCycle(grid)
		//active := grid.CountActiveCells()
		//log.Printf("Cycle %d: %d active cells", i + 1, active)
	}
	return grid.CountActiveCells(), nil
}

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	return len(lines), nil
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
