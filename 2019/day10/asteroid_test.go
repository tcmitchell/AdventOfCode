package main

import "testing"

// The grid starts in the upper left corner at 0, 0.
// X increases to the right and Y increases down.

func TestQ1(t *testing.T) {
	a := asteroid{x: 3, y: 3}
	// Test less than half way across the quadrant
	a2 := asteroid{x: 4, y: 1}
	got := a.angle2asteroid(&a2)
	expectedLo := 0.0
	expectedHi := 45.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
	// Test half way across the quadrant
	a2 = asteroid{x: 4, y: 2}
	got = a.angle2asteroid(&a2)
	expected := 45
	if int(got) != expected {
		t.Errorf("Got %f, expected %d", got, expected)
	}
	// Test more than half way across the quadrant
	a2 = asteroid{x: 6, y: 2}
	got = a.angle2asteroid(&a2)
	expectedLo = 45.0
	expectedHi = 90.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
}

func TestQ2(t *testing.T) {
	a := asteroid{x: 3, y: 3}
	// Test less than half way across the quadrant
	a2 := asteroid{x: 6, y: 4}
	got := a.angle2asteroid(&a2)
	expectedLo := 90.0
	expectedHi := 135.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
	// Test half way across the quadrant
	a2 = asteroid{x: 4, y: 4}
	got = a.angle2asteroid(&a2)
	expected := 135
	if int(got) != expected {
		t.Errorf("Got %f, expected %d", got, expected)
	}
	// Test more than half way across the quadrant
	a2 = asteroid{x: 4, y: 6}
	got = a.angle2asteroid(&a2)
	expectedLo = 135.0
	expectedHi = 180.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
}

func TestQ3(t *testing.T) {
	a := asteroid{x: 3, y: 3}
	// Test less than half way across the quadrant
	a2 := asteroid{x: 2, y: 6}
	got := a.angle2asteroid(&a2)
	expectedLo := 180.0
	expectedHi := 225.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
	// Test half way across the quadrant
	a2 = asteroid{x: 2, y: 4}
	got = a.angle2asteroid(&a2)
	expected := 225
	if int(got) != expected {
		t.Errorf("Got %f, expected %d", got, expected)
	}
	// Test more than half way across the quadrant
	a2 = asteroid{x: 1, y: 4}
	got = a.angle2asteroid(&a2)
	expectedLo = 225.0
	expectedHi = 270.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
}

func TestQ4(t *testing.T) {
	a := asteroid{x: 3, y: 3}
	// Test less than half way across the quadrant
	a2 := asteroid{x: 1, y: 2}
	got := a.angle2asteroid(&a2)
	expectedLo := 270.0
	expectedHi := 315.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
	// Test half way across the quadrant
	a2 = asteroid{x: 2, y: 2}
	got = a.angle2asteroid(&a2)
	expected := 315
	if int(got) != expected {
		t.Errorf("Got %f, expected %d", got, expected)
	}
	// Test more than half way across the quadrant
	a2 = asteroid{x: 2, y: 1}
	got = a.angle2asteroid(&a2)
	expectedLo = 315.0
	expectedHi = 359.0
	if got < expectedLo || got > expectedHi {
		t.Errorf("Got %f expected between %f and %f",
			got, expectedLo, expectedHi)
	}
}

func TestVertical(t *testing.T) {
	a := asteroid{x: 22, y: 28}
	// Test vertical point
	a2 := asteroid{x: 22, y: 12}
	got := a.angle2asteroid(&a2)
	expected := 0.0
	if got != expected {
		t.Errorf("Got %f, expected %f", got, expected)
	}
}

func TestAngleEquality(t *testing.T) {
	a := asteroid{x: 3, y: 3}
	//
	a2 := asteroid{x: 4, y: 2}
	got2 := a.angle2asteroid(&a2)

	a3 := asteroid{x: 5, y: 1}
	got3 := a.angle2asteroid(&a3)

	if got2 != got3 {
		t.Errorf("Angles not equal: %f and %f", got2, got3)
	}
}

func TestDistance(t *testing.T) {
	a := asteroid{x: -1, y: 1}
	a2 := asteroid{x: 3, y: 4}
	got := a.dist2asteroid(&a2)
	expected := 5.0
	if got != expected {
		t.Errorf("Expected distance %f, got %f", expected, got)
	}
}
