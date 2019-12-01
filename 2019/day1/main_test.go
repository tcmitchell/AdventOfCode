package main

import (
	"testing"
)

// For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
// For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
// For a mass of 1969, the fuel required is 654.
// For a mass of 100756, the fuel required is 33583.

func TestFuelRequired(t *testing.T) {
	input := []int{12, 14, 1969, 100756}
	expected := []int{2, 2, 654, 33583}
	for i, in := range input {
		got := fuelRequired(float64(in))
		if got != expected[i] {
			t.Errorf("fuelRequired returned %d, expected %d", got, expected[i])
		}
	}
}
