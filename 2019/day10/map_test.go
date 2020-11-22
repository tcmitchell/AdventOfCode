package main

import (
	"testing"
)

func testPart1(t *testing.T, mapFile string, expectedCount, expectedX, expectedY int) {
	aMap, err := loadAsteroidMap(mapFile)
	if err != nil {
		t.Fatal(err)
	}
	// fmt.Print(aMap)
	losAsteroid, losCount, err := part1(aMap)
	if err != nil {
		t.Fatal(err)
	}
	if losCount != expectedCount {
		t.Errorf("Part 1 count = %d, expected %d", losCount, expectedCount)
	}
	if losAsteroid.x != expectedX || losAsteroid.y != expectedY {
		t.Errorf("Expected asteroid (%d, %d), got (%d, %d)",
			expectedX, expectedY, losAsteroid.x, losAsteroid.y)
	}
}

func TestInputMap(t *testing.T) {
	mapFile := "input.txt"
	expectedCount := 326
	expectedX := 22
	expectedY := 28
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
}

func TestMap1(t *testing.T) {
	mapFile := "test1.txt"
	expectedX := 3
	expectedY := 4
	expectedCount := 8
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
}

func TestMap2(t *testing.T) {
	mapFile := "test2.txt"
	expectedX := 5
	expectedY := 8
	expectedCount := 33
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
}

func TestMap3(t *testing.T) {
	mapFile := "test3.txt"
	expectedX := 1
	expectedY := 2
	expectedCount := 35
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
}

func TestMap4(t *testing.T) {
	mapFile := "test4.txt"
	expectedX := 6
	expectedY := 3
	expectedCount := 41
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
}

func TestMap5(t *testing.T) {
	mapFile := "test5.txt"
	expectedX := 11
	expectedY := 13
	expectedCount := 210
	testPart1(t, mapFile, expectedCount, expectedX, expectedY)
	// TODO: part 2 testing
}
