package main

import "testing"

//Part 1:
//Part 2:

func TestPart1Test1(t *testing.T) {
	var expected int = 112
	actual, err := part1("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart1Input(t *testing.T) {
	var expected int = 269
	actual, err := part1("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Test1(t *testing.T) {
	var expected int = 848
	actual, err := part2("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Input(t *testing.T) {
	var expected int = 1380
	actual, err := part2("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}
