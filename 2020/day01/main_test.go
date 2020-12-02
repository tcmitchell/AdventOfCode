package main

import "testing"

func TestPart1Test1(t *testing.T) {
	expected := 514579
	actual, err := part1("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Test1(t *testing.T) {
	expected := 241861950
	actual, err := part2("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}
