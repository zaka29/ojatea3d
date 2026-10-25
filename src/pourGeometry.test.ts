import { describe, expect, it } from 'vitest'
import { Matrix4, Vector3 } from 'three'
import { canPour } from './pourGeometry'
import { kettleReady, kyusuReady, kyusuOpening, cupOpening } from './sceneLayout'

describe('anchored pour geometry', () => {
  it.each([
    { spout: [1, .18, 0], pose: kettleReady, angle: -.72, target: kyusuOpening, radius: .3 },
    { spout: [.84, .12, 0], pose: kyusuReady, angle: -.64, target: cupOpening, radius: .28 },
  ])('aligns the configured vessel at its final pour angle', ({ spout, pose, angle, target, radius }) => {
    const world = new Vector3(...spout).applyMatrix4(new Matrix4().makeRotationZ(angle)).add(new Vector3(...pose))
    expect(canPour(world, new Vector3(...target), angle, angle, radius)).toBe(true)
  })
  it('rejects upright, missed, below-target, and excessive-height streams', () => {
    const target = new Vector3(0, 0, 0)
    expect(canPour(new Vector3(0, .2, 0), target, 0, -.72, .3)).toBe(false)
    for (const spout of [new Vector3(.5, .2, 0), new Vector3(0, -.1, 0), new Vector3(0, 1, 0), new Vector3(0, .2, .5)]) {
      expect(canPour(spout, target, -.72, -.72, .3)).toBe(false)
    }
  })
})
