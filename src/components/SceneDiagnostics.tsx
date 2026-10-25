import { useFrame } from '@react-three/fiber'
import { useEffect, useRef } from 'react'
import { useThree } from '@react-three/fiber'
import { Vector3 } from 'three'

// Read-only development telemetry lets regression tests inspect the rendered scene,
// including real object trajectories, without skipping animations or mutating ritual state.
export function SceneDiagnostics() {
  const { gl } = useThree()
  useEffect(() => {
    const original = gl.info.autoReset
    gl.info.autoReset = false
    gl.info.reset()
    return () => { gl.info.autoReset = original; gl.info.reset() }
  }, [gl])
  const elapsed = useRef(0)
  const samples = useRef<number[]>([])
  useFrame(({ gl, scene, camera, size }, delta) => {
    // Shadows render several offscreen passes. Sum an entire animation-frame
    // interval instead of accidentally reporting only the last blur quad.
    const render = { ...gl.info.render }
    gl.info.reset()
    elapsed.current += delta
    samples.current.push(delta * 1000)
    if (samples.current.length > 120) samples.current.shift()
    if (elapsed.current < .2) return
    elapsed.current = 0
    const objects: Record<string, unknown> = {}
    for (const name of ['caddy', 'caddy-lid', 'scoop', 'kettle', 'kyusu', 'kyusu-lid', 'cup']) {
      const object = scene.getObjectByName(name)
      if (!object) continue
      const world = object.getWorldPosition(new Vector3())
      const screen = world.clone().project(camera)
      objects[name] = {
        world: world.toArray(), rotation: object.rotation.toArray().slice(0, 3),
        screen: [(screen.x + 1) * size.width / 2, (1 - screen.y) * size.height / 2],
      }
    }
    const frames = [...samples.current].sort((a, b) => a - b)
    gl.domElement.dataset.scene = JSON.stringify({
      objects, camera: { position: camera.position.toArray(), rotation: camera.rotation.toArray().slice(0, 3) },
      render, memory: gl.info.memory,
      renderer: (() => {
        const context = gl.getContext()
        const debug = context.getExtension('WEBGL_debug_renderer_info')
        return context.getParameter(debug ? debug.UNMASKED_RENDERER_WEBGL : context.RENDERER)
      })(),
      frameMsMedian: frames[Math.floor(frames.length / 2)],
      frameMsP95: frames[Math.floor(frames.length * .95)],
    })
  })
  return null
}
