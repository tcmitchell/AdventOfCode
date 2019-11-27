package main

import (
	"bufio"
	"fmt"
	"math"
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
		// fmt.Printf("%s -> %s\n", parts[0], parts[1])
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

// Break up an image into smaller images, each of the given size
func breakUpImage(image string, size int) ([]string, error) {
	// fmt.Printf("bUI  input: %s\n", image)
	// Break the image up into pixels
	rows := strings.Split(image, "/")
	pixels := make([][]string, len(rows))
	for i, row := range rows {
		// fmt.Println(row)
		pixels[i] = strings.Split(row, "")
	}
	result := make([]string, 0)
	for r := 0; r < imageSize(image); r += size {
		for c := 0; c < imageSize(image); c += size {
			subImage := make([]string, size)
			for i := 0; i < size; i++ {
				// fmt.Printf("r=%d; c=%d; i=%d\n", r, c, i)
				subImage[i] = strings.Join(pixels[r+i][c:c+size], "")
				// fmt.Printf("subImage[%d]: %s\n", i, subImage[i])
			}
			result = append(result, strings.Join(subImage, "/"))
		}
	}

	// for _, img := range result {
	// 	fmt.Println(img)
	// }

	return result, nil
}

// Assemble the sub images into a composite image
func assembleImage(images []string) (string, error) {
	// get the size of the first image
	imgSize := imageSize(images[0])
	// verify all the images are the same size?
	splitImages := make([][]string, len(images))
	for i, img := range images {
		splitImages[i] = strings.Split(img, "/")
	}
	// determine dimensions of final image
	destSize := int(math.Sqrt(float64(len(images))))
	// fmt.Println("destSize =", destSize)
	destRows := destSize * imgSize
	// fmt.Println("destRows =", destRows)
	rows := make([]string, destRows)
	r := 0
	for img := 0; img < len(images); img += destSize {
		for c := 0; c < imgSize; c++ {
			for i := 0; i < destSize; i++ {
				// Build rows
				// fmt.Printf("img: %d; i: %d; c: %d\n", img, i, c)
				// fmt.Printf("rows[%d] = splitImages[%d][%d]\n", r, img+i, c)
				rows[r] += splitImages[img+i][c]
			}
			r++
		}
	}
	image := strings.Join(rows, "/")
	fmt.Println("assembleImage:", image)
	return image, nil
}

// Enhances an image by breaking it up into subimages, enhancing each
// subimage, then assembling the subimages into a whole.
func enhanceImage(rules map[string]string, image string) (string, error) {
	size := imageSize(image)
	subimageSize := 0
	if math.Mod(float64(size), 2) == 0 {
		subimageSize = 2
	} else if math.Mod(float64(size), 3) == 0 {
		subimageSize = 3
	} else {
		fmt.Errorf("%d is not divisible by 2 or 3", size)
	}
	imgs, err := breakUpImage(image, subimageSize)
	if err != nil {
		return "", err
	}
	for i, img := range imgs {
		newImage, err := lookUpImage(rules, img)
		if err != nil {
			return "", err
		}
		imgs[i] = newImage
	}
	return assembleImage(imgs)
}

func part1() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	rules := loadRules(c)
	// for rule := range rules {
	// 	fmt.Printf("%s to %s\n", rule, rules[rule])
	// }
	var err error
	image := ".#./..#/###"
	for i := 0; i < 5; i++ {
		image, err = enhanceImage(rules, image)
		if err != nil {
			panic(err)
		}
	}
	countOn := 0
	for _, row := range strings.Split(image, "/") {
		fmt.Println(row)
		countOn += strings.Count(row, "#")
	}
	fmt.Printf("%d pixels are on", countOn)
	return

	image2, err := lookUpImage(rules, image)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Image 2: %s\n", image2)
	fmt.Printf("Image 2 size: %d\n", imageSize(image2))
	imgs, err := breakUpImage(image2, 2)
	if err != nil {
		panic(err)
	}
	for i, img := range imgs {
		fmt.Printf("Subimage %d: %s\n", i, img)
		imgs[i], err = lookUpImage(rules, img)
		if err != nil {
			panic(err)
		}
	}
	for i, img := range imgs {
		fmt.Printf("Enhanced Subimage %d: %s\n", i, img)
	}
	assembleImage(imgs)
}

func main() {
	part1()
}
