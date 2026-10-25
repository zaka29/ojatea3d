import { Html } from '@react-three/drei'
import { ThreeEvent, useFrame, useThree } from '@react-three/fiber'
import { ReactNode, RefObject, useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import type { InteractionStage } from '../store'
import { isSceneShortcut, useReducedMotion } from '../interaction'
import { canPour } from '../pourGeometry'

export type Point3 = [number, number, number]

type GuidedPourProps = {
  name: string
  children: ReactNode
  enabled: boolean
  held: boolean
  stage: InteractionStage
  completed: boolean
  home: Point3
  readyPose: Point3
  spoutAnchor: Point3
  targetAnchor: Point3
  pourRotation: number
  targetRadius?: number
  streamColor?: string
  onHeldChange: (held: boolean) => void
  onStageChange: (stage: InteractionStage) => void
  onPour: (delta: number) => void
  onHoverChange?: (hovered: boolean) => void
}

export function GuidedPour({ name, children, enabled, held, stage, completed, home, readyPose, spoutAnchor, targetAnchor, pourRotation, targetRadius = .3, streamColor = '#b7d9d4', onHeldChange, onStageChange, onPour, onHoverChange }: GuidedPourProps) {
  const vessel = useRef<THREE.Group>(null)
  const { gl } = useThree()
  const reducedMotion = useReducedMotion()
  const homePoint = useMemo(() => new THREE.Vector3(...home), [home])
  const readyPoint = useMemo(() => new THREE.Vector3(...readyPose), [readyPose])

  const select = () => {
    if (!enabled) return
    if (stage === 'idle' || stage === 'completed') onStageChange('approaching')
  }

  const beginPour = () => {
    if (!enabled || (stage !== 'readyToPour' && stage !== 'settling')) return
    onHeldChange(true)
    onStageChange('pouring')
  }

  const stopPour = () => {
    if (!enabled || !held) return
    onHeldChange(false)
    if (!completed) onStageChange('settling')
  }

  useEffect(() => {
    const keyDown = (event: KeyboardEvent) => {
      if (!isSceneShortcut(event) || !enabled) return
      if (event.code === 'Enter') { event.preventDefault(); select() }
      if (event.code === 'Space') { event.preventDefault(); beginPour() }
      if (event.code === 'Escape' && stage !== 'idle' && stage !== 'returning') {
        onHeldChange(false)
        onStageChange('returning')
      }
    }
    const keyUp = (event: KeyboardEvent) => { if (event.code === 'Space') stopPour() }
    const pointerUp = () => stopPour()
    window.addEventListener('keydown', keyDown)
    window.addEventListener('keyup', keyUp)
    window.addEventListener('pointerup', pointerUp)
    return () => {
      window.removeEventListener('keydown', keyDown)
      window.removeEventListener('keyup', keyUp)
      window.removeEventListener('pointerup', pointerUp)
    }
  })

  useFrame((_, delta) => {
    if (!vessel.current) return
    // Several vessels share the ritual's pour stage; only the active one may respond.
    if (!enabled) return
    const object = vessel.current
    const positionSpeed = reducedMotion ? 14 : 4.5
    const tiltSpeed = reducedMotion ? 14 : 3.4
    const positionSmoothing = 1 - Math.exp(-delta * positionSpeed)
    const tiltSmoothing = 1 - Math.exp(-delta * tiltSpeed)

    if (stage === 'approaching') {
      object.position.lerp(readyPoint, positionSmoothing)
      object.rotation.z = THREE.MathUtils.lerp(object.rotation.z, 0, positionSmoothing)
      if (object.position.distanceTo(readyPoint) < .012) onStageChange('readyToPour')
    } else if (stage === 'readyToPour') {
      object.rotation.z = THREE.MathUtils.lerp(object.rotation.z, 0, tiltSmoothing)
    } else if (stage === 'pouring') {
      object.rotation.z = THREE.MathUtils.lerp(object.rotation.z, pourRotation, tiltSmoothing)
      const spout = object.localToWorld(new THREE.Vector3(...spoutAnchor))
      const target = new THREE.Vector3(...targetAnchor)
      if (held && canPour(spout, target, object.rotation.z, pourRotation, targetRadius)) onPour(Math.min(delta, .05))
    } else if (stage === 'settling') {
      object.rotation.z = THREE.MathUtils.lerp(object.rotation.z, 0, tiltSmoothing)
      if (Math.abs(object.rotation.z) < .012) onStageChange('readyToPour')
    } else if (stage === 'returning') {
      object.rotation.z = THREE.MathUtils.lerp(object.rotation.z, 0, tiltSmoothing)
      object.position.lerp(homePoint, positionSmoothing)
      if (object.position.distanceTo(homePoint) < .015 && Math.abs(object.rotation.z) < .015) {
        object.position.copy(homePoint)
        object.rotation.set(0, 0, 0)
        onStageChange(completed ? 'completed' : 'idle')
      }
    } else if (stage === 'idle') {
      object.position.copy(homePoint)
      object.rotation.set(0, 0, 0)
    }
  })

  const pointerDown = (event: ThreeEvent<PointerEvent>) => {
    event.stopPropagation()
    if (!enabled || event.button !== 0) return
    if (stage === 'idle' || stage === 'completed') select()
    else beginPour()
    gl.domElement.setPointerCapture(event.pointerId)
  }

  return (
    <group
      name={name}
      ref={vessel}
      position={home}
      onPointerDown={pointerDown}
      onPointerEnter={(event) => { event.stopPropagation(); if (enabled) { onHoverChange?.(true); gl.domElement.style.cursor = stage === 'idle' ? 'pointer' : 'grab' } }}
      onPointerLeave={() => { onHoverChange?.(false); gl.domElement.style.cursor = 'default' }}
    >
      {children}
      {enabled && (stage === 'readyToPour' || stage === 'settling') && <Html center position={[0, .72, 0]} style={{ pointerEvents: 'none' }}><div className="object-label">PRESS &amp; HOLD TO POUR</div></Html>}
      <PourStream vessel={vessel} active={enabled && held && stage === 'pouring'} pourRotation={pourRotation} spoutAnchor={spoutAnchor} targetAnchor={targetAnchor} targetRadius={targetRadius} color={streamColor} />
    </group>
  )
}

function PourStream({ vessel, active, pourRotation, spoutAnchor, targetAnchor, targetRadius, color }: { vessel: RefObject<THREE.Group | null>, active: boolean, pourRotation: number, spoutAnchor: Point3, targetAnchor: Point3, targetRadius: number, color: string }) {
  const stream = useRef<THREE.Mesh>(null)
  useFrame(() => {
    if (!stream.current || !vessel.current) return
    const start = new THREE.Vector3(...spoutAnchor)
    const worldTarget = new THREE.Vector3(...targetAnchor)
    const worldSpout = vessel.current.localToWorld(start.clone())
    const valid = active && canPour(worldSpout, worldTarget, vessel.current.rotation.z, pourRotation, targetRadius)
    const target = vessel.current.worldToLocal(worldTarget)
    const direction = target.clone().sub(start)
    stream.current.visible = valid
    if (!valid) return
    stream.current.position.copy(start).add(target).multiplyScalar(.5)
    stream.current.scale.y = direction.length()
    stream.current.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.clone().normalize())
    ;(stream.current.material as THREE.MeshStandardMaterial).opacity = .48 + Math.sin(performance.now() * .02) * .06
  })
  return <mesh ref={stream} visible={false}><cylinderGeometry args={[.025, .04, 1, 10]} /><meshStandardMaterial color={color} transparent opacity={.6} emissive={color} emissiveIntensity={.24} /></mesh>
}
