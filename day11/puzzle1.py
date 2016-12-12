#!/usr/bin/env python

import copy
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

    def __str__(self):
        return self.material.short_name + 'M'

    def __repr__(self):
        return '#<Microchip ' + self.material.element + '>'

    def is_compatible(self, other):
        return (self.type == other.type or self.material == other.material)


class Generator(object):

    def __init__(self, material):
        self.type = Type.Generator
        self.material = material

    def __deepcopy__(self, memo):
        return self

    def __str__(self):
        return self.material.short_name + 'G'

    def __repr__(self):
        return '#<Generator ' + self.material.element + '>'

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return (self.material.element == other.material.element)
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(self.material.element)

    def is_compatible(self, other):
        return (self.type == other.type or self.material == other.material)


class Floor(object):

    def __init__(self, i):
        self.number = i
        self.items = []

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return (self.number == other.number and
                    sorted(self.items) == sorted(other.items))
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(self.number, sorted(self.items())))

    def is_legal(self):
        "Determines if the items on the floor are legal together"
        #
        # Need to handle the case where a microchip is attached
        # to its generator
        #
        if len(self.items) < 2:
            # Zero or one items are fine
            return True
        microchips = [x for x in self.items if x.type == Type.Microchip]
        generators = [x for x in self.items if x.type == Type.Generator]
        if not microchips or not generators:
            # All one kind or the other is fine
            return True
        #
        # We've got some microchips and some generators.
        # Each microchip has to have a matching generator for this
        #   floor to be legal
        for m in microchips:
            if Generator(m.material) not in generators:
                return False
        # No mismatched microchips, so legal
        return True

    def extend(self, thing):
        self.items.extend(thing)

    def remove_items(self, items):
        for i in items:
            if i in self.items:
                self.items.remove(i)
            else:
                msg = 'Floor.remove_items item %r is not in %r'
                raise Exception(msg % (i, self.items))

    def add_items(self, items):
        self.items.extend(items)

    def is_empty(self):
        return len(self.items) == 0


class Move(object):

    def __init__(self, old_floor, new_floor, items):
        self.old_floor = old_floor
        self.new_floor = new_floor
        self.items = items


class WorldState(object):

    def __init__(self, numFloors):
        self.floors = [Floor(i) for i in range(numFloors)]
        self.elevator = 0
        self.generation = 0

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return (self.elevator == other.elevator and
                    self.floors == other.floors)
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(self.elevator, self.floors))

    def is_legal(self):
        "This world state is legal if all the floors in the state are legal"
        return not [f.is_legal() for f in self.floors].count(False)

    def next_floors(self):
        "Where can the elevator move next?"
        return [x for x in [self.elevator+1, self.elevator-1]
                    if x in range(len(self.floors))]

    def next_items(self):
        """What items can move next?

        One or two items fit on the elevator. If two they must be compatible
        either by type or by material.
        """
        items = list(self.floors[self.elevator].items)
        # Each thing can travel alone
        result = [[i] for i in items]
        # What combinations can travel together?
        while items:
            item = items.pop()
            for i in items:
                if item.is_compatible(i):
                    result.insert(0, [item, i])
        return result

    def next_moves(self):
        result = []
        floors = self.next_floors()
        items = self.next_items()
        for f in floors:
            for i in items:
                result.append(Move(self.elevator, f, i))
        return result

    def apply_move(self, move):
        self.floors[move.old_floor].remove_items(move.items)
        self.floors[move.new_floor].add_items(move.items)
        self.elevator = move.new_floor

    def is_complete(self):
        return (self.floors[0].is_empty() and
                self.floors[1].is_empty() and
                self.floors[2].is_empty())

    def __str__(self):
        out = ''
        for i in reversed(range(len(self.floors))):
            out += 'F%d ' % (i+1)
            if self.elevator == i:
                out += ' E '
            else:
                out += '   '
            for item in self.floors[i].items:
                out += str(item) + ' '
            out += '\n'
        return out


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

def real_world_state():
    ws = WorldState(4)
    # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    ws.floors[0].extend([Microchip(Element.Strontium),
                         Generator(Element.Strontium),
                         Microchip(Element.Plutonium),
                         Generator(Element.Plutonium)])
    # The second floor contains a hydrogen generator.
    ws.floors[1].extend([Generator(Element.Thulium),
                         Microchip(Element.Ruthenium),
                         Generator(Element.Ruthenium),
                         Microchip(Element.Curium),
                         Generator(Element.Curium)])
    # The third floor contains a lithium generator.
    ws.floors[2].extend([Microchip(Element.Thulium)])
    # The fourth floor contains nothing relevant.
    return ws

def test_a_bit(ws1):
    ws2 = copy.deepcopy(ws1)
    if ws1 != ws2:
        raise Exception('equality is not working')
    else:
        print 'deep copy looks good'
    ws2.elevator = ws2.elevator + 1
    if ws1 == ws2:
        raise Exception('equality is not working')
    else:
        print 'inequality looks good'
    print 'Next floors ', ws1.elevator, '=', ws1.next_floors()
    print 'Next floors ', ws2.elevator, '=', ws2.next_floors()
    print 'Next items 1', ws1.next_items()
    print 'Next items 2', ws2.next_items()
    print 'Next moves 1', ws1.next_moves()
    print 'Next moves 2', ws2.next_moves()

def main():
    all_states = []
    next_states = []
    # Construct the initial world state
    # world_state = test_world_state()
    world_state = real_world_state()
    # test_a_bit(world_state)
    all_states.append(world_state)
    next_states.append(world_state)
    while next_states:
        state = next_states.pop(0)
        print 'Working with gen %d state:' % (state.generation)
        print state
        for move in state.next_moves():
            # print 'Examining Move', move
            ws_prime = copy.deepcopy(state)
            ws_prime.apply_move(move)
            ws_prime.generation = state.generation + 1
            if ws_prime in all_states:
                print 'Already been here'
                continue
            if not ws_prime.is_legal():
                print 'Not legal'
                all_states.append(ws_prime)
                continue
            if ws_prime.is_complete():
                raise Exception('Puzzle complete, generation %d' % (ws_prime.generation))
            print 'Adding state'
            # print state
            all_states.append(ws_prime)
            next_states.append(ws_prime)
    print 'No more states to explore'

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
