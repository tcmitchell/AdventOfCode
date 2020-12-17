package aoc

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
