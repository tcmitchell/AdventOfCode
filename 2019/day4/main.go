package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func loadInput(filename string) (int, int, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, nil, err
	}
	data := strings.TrimSpace(string(bytes))
	hiloStrings := strings.Split(data, "-")
	hilo := make([][]int, len(hiloStrings))
	for i, x := range hiloStrings {
		hilo[i] = make([]int, 6)
		for j, y := range strings.Split(x, "") {
			hilo[i][j], err = strconv.Atoi(y)
			if err != nil {
				return nil, nil, err
			}
		}
	}
	return hilo[0], hilo[1], nil
}

func passwdDigits(passwd int) ([]int, error) {
	result := make([]int, 0)
	for d := range strings.Split(string(passwd), "") {
		digit, err := strconv.Atoi(d)
		if err != nil {
			return nil, err
		}
		result = append(result, digit)
	}
	return result, nil
}

func part1(puzzleInput string) error {
	lo, hi, err := loadInput(puzzleInput)
	if err != nil {
		return err
	}
	fmt.Printf("lo: %s\n", passwdDigits(lo))
	fmt.Printf("hi: %s\n", passwdDigits(hi))
	return nil
}

func part2(puzzleInput string) error {
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
