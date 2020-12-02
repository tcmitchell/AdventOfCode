package aoc

import (
	"io/ioutil"
	"strconv"
	"strings"
)

func Strings2ints(input []string) ([]int, error) {
	result := make([]int, len(input))
	for i, item := range input {
		intItem, err := strconv.Atoi(item)
		if err != nil {
			return nil, err
		}
		result[i] = intItem
	}
	return result, nil
}

func ReadFileOfStrings(filename string) ([]string, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	input := strings.TrimSpace(string(bytes))
	lines := strings.Split(input, "\n")
	return lines, nil
}

// Reads the given file as a list of integers
func ReadFileOfInts(filename string) ([]int, error) {
	lines, err := ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	return Strings2ints(lines)
}
