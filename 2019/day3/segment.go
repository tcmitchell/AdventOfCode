package main

import "fmt"

// VERTICAL direction
const VERTICAL string = "V"

// HORIZONTAL direction
const HORIZONTAL string = "H"

// Segment is a line segment
type Segment struct {
	x1, y1, x2, y2 int
	direction      string
}

// NewSegment creates a line segment
func NewSegment(x1, y1, x2, y2 int) (*Segment, error) {
	var dir string
	if x1 == x2 {
		dir = VERTICAL
		if y2 < y1 {
			y1, y2 = y2, y1
		}
	} else if y1 == y2 {
		dir = HORIZONTAL
		if x2 < x1 {
			x1, x2 = x2, x1
		}
	} else {
		return nil, fmt.Errorf("Segment is not H or V")
	}
	return &Segment{x1, y1, x2, y2, dir}, nil
}

func (seg *Segment) String() string {
	return fmt.Sprintf("Seg(%s:%d,%d - %d,%d)",
		seg.direction, seg.x1, seg.y1, seg.x2, seg.y2)
}

func (seg *Segment) intersects(other *Segment) (bool, int, int) {
	if seg.direction == other.direction {
		return false, 0, 0
	}
	switch seg.direction {
	case HORIZONTAL:
		if seg.x1 < other.x1 && other.x1 < seg.x2 &&
			other.y1 < seg.y1 && seg.y1 < other.y2 {
			return true, other.x1, seg.y1
		}
	case VERTICAL:
		if seg.y1 < other.y1 && other.y1 < seg.y2 &&
			other.x1 < seg.x1 && seg.x1 < other.x2 {
			return true, seg.x1, other.y1
		}
	}
	return false, 0, 0
}
