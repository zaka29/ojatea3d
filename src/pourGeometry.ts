import { Vector3 } from 'three'

export function canPour(spout: Vector3, target: Vector3, angle: number, pourAngle: number, radius: number) {
  const height = spout.y - target.y
  return Math.abs(angle) >= Math.abs(pourAngle) * .76 &&
    Math.hypot(spout.x - target.x, spout.z - target.z) <= radius && height > 0 && height < .4
}
