package main

import (
	"testing"
)

func TestSize2(t *testing.T) {
	image := "../.#"
	expected := 2
	got := imageSize(image)
	if got != expected {
		t.Errorf("imageSize returned %d, expected %d", got, expected)
	}
}

func TestSize3(t *testing.T) {
	image := ".#./..#/###"
	expected := 3
	got := imageSize(image)
	if got != expected {
		t.Errorf("imageSize returned %d, expected %d", got, expected)
	}
}

func TestSize4(t *testing.T) {
	image := "#..#/..../..../#..#"
	expected := 4
	got := imageSize(image)
	if got != expected {
		t.Errorf("imageSize returned %d, expected %d", got, expected)
	}
}

func TestFlip2(t *testing.T) {
	image := "../.#"
	expected := ".#/.."
	got, err := flipImage(image)
	if err != nil {
		t.Errorf("flipImage error: %s", err)
	} else if got != expected {
		t.Errorf("flipImage returned %s, expected %s", got, expected)
	}
}

func TestFlip3(t *testing.T) {
	image := ".#./..#/###"
	expected := "###/..#/.#."
	got, err := flipImage(image)
	if err != nil {
		t.Errorf("flipImage error: %s", err)
	} else if got != expected {
		t.Errorf("flipImage returned %s, expected %s", got, expected)
	}
}

func TestFlip4(t *testing.T) {
	image := "#..#/..../..../#..#"
	_, err := flipImage(image)
	if err == nil {
		t.Errorf("flipImage expected error on size 4")
	}
}

func TestRotate2(t *testing.T) {
	image := "../.#"
	expected := "../#."
	got, err := rotateImage(image)
	if err != nil {
		t.Errorf("rotateImage error: %s", err)
	} else if got != expected {
		t.Errorf("rotateImage returned %s, expected %s", got, expected)
	}
}

func TestRotate3(t *testing.T) {
	image := ".#./..#/###"
	expected := "#../#.#/##."
	got, err := rotateImage(image)
	if err != nil {
		t.Errorf("rotateImage error: %s", err)
	} else if got != expected {
		t.Errorf("rotateImage returned %s, expected %s", got, expected)
	}
}

func TestRotate4(t *testing.T) {
	image := "#..#/..../..../#..#"
	_, err := rotateImage(image)
	if err == nil {
		t.Errorf("rotateImage expected error on size 4")
	}
}

func TestPermute2(t *testing.T) {
	image := "../.#"
	expected := []string{
		// Rotations
		"../.#", "../#.", "#./..", ".#/..",
		// Flipped rotations
		".#/..", "../.#", "../#.", "#./..",
	}
	got, err := permuteImage(image)
	if err != nil {
		t.Errorf("permuteImage error: %s", err)
		return
	}
	gotLen := len(got)
	expectedLen := len(expected)
	if gotLen != expectedLen {
		t.Errorf("permuteImage returned %d items, expected %d", gotLen, expectedLen)
	}
	for i := range expected {
		if expected[i] != got[i] {
			t.Errorf("permuteImage got %s at position %d, expected %s", got[i], i, expected[i])
		}
	}
}

func TestPermute3(t *testing.T) {
	image := ".#./..#/###"
	expected := []string{
		// Rotations
		".#./..#/###", "#../#.#/##.", "###/#../.#.", ".##/#.#/..#",
		// Flipped rotations
		"###/..#/.#.", "..#/#.#/.##", ".#./#../###", "##./#.#/#..",
	}
	got, err := permuteImage(image)
	if err != nil {
		t.Errorf("permuteImage error: %s", err)
		return
	}
	gotLen := len(got)
	expectedLen := len(expected)
	if gotLen != expectedLen {
		t.Errorf("permuteImage returned %d items, expected %d", gotLen, expectedLen)
	}
	for i := range expected {
		if expected[i] != got[i] {
			t.Errorf("permuteImage got %s at position %d, expected %s", got[i], i, expected[i])
		}
	}
}

func TestPermute4(t *testing.T) {
	image := "#..#/..../..../#..#"
	_, err := permuteImage(image)
	if err == nil {
		t.Errorf("permuteImage expected error on size 4")
	}
}
