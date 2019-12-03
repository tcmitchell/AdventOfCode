package main

import (
	"testing"
)

// Equal tells whether a and b contain the same elements.
// A nil argument is equivalent to an empty slice.
func intcodeEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

// 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
func TestRunProgram1(t *testing.T) {
	program := []int{1, 0, 0, 0, 99}
	expected := []int{2, 0, 0, 0, 99}
	got := runProgram(program)
	if !intcodeEqual(got, expected) {
		t.Errorf("Got output program %d, expected %d", got, expected)
	}
}

// 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
func TestRunProgram2(t *testing.T) {
	program := []int{2, 3, 0, 3, 99}
	expected := []int{2, 3, 0, 6, 99}
	got := runProgram(program)
	if !intcodeEqual(got, expected) {
		t.Errorf("Got output program %d, expected %d", got, expected)
	}
}

// 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
func TestRunProgram3(t *testing.T) {
	program := []int{2, 4, 4, 5, 99, 0}
	expected := []int{2, 4, 4, 5, 99, 9801}
	got := runProgram(program)
	if !intcodeEqual(got, expected) {
		t.Errorf("Got output program %d, expected %d", got, expected)
	}
}

// 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
func TestRunProgram4(t *testing.T) {
	program := []int{1, 1, 1, 4, 99, 5, 6, 0, 99}
	expected := []int{30, 1, 1, 4, 2, 5, 6, 0, 99}
	got := runProgram(program)
	if !intcodeEqual(got, expected) {
		t.Errorf("Got output program %d, expected %d", got, expected)
	}
}
