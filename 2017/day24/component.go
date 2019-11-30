package main

import (
	"fmt"
	"strconv"
	"strings"
)

type component struct {
	portA int
	portB int
}

func makeComponent(line string) (*component, error) {
	ports := strings.Split(line, "/")
	a, err := strconv.Atoi(ports[0])
	if err != nil {
		return nil, err
	}
	b, err := strconv.Atoi(ports[1])
	if err != nil {
		return nil, err
	}
	return &component{a, b}, nil
}

func (c component) String() string {
	return fmt.Sprintf("%d/%d", c.portA, c.portB)
}

func (c component) hasPort(port int) bool {
	return port == c.portA || port == c.portB
}

func otherPort(c component, p int) int {
	if c.portA == p {
		return c.portB
	}
	return c.portA
}
