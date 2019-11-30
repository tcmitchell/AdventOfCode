package main

import "fmt"

type bridge struct {
	components []component
	stockpile  []component
	endPort    int
	done       bool
}

func (b bridge) String() string {
	return fmt.Sprintf("%q (ep:%d; done:%t; sp:%q)", b.components, b.endPort, b.done, b.stockpile)
}

func makeBridge(c component, stockpile []component) *bridge {
	components := make([]component, 1)
	components[0] = c
	newBridge := bridge{components, stockpile, otherPort(c, 0), false}
	return &newBridge
}

func copyBridge(b bridge) *bridge {
	newBridge := bridge{copyComponents(b.components),
		copyComponents(b.stockpile),
		b.endPort, false}
	return &newBridge
}

func (b *bridge) addComponent(c component) {
	// Add to components
	b.components = append(b.components, c)
	// Remove from stockpile
	b.stockpile = removeItem(b.stockpile, c)
	// Update endPort
	b.endPort = otherPort(c, b.endPort)
}

func (b bridge) strength() int {
	strength := 0
	for _, c := range b.components {
		strength += c.portA + c.portB
	}
	return strength
}
