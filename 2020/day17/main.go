package main

import (
	"../aoc"
	"fmt"
	"log"
	"strings"
)

var Active = "#"
var Inactive = "."

type Grid3D struct {
	Points                             map[aoc.Point3D]string
	MinX, MaxX, MinY, MaxY, MinZ, MaxZ int
	Neighbors                          map[aoc.Point3D][]aoc.Point3D
}

func NewGrid() *Grid3D {
	var grid Grid3D
	grid.Points = make(map[aoc.Point3D]string)
	grid.Neighbors = make(map[aoc.Point3D][]aoc.Point3D)
	return &grid
}

func (g *Grid3D) GetNeighbors(p aoc.Point3D) []aoc.Point3D {
	n, ok := g.Neighbors[p]
	if !ok {
		// Not already in the map, so generate the neighbors
		n = p.Neighbors()
		g.Neighbors[p] = n
	}
	return n
}

func (g *Grid3D) CountActiveNeighbors(p aoc.Point3D) int {
	result := 0
	for _, n := range g.GetNeighbors(p) {
		if g.Points[n] == Active {
			result += 1
		}
	}
	return result
}

func (g *Grid3D) CountActiveCells() int {
	result := 0
	for _, s := range g.Points {
		if s == Active {
			result++
		}
	}
	return result
}

func loadGrid3D(filename string) (*Grid3D, error) {
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
			point := aoc.Point3D{X: x, Y: y}
			grid.Points[point] = state
			if x > maxX {
				maxX = x
			}
		}
	}
	grid.MaxX = maxX
	grid.MaxY = maxY
	return grid, nil
}

func RunCycle(grid *Grid3D) *Grid3D {
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
				loc := aoc.Point3D{X: x, Y: y, Z: z}
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
	grid, err := loadGrid3D(filename)
	if err != nil {
		return 0, err
	}
	for i := 0; i < 6; i++ {
		grid = RunCycle(grid)
	}
	return grid.CountActiveCells(), nil
}

type Grid4D struct {
	Points    map[aoc.Point4D]string
	Min       aoc.Point4D
	Max       aoc.Point4D
	Neighbors map[aoc.Point4D][]aoc.Point4D
}

func NewGrid4D() *Grid4D {
	var grid Grid4D
	grid.Points = make(map[aoc.Point4D]string)
	grid.Neighbors = make(map[aoc.Point4D][]aoc.Point4D)
	return &grid
}

func (g *Grid4D) GetNeighbors(p aoc.Point4D) []aoc.Point4D {
	n, ok := g.Neighbors[p]
	if !ok {
		// Not already in the map, so generate the neighbors
		n = p.Neighbors()
		g.Neighbors[p] = n
	}
	return n
}

func (g *Grid4D) CountActiveNeighbors(p aoc.Point4D) int {
	result := 0
	for _, n := range g.GetNeighbors(p) {
		if g.Points[n] == Active {
			result += 1
		}
	}
	return result
}

func (g *Grid4D) CountActiveCells() int {
	result := 0
	for _, s := range g.Points {
		if s == Active {
			result++
		}
	}
	return result
}

func loadGrid4D(filename string) (*Grid4D, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	grid := NewGrid4D()
	maxX := 0
	maxY := 0
	for y, line := range lines {
		if y > maxY {
			maxY = y
		}
		for x, state := range strings.Split(line, "") {
			point := aoc.Point4D{X: x, Y: y}
			grid.Points[point] = state
			if x > maxX {
				maxX = x
			}
		}
	}
	grid.Max.X = maxX
	grid.Max.Y = maxY
	return grid, nil
}

func RunCycle4D(grid *Grid4D) *Grid4D {
	result := NewGrid4D()
	result.Min.X = grid.Min.X - 1
	result.Max.X = grid.Max.X + 1
	result.Min.Y = grid.Min.Y - 1
	result.Max.Y = grid.Max.Y + 1
	result.Min.Z = grid.Min.Z - 1
	result.Max.Z = grid.Max.Z + 1
	result.Min.W = grid.Min.W - 1
	result.Max.W = grid.Max.W + 1
	result.Neighbors = grid.Neighbors
	for x := result.Min.X; x <= result.Max.X; x++ {
		for y := result.Min.Y; y <= result.Max.Y; y++ {
			for z := result.Min.Z; z <= result.Max.Z; z++ {
				//log.Printf("%v: %s", loc, grid.Points[loc])
				for w := result.Min.W; w <= result.Max.W; w++ {
					loc := aoc.Point4D{X: x, Y: y, Z: z, W: w}
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
	}
	return result
}

func part2(filename string) (int, error) {
	grid, err := loadGrid4D(filename)
	if err != nil {
		return 0, err
	}
	for i := 0; i < 6; i++ {
		grid = RunCycle4D(grid)
		//active := grid.CountActiveCells()
		//log.Printf("Cycle %d: %d active cells", i + 1, active)
	}
	return grid.CountActiveCells(), nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	filename = "test-input1.txt"
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
