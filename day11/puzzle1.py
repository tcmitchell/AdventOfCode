#!/usr/bin/env python

import sys

class Type(object):
    Microchip = 'Microchip'
    Generator = 'Generator'


class Element(object):

    def __init__(self, element):
        self.element = element
        self.short_name = element[0]

    def __deepcopy__(self, memo):
        return self


Element.Strontium = Element('Strontium')
Element.Plutonium = Element('Plutonium')
Element.Thulium = Element('Thulium')
Element.Ruthenium = Element('Ruthenium')
Element.Curium = Element('Curium')
Element.Hydrogen = Element('Hydrogen')
Element.Lithium = Element('Lithium')

class Microchip(object):

    def __init__(self, material):
        self.type = Type.Microchip
        self.material = material

    def __deepcopy__(self, memo):
        return self


class Generator(object):

    def __init__(self, material):
        self.type = Type.Generator
        self.material = material

    def __deepcopy__(self, memo):
        return self


class Floor(object):

    def __init__(self, i):
        self.number = i
        self.items = []

    def is_legal(self):
        "Determines if the items on the floor are legal together"
        pass

    def extend(self, thing):
        self.items.extend(thing)


class WorldState(object):

    def __init__(self, numFloors):
        self.floors = [Floor(i) for i in range(numFloors)]
        self.children = []
        self.elevator = 0

    def is_legal(self):
        "This world state is legal if all the floors in the state are legal"
        return not [f.is_legal() for f in self.floors].count(False)


def test_world_state():
    ws = WorldState(4)
    # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    ws.floors[0].extend([Microchip(Element.Hydrogen), Microchip(Element.Lithium)])
    # The second floor contains a hydrogen generator.
    ws.floors[1].extend([Generator(Element.Hydrogen)])
    # The third floor contains a lithium generator.
    ws.floors[2].extend([Generator(Element.Lithium)])
    # The fourth floor contains nothing relevant.
    return ws


def main():
    # Construct the initial world state
    world_state = test_world_state()
    #
    # Generate a set of possible moves from this state.
    # For each 1 or 2 items that can move from the current floor
    #     to another floor (up unless the elevator is at the top floor)
    #   Deep copy this world state
    #   Make the corresponding move
    #   Test for legality
    #   If legal, add to set of children states
    # Finally, set the list of children to the legal states
    #


if __name__ == '__main__':
    main()
