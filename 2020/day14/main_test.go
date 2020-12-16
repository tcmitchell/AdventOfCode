package main

import "testing"

func TestPart1Test1(t *testing.T) {
	var expected int64 = 165
	actual, err := part1("test-input1.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart1Input(t *testing.T) {
	var expected int64 = 15172047086292
	actual, err := part1("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Test2(t *testing.T) {
	var expected int64 = 208
	actual, err := part2("test-input2.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestPart2Input(t *testing.T) {
	var expected int64 = 4197941339968
	actual, err := part2("input.txt")
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

func TestBits36(t *testing.T) {
	expected := "000000000000000000000000000000000001"
	actual := bits36(1)
	if actual != expected {
		t.Errorf("expected %s, got %s", expected, actual)
	}
}

func TestPow(t *testing.T) {
	expected := 4
	actual := pow(2, 2)
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
	expected = 8
	actual = pow(2, 3)
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}
