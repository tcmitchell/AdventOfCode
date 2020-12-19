package main

import (
	"log"
	"testing"
)

func TestP1ShuntingYard(t *testing.T) {
	line := "2 * 3 + (4 * 5)"
	expected := 26
	tokens, err := tokenize(line)
	if err != nil {
		t.Error(err)
	}
	tokens, err = p1ShuntingYard(tokens)
	if err != nil {
		t.Error(err)
	}
	log.Printf("%v", tokens)
	actual, err := p1EvalRpn(tokens)
	if err != nil {
		t.Error(err)
	}
	if actual != expected {
		t.Errorf("expected %d, got %d", expected, actual)
	}
}

//func TestP1EvalExpr(t *testing.T) {
//	var expected int = 26
//	actual, err := p1Eval("2 * 3 + (4 * 5)")
//	if err != nil {
//		t.Error(err)
//	}
//	if actual != expected {
//		t.Errorf("expected %d, got %d", expected, actual)
//	}
//}

//func TestPart1Input(t *testing.T) {
//	var expected int = 269
//	actual, err := part1("input.txt")
//	if err != nil {
//		t.Error(err)
//	}
//	if actual != expected {
//		t.Errorf("expected %d, got %d", expected, actual)
//	}
//}

//func TestPart2Test1(t *testing.T) {
//	var expected int = 848
//	actual, err := part2("test-input1.txt")
//	if err != nil {
//		t.Error(err)
//	}
//	if actual != expected {
//		t.Errorf("expected %d, got %d", expected, actual)
//	}
//}
//
//func TestPart2Input(t *testing.T) {
//	var expected int = 1380
//	actual, err := part2("input.txt")
//	if err != nil {
//		t.Error(err)
//	}
//	if actual != expected {
//		t.Errorf("expected %d, got %d", expected, actual)
//	}
//}
