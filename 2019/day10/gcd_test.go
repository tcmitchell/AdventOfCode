package main

import "testing"

func TestGcd1(t *testing.T) {
	expected := 2
	got := gcd(12, 14)
	if got != expected {
		t.Errorf("gcd returned %d, expected %d", got, expected)
	}
}

func TestGcd2(t *testing.T) {
	expected := 21
	got := gcd(252, 105)
	if got != expected {
		t.Errorf("gcd returned %d, expected %d", got, expected)
	}
	got = gcd(105, 252)
	if got != expected {
		t.Errorf("gcd returned %d, expected %d", got, expected)
	}
}

func TestGcd3(t *testing.T) {
	expected := 1
	got := gcd(253, 105)
	if got != expected {
		t.Errorf("gcd returned %d, expected %d", got, expected)
	}
	got = gcd(105, 253)
	if got != expected {
		t.Errorf("gcd returned %d, expected %d", got, expected)
	}
}
