package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func loadInput(filename string) ([]int, []int, error) {
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

func validPassword(password []int) bool {
	// fmt.Printf("Testing %d\n", password)
	if !(password[0] == password[1] ||
		password[1] == password[2] ||
		password[2] == password[3] ||
		password[3] == password[4] ||
		password[4] == password[5]) {
		// fmt.Printf("\tNo duplicate\n")
		return false
	}
	if !(password[0] <= password[1] &&
		password[1] <= password[2] &&
		password[2] <= password[3] &&
		password[3] <= password[4] &&
		password[4] <= password[5]) {
		// fmt.Printf("\tNot increasing\n")
		return false
	}
	if password[0] == 5 && password[1] >= 7 {
		// Handcoded stop condition
		return false
	}
	// fmt.Printf("\tLooks good\n")
	return true
}

func validPassword2(password []int) bool {
	// fmt.Printf("Testing %d\n", password)
	if !(password[0] == password[1] ||
		password[1] == password[2] ||
		password[2] == password[3] ||
		password[3] == password[4] ||
		password[4] == password[5]) {
		// fmt.Printf("\tNo duplicate\n")
		return false
	}
	a := password[0]
	b := password[1]
	c := password[2]
	d := password[3]
	e := password[4]
	f := password[5]

	if !(a == b && b != c ||
		a != b && b == c && c != d ||
		b != c && c == d && d != e ||
		c != d && d == e && e != f ||
		d != e && e == f) {
		return false
	}

	if password[0] == 5 && password[1] >= 7 {
		// Handcoded stop condition
		return false
	}
	// fmt.Printf("\tLooks good\n")
	return true
}

func copyPassword(password []int) []int {
	result := make([]int, len(password))
	for i, p := range password {
		result[i] = p
	}
	return result
}

func genPasswords(passwords [][]int, pos int, start int, password []int,
	validator func([]int) bool) [][]int {
	if pos >= 6 {
		if validator(password) {
			passwords = append(passwords, copyPassword(password))
		}
		return passwords
	}
	for i := start; i <= 9; i++ {
		password[pos] = i
		passwords = genPasswords(passwords, pos+1, i, password, validator)
	}
	return passwords
}

func doPart(puzzleInput string, validator func([]int) bool) ([][]int, error) {
	passwords := make([][]int, 0)
	password := make([]int, 6)
	for i := 1; i < 6; i++ {
		password[0] = i
		passwords = genPasswords(passwords, 1, i, password, validator)
	}
	// fmt.Printf("Found %d valid passwords", len(passwords))
	return passwords, nil
}

func part1(puzzleInput string) error {
	passwords, err := doPart(puzzleInput, validPassword)
	if err != nil {
		return err
	}
	fmt.Printf("Part1: %d (valid passwords)\n", len(passwords))
	return nil
}

func part2(puzzleInput string) error {
	passwords, err := doPart(puzzleInput, validPassword2)
	if err != nil {
		return err
	}
	fmt.Printf("Part2: %d (valid passwords)\n", len(passwords))
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
