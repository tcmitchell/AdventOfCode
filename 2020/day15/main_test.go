package main

import "testing"

func TestPart1(t *testing.T) {
	//Given the starting numbers 1,3,2, the 2020th number spoken is 1.
	//Given the starting numbers 2,1,3, the 2020th number spoken is 10.
	//Given the starting numbers 1,2,3, the 2020th number spoken is 27.
	//Given the starting numbers 2,3,1, the 2020th number spoken is 78.
	//Given the starting numbers 3,2,1, the 2020th number spoken is 438.
	//Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
	var data = map[string]int{
		"0,3,6": 436,
		"1,3,2": 1,
		"2,1,3": 10,
		"1,2,3": 27,
		"2,3,1": 78,
		"3,2,1": 438,
		"3,1,2": 1836,
	}
	for input, expected := range data {
		actual, err := part1(input)
		if err != nil {
			t.Error(err)
		}
		if actual != expected {
			t.Errorf("expected %d, got %d", expected, actual)
		}
	}
}
