package aoc

type Point2D struct {
	X, Y int
}

type Point3D struct {
	X, Y, Z int
}

func (p Point3D) Neighbors() []Point3D {
	result := make([]Point3D, 0)
	for x := p.X - 1; x <= p.X+1; x++ {
		for y := p.Y - 1; y <= p.Y+1; y++ {
			for z := p.Z - 1; z <= p.Z+1; z++ {
				if x == p.X && y == p.Y && z == p.Z {
					continue
				}
				result = append(result, Point3D{x, y, z})
			}
		}
	}
	return result
}

type Point4D struct {
	X, Y, Z, W int
}

func (p Point4D) Neighbors() []Point4D {
	result := make([]Point4D, 0)
	for x := p.X - 1; x <= p.X+1; x++ {
		for y := p.Y - 1; y <= p.Y+1; y++ {
			for z := p.Z - 1; z <= p.Z+1; z++ {
				for w := p.W - 1; w <= p.W+1; w++ {
					if x == p.X && y == p.Y && z == p.Z && w == p.W {
						continue
					}
					result = append(result, Point4D{x, y, z, w})
				}
			}
		}
	}
	return result
}
