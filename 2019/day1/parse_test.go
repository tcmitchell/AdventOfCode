package main

import (
	"fmt"
	"strconv"
	"testing"
)

// var smallStr = "35"
var smallStr = "129727"
var bigStr = "999999999999999"

func BenchmarkAtoi(b *testing.B) {
	for i := 0; i < b.N; i++ {
		val, _ := strconv.Atoi(smallStr)
		_ = val
	}
}

func BenchmarkAtoiParseInt(b *testing.B) {
	for i := 0; i < b.N; i++ {
		val, _ := strconv.ParseInt(smallStr, 0, 64)
		_ = val
	}
}

func BenchmarkSscan(b *testing.B) {
	var val int
	for i := 0; i < b.N; i++ {
		fmt.Sscan(smallStr, &val)
		// _ = val
	}
}
