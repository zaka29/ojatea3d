import { describe, expect, it } from 'vitest'
import { Box3, CylinderGeometry, Group, LatheGeometry, Mesh, SphereGeometry } from 'three'
import { TRAY_SURFACE_Y, SCOOP_HANDLE_Y, caddyHome, cupHome, kettleHome, kyusuBodyProfile, kyusuHome, kyusuLidRest, scoopHome } from './sceneLayout'

describe('resting geometry and tray contact', () => {
  it('places every object base and the removed lid on the same surface', () => {
    const caddy = new Mesh(new CylinderGeometry(.35, .39, .65, 24))
    caddy.position.set(...caddyHome)
    const kettle = new Mesh(new CylinderGeometry(.46, .53, .95, 24))
    kettle.position.set(...kettleHome)
    const kyusu = new Mesh(new LatheGeometry(kyusuBodyProfile, 32))
    kyusu.position.set(...kyusuHome)
    const lid = new Mesh(new CylinderGeometry(.24, .29, .16, 24))
    lid.position.set(kyusuHome[0] + kyusuLidRest[0], kyusuHome[1] + kyusuLidRest[1], kyusuHome[2] + kyusuLidRest[2])
    const cup = new Group()
    const cupBase = new Mesh(new CylinderGeometry(.25, .25, .035, 24))
    cupBase.position.y = -.25
    cup.add(cupBase)
    cup.position.set(...cupHome)
    const scoop = new Mesh(new SphereGeometry(.13, 16, 10))
    scoop.scale.set(1.45, .35, .8)
    scoop.position.set(...scoopHome)
    const handle = new Mesh(new CylinderGeometry(.025, .035, .72, 12))
    handle.rotation.z = Math.PI / 2
    handle.position.set(scoopHome[0] + .34, scoopHome[1] + SCOOP_HANDLE_Y, scoopHome[2])
    for (const object of [caddy, kettle, kyusu, lid, cup, scoop, handle]) {
      expect(new Box3().setFromObject(object).min.y).toBeCloseTo(TRAY_SURFACE_Y, 6)
      object.traverse(child => { if (child instanceof Mesh) child.geometry.dispose() })
    }
  })
})
