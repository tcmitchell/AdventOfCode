package main

import (
	"../aoc"
	"fmt"
	"log"
	"strings"
)

type Point struct {
	x, y int
}

type Room [][]string

type NeighborFunc func(room Room, r, c int) []Point

// Load a room from file. Rooms contain either 'L' or '.',
// representing chair or floor respectively.
func loadRoom(filename string) (Room, error) {
	rows, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	room := make([][]string, len(rows))
	// Split string into parts - are these strings? Or runes?
	for i, row := range rows {
		room[i] = strings.Split(row, "")
	}
	return room, nil
}

// Generate the list of neighbors for a given location
// in the room.
func p1NeighborsOf(room Room, r, c int) []Point {
	height := len(room)
	width := len(room[0])
	neighborPoints := make([]Point, 0)
	for y := r - 1; y < r+2; y++ {
		for x := c - 1; x < c+2; x++ {
			if y < 0 || y >= height {
				// Skip y if out of bounds
				continue
			}
			if x < 0 || x >= width {
				// Skip x if out of bounds
				continue
			}
			if y == r && x == c {
				// Skip the point itself
				continue
			}
			neighborPoints = append(neighborPoints, Point{x, y})
		}
	}
	return neighborPoints
}

// Generate the list of neighbor points for each location
// in the room. Do this one time, then use them during
// room evolution.
func neighborPoints(room Room, nFunc NeighborFunc) [][][]Point {
	height := len(room)
	width := len(room[0])
	neighbors := make([][][]Point, height)
	for r := 0; r < height; r++ {
		neighbors[r] = make([][]Point, width)
		for c := 0; c < width; c++ {
			neighbors[r][c] = nFunc(room, r, c)
		}
	}
	return neighbors
}

func occupiedNeighbors(r, c int, room Room, neighbors [][][]Point) int {
	count := 0
	for _, pt := range neighbors[r][c] {
		if room[pt.y][pt.x] == "#" {
			count++
		}
	}
	return count
}

func evolveRoom(room Room, neighbors [][][]Point, occupiedLimit int) (Room, int) {
	height := len(room)
	width := len(room[0])
	result := make(Room, height)
	changed := 0
	for r := 0; r < height; r++ {
		result[r] = make([]string, width)
		for c := 0; c < width; c++ {
			if room[r][c] == "." {
				result[r][c] = "."
				continue
			}
			occupied := occupiedNeighbors(r, c, room, neighbors)
			if room[r][c] == "L" && occupied == 0 {
				result[r][c] = "#"
				changed++
			} else if room[r][c] == "#" && occupied >= occupiedLimit {
				result[r][c] = "L"
				changed++
			} else {
				result[r][c] = room[r][c]
			}
		}
	}
	return result, changed
}

//func printRoom(room Room) {
//	for r := 0; r < len(room); r++ {
//		for c := 0; c < len(room[r]); c++ {
//			fmt.Print(room[r][c])
//		}
//		fmt.Println()
//	}
//}

func countOccupied(room Room) int {
	occupied := 0
	for r := 0; r < len(room); r++ {
		for c := 0; c < len(room[r]); c++ {
			if room[r][c] == "#" {
				occupied++
			}
		}
	}
	return occupied
}

func part1(filename string) (int, error) {
	room, err := loadRoom(filename)
	if err != nil {
		return 0, err
	}
	neighbors := neighborPoints(room, p1NeighborsOf)
	//for r := 0; r < len(room); r++ {
	//	for c := 0; c < len(room[r]); c++ {
	//		log.Printf("%d, %d: %v\n", r, c, neighbors[r][c])
	//	}
	//	log.Println()
	//}
	changes := -1
	i := 1
	for ; changes != 0; i++ {
		room, changes = evolveRoom(room, neighbors, 4)
	}
	//printRoom(room)
	//log.Printf("Detected %d changes at iteration %d", changes, i)
	return countOccupied(room), nil
}

func p2ClosestNeighbor(room Room, r, c, rStep, cStep int) (Point, error) {
	height := len(room)
	width := len(room[0])
	for y, x := r+rStep, c+cStep; 0 <= y && y < height && 0 <= x && x < width; y, x = y+rStep, x+cStep {
		if room[y][x] != "." {
			return Point{x, y}, nil
		}
	}
	//if rStep == 0 {
	//	for x := c + cStep; 0 <= x && x < width; x += cStep {
	//		if room[r][x] != "." {
	//			return Point{x, r}, nil
	//		}
	//	}
	//} else if cStep == 0 {
	//	for y := r + rStep; 0 <= y && y < height; y += rStep {
	//		if room[y][c] != "." {
	//			return Point{c, y}, nil
	//		}
	//	}
	//} else {
	//	for y := r + rStep; 0 <= y && y < height; y += rStep {
	//		for x := c + cStep; 0 <= x && x < width; x += cStep {
	//			if room[x][y] != "." {
	//				return Point{x, y}, nil
	//			}
	//		}
	//	}
	//}
	return Point{}, fmt.Errorf("no neighbor found")
}

// Generate the list of neighbors for a given location
// in the room. Run rays in all 8 directions to find the
// closest chair locations.
func p2NeighborsOf(room Room, r, c int) []Point {
	neighborPoints := make([]Point, 0)
	// North
	pt, err := p2ClosestNeighbor(room, r, c, -1, 0)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// Northeast
	pt, err = p2ClosestNeighbor(room, r, c, -1, 1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// East
	pt, err = p2ClosestNeighbor(room, r, c, 0, 1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// Southeast
	pt, err = p2ClosestNeighbor(room, r, c, 1, 1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// South
	pt, err = p2ClosestNeighbor(room, r, c, 1, 0)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// Southwest
	pt, err = p2ClosestNeighbor(room, r, c, 1, -1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// West
	pt, err = p2ClosestNeighbor(room, r, c, 0, -1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	// Northwest
	pt, err = p2ClosestNeighbor(room, r, c, -1, -1)
	if err == nil {
		neighborPoints = append(neighborPoints, pt)
	}
	return neighborPoints
}

func part2(filename string) (int, error) {
	room, err := loadRoom(filename)
	if err != nil {
		return 0, err
	}
	neighbors := neighborPoints(room, p2NeighborsOf)
	//printRoom(room)
	//for r := 0; r < len(room); r++ {
	//	for c := 0; c < len(room[r]); c++ {
	//		log.Printf("%d, %d: %v\n", r, c, neighbors[r][c])
	//	}
	//	log.Println()
	//}
	changes := -1
	i := 1
	for ; changes != 0; i++ {
		room, changes = evolveRoom(room, neighbors, 5)
		//log.Printf("Iteration %d had %d changes", i, changes)
		//printRoom(room)
	}
	//log.Printf("Detected %d changes at iteration %d", changes, i)
	return countOccupied(room), nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
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
