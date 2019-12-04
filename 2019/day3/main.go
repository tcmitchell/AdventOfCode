package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

func loadWirePaths(filename string) ([]string, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	data := strings.TrimSpace(string(bytes))
	lines := strings.Split(data, "\n")
	return lines, nil
}

func parseSegment(x, y int, wireSegment string) (int, int, error) {
	dir := wireSegment[0]
	length, err := strconv.Atoi(wireSegment[1:])
	if err != nil {
		return 0, 0, err
	}
	switch dir {
	case 'U':
		// fmt.Printf("%d, %d -> %d, %d\n", x, y, x, y+length)
		return x, y + length, nil
	case 'D':
		// fmt.Printf("%d, %d -> %d, %d\n", x, y, x, y-length)
		return x, y - length, nil
	case 'R':
		// fmt.Printf("%d, %d -> %d, %d\n", x, y, x+length, y)
		return x + length, y, nil
	case 'L':
		// fmt.Printf("%d, %d -> %d, %d\n", x, y, x-length, y)
		return x - length, y, nil
	default:
		return 0, 0, fmt.Errorf("Unknown direction %d", dir)
	}
}

func pathToSegments(path []string) ([]*Segment, error) {
	var x1, y1 int
	result := make([]*Segment, len(path))
	for i, p := range path {
		x2, y2, err := parseSegment(x1, y1, p)
		if err != nil {
			return nil, err
		}
		result[i], err = NewSegment(x1, y1, x2, y2)
		if err != nil {
			return nil, err
		}
		x1, y1 = x2, y2
	}
	return result, nil
}

// AbsInt yields the absolute value of an int
func AbsInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// // ManhattanDistance computes the manhattan distance between two points
// func ManhattanDistance(x1, y1, x2, y2 int) int {
// 	return int(AbsInt(x2-x1) + AbsInt(y2-y1))
// }

func part1(puzzleInput string) error {
	wirePaths, err := loadWirePaths(puzzleInput)
	if err != nil {
		return err
	}
	path1, err := pathToSegments(strings.Split(wirePaths[0], ","))
	if err != nil {
		return err
	}
	path2, err := pathToSegments(strings.Split(wirePaths[1], ","))
	if err != nil {
		return err
	}
	closest := math.MaxInt64
	for _, seg2 := range path2 {
		for _, seg1 := range path1 {
			foo, x, y := seg1.intersects(seg2)
			if foo {
				fmt.Printf("%s intersects %s\n", seg2, seg1)
				md := AbsInt(x) + AbsInt(y)
				fmt.Printf("Manhattan distance is %d\n", md)
				if md < closest {
					closest = md
				}
			}
		}
	}
	fmt.Printf("Part 1: %d", closest)
	return nil
}

func part2(puzzleInput string) {
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
