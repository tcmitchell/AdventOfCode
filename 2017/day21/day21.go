package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const maxX = uint(1000)
const maxY = uint(1000)

// ReadInputLines reads the input file line by line,
// passing each line to the given channel.
func ReadInputLines(infile string, c chan string) {
	f, err := os.Open(infile)
	if err != nil {
		panic("foo")
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		c <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	close(c)
}

func loadRules(c chan string) map[string]string {
	result := make(map[string]string)
	for rule := range c {
		// fmt.Println(rule)
		parts := strings.Split(rule, " => ")
		fmt.Printf("%s -> %s\n", parts[0], parts[1])
		result[parts[0]] = parts[1]
	}
	return result
}

func transformImage(image string, xform []int) (string, error) {
	exploded := strings.Split(image, "")
	result := make([]string, len(exploded))
	for i := 0; i < len(xform); i++ {
		result[i] = exploded[xform[i]]
	}
	return strings.Join(result, ""), nil
}

func rotateImage(image string) (string, error) {
	size := imageSize(image)
	if size == 2 {
		xform := []int{3, 0, 2, 4, 1}
		return transformImage(image, xform)
	}
	if size == 3 {
		xform := []int{8, 4, 0, 3, 9, 5, 1, 7, 10, 6, 2}
		return transformImage(image, xform)
	}
	return "", fmt.Errorf("Unknown image size %d", size)
}

func flipImage(image string) (string, error) {
	size := imageSize(image)
	if size == 2 {
		xform := []int{3, 4, 2, 0, 1}
		return transformImage(image, xform)
	}
	if size == 3 {
		xform := []int{8, 9, 10, 3, 4, 5, 6, 7, 0, 1, 2}
		return transformImage(image, xform)
	}
	return "", fmt.Errorf("Unknown image size %d", size)
}

func permuteImage(image string) ([]string, error) {
	var err error
	result := make([]string, 8)
	result[0] = image
	for i := 1; i < 4; i++ {
		result[i], err = rotateImage(result[i-1])
		if err != nil {
			return nil, err
		}
	}
	result[4], err = flipImage(image)
	if err != nil {
		return nil, err
	}
	for i := 5; i < 8; i++ {
		result[i], err = rotateImage(result[i-1])
		if err != nil {
			return nil, err
		}
	}
	return result, nil
}

func lookUpImage(rules map[string]string, image string) (string, error) {
	// Look up the image in the rules, rotating and flipping
	// the image as necessary to find the rule.
	newImage, ok := rules[image]
	if ok {
		return newImage, nil
	}
	// If the image as passed is not in the rules, permute
	// it, and try the permutations in turn. Skip the first
	// entry because it is the original image and we know
	// that's not in there.
	images, err := permuteImage(image)
	if err != nil {
		return "", err
	}
	for _, b := range images[1:] {
		newImage, ok := rules[b]
		if ok {
			return newImage, nil
		}
	}
	return "", fmt.Errorf("No match for %s", image)
}

// Determine the size of a image
func imageSize(image string) int {
	return len([]rune(strings.Split(image, "/")[0]))
}

func part1() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	rules := loadRules(c)
	for rule := range rules {
		fmt.Printf("%s to %s\n", rule, rules[rule])
	}
	image := ".#./..#/###"
	image2, err := lookUpImage(rules, image)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Image 2: %s\n", image2)
	fmt.Printf("Image 2 size: %d\n", imageSize(image2))
}

func main() {
	part1()
}
