package main

import (
	"../aoc"
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

var HairColorRegex = regexp.MustCompile(`^#[\da-f]{6}$`)

var PassportIdRegex = regexp.MustCompile(`^\d{9}$`)

var EyeColors = map[string]string{
	"amb": "",
	"blu": "",
	"brn": "",
	"gry": "",
	"grn": "",
	"hzl": "",
	"oth": "",
}

type Passport map[string]string

func (p Passport) String() string {
	elems := make([]string, len(p))
	i := 0
	for k, v := range p {
		elems[i] = fmt.Sprintf("%s=>%s", k, v)
		i++
	}
	return strings.Join(elems, " ")
}

func parsePassports(filename string) ([]Passport, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	result := make([]Passport, 0)
	passport := make(Passport)
	for i := 0; i < len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if line == "" {
			result = append(result, passport)
			passport = make(map[string]string)
			continue
		}
		fields := strings.Split(line, " ")
		for _, f := range fields {
			kv := strings.Split(f, ":")
			passport[kv[0]] = kv[1]
		}
	}
	// Add the passport we were working on
	result = append(result, passport)
	return result, nil
}

func validPassport(passport Passport) bool {
	requiredFields := []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
	for _, f := range requiredFields {
		_, ok := passport[f]
		if !ok {
			return false
		}
	}
	return true
}

func part1(filename string) (int, error) {
	passports, err := parsePassports(filename)
	if err != nil {
		return 0, err
	}
	//log.Printf("Loaded %d passports", len(passports))
	validCount := 0
	for _, p := range passports {
		//for k, v := range p {
		//	log.Printf("%s: %s\n", k, v)
		//}
		//log.Println()
		if validPassport(p) {
			validCount++
		}
	}
	// 212 is too low
	return validCount, nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	p1, err := part1(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d\n", p1)
	p2, err := part2(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}

func validIntString(v string, lo int, hi int) bool {
	value, err := strconv.Atoi(v)
	if err != nil {
		return false
	}
	return lo <= value && value <= hi
}
func validIntField(passport Passport, field string, lo int, hi int) bool {
	v, ok := passport[field]
	if !ok {
		return false
	}
	return validIntString(v, lo, hi)
}

func validByr(passport Passport) bool {
	return validIntField(passport, "byr", 1920, 2002)
}

func validIyr(passport Passport) bool {
	return validIntField(passport, "iyr", 2010, 2020)
}

func validEyr(passport Passport) bool {
	return validIntField(passport, "eyr", 2020, 2030)
}

func validHeight(passport Passport) bool {
	v, ok := passport["hgt"]
	if !ok {
		return false
	}
	if v[len(v)-2:] == "in" {
		return validIntString(v[0:len(v)-2], 59, 76)
	} else if v[len(v)-2:] == "cm" {
		return validIntString(v[0:len(v)-2], 150, 193)
	} else {
		return false
	}
}

func validHairColor(passport Passport) bool {
	return HairColorRegex.MatchString(passport["hcl"])
}

func validEyeColor(passport Passport) bool {
	_, ok := EyeColors[passport["ecl"]]
	return ok
}

func validPassportId(passport Passport) bool {
	return PassportIdRegex.MatchString(passport["pid"])
}

func validFields(passport Passport) bool {
	return validByr(passport) && validIyr(passport) && validEyr(passport) &&
		validHeight(passport) && validHairColor(passport) &&
		validEyeColor(passport) && validPassportId(passport)
}

func part2(filename string) (int, error) {
	passports, err := parsePassports(filename)
	if err != nil {
		return 0, err
	}
	//log.Printf("Loaded %d passports", len(passports))
	validCount := 0
	for _, p := range passports {
		if validPassport(p) && validFields(p) {
			validCount++
		}
	}
	return validCount, nil
}
