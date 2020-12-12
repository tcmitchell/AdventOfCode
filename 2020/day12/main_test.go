package main

import "testing"

func TestPart1TestInput(t *testing.T) {
	expected := 25
	actual, err := part1("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart1Input(t *testing.T) {
	expected := 2458
	actual, err := part1("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2TestInput(t *testing.T) {
	expected := 286
	actual, err := part2("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Input(t *testing.T) {
	expected := 145117
	actual, err := part2("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}
