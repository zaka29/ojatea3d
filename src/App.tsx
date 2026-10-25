import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { ContactShadows, Environment, Html, RoundedBox, Sparkles } from '@react-three/drei'
import { RotateCcw, Volume2, VolumeX } from 'lucide-react'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'
import { GuidedPour } from './components/GuidedPour'
import { ritualDefinition } from './ritualMachine'
import { STEEP_DURATION, useExperience } from './store'
import { isSceneShortcut, useReducedMotion } from './interaction'
import { SceneDiagnostics } from './components/SceneDiagnostics'
import { TRAY_CENTER_Y, TRAY_THICKNESS, TRAY_SURFACE_Y, SCOOP_HANDLE_Y, kettleHome, kettleReady, kyusuOpening, kyusuHome, kyusuReady, cupHome, cupOpening, caddyHome, scoopHome, kyusuLidRest, kyusuBodyProfile } from './sceneLayout'

const clay = '#b8a885'
const charcoal = '#22251f'
const copper = '#96755a'
const kettleSpout: [number, number, number] = [1, .18, 0]
const kyusuSpout: [number, number, number] = [.84, .12, 0]

function Room() {
  const reducedMotion = useReducedMotion()
  return (
    <>
      <color attach="background" args={['#20271f']} />
      <fog attach="fog" args={['#20271f', 7, 17]} />
      <ambientLight intensity={0.65} color="#c8d2b7" />
      <directionalLight position={[-3, 6, 4]} intensity={3.1} color="#ffe8bd" castShadow shadow-mapSize={[1024, 1024]} />
      <pointLight position={[3, 2.4, -2]} intensity={14} color="#d17d4f" distance={5} />

      <mesh position={[0, -1.26, -1]} receiveShadow>
        <boxGeometry args={[12, 0.18, 12]} />
        <meshStandardMaterial color="#292b24" roughness={0.94} />
      </mesh>
      <mesh position={[0, 2.6, -5.5]} receiveShadow>
        <boxGeometry args={[12, 8, 0.15]} />
        <meshStandardMaterial color="#44483c" roughness={1} />
      </mesh>

      <group position={[-3.45, 1.45, -5.25]}>
        <mesh>
          <boxGeometry args={[2.7, 3.7, 0.14]} />
          <meshStandardMaterial color="#d4c6a4" roughness={0.9} />
        </mesh>
        {[-0.9, 0, 0.9].map((x) => <mesh key={x} position={[x, 0, 0.09]}><boxGeometry args={[0.045, 3.7, 0.04]} /><meshBasicMaterial color="#736c57" /></mesh>)}
        <mesh position={[0, 0, 0.1]}><boxGeometry args={[2.7, 0.045, 0.04]} /><meshBasicMaterial color="#736c57" /></mesh>
      </group>

      <group position={[3.5, -0.1, -5.2]}>
        <mesh position={[0, 0.15, 0]}><cylinderGeometry args={[0.55, 0.75, 0.5, 16]} /><meshStandardMaterial color="#272b22" /></mesh>
        {[0, 1, 2, 3, 4].map((i) => <mesh key={i} position={[Math.sin(i * 2.2) * .25, .65 + i * .32, Math.cos(i * 2.2) * .15]} rotation={[0, 0, Math.sin(i) * .5]}><sphereGeometry args={[.27, 8, 8]} /><meshStandardMaterial color="#43513d" roughness={1} /></mesh>)}
      </group>

      <Table />
      {!reducedMotion && <Sparkles count={30} scale={[7, 3.5, 5]} size={0.7} speed={0.08} opacity={0.18} color="#f6ddae" />}
      <Environment files="/environment/lebombo_1k.hdr" environmentIntensity={0.16} />
    </>
  )
}

function Table() {
  return (
    <group>
      <RoundedBox args={[7, .22, 3.7]} radius={0.08} position={[0, -0.77, -1.45]} castShadow receiveShadow>
        <meshStandardMaterial color="#6d513a" roughness={.68} />
      </RoundedBox>
      <mesh position={[0, -0.61, -1.4]} receiveShadow>
        <boxGeometry args={[4.6, .045, 2.55]} />
        <meshStandardMaterial color="#80684b" roughness={.85} />
      </mesh>
      <mesh position={[0, TRAY_CENTER_Y, -1.4]} receiveShadow>
        <boxGeometry args={[4.35, TRAY_THICKNESS, 2.3]} />
        <meshStandardMaterial color="#9b8664" roughness={.8} />
      </mesh>
      <ContactShadows position={[0, TRAY_SURFACE_Y + .001, -1.5]} opacity={0.42} scale={7} blur={1.5} far={3} color="#191b16" />
      <Kyusu />
      <Cup />
      <Caddy />
      <TeaScoop />
      <Kettle />
      <SteepingSystem />
    </group>
  )
}

function Kyusu() {
  const fill = useExperience((s) => s.waterFill)
  const cupFill = useExperience((s) => s.cupFill)
  const activeStep = useExperience((s) => s.activeStep)
  const leafScoops = useExperience((s) => s.leafScoops)
  const steepElapsed = useExperience((s) => s.steepElapsed)
  const held = useExperience((s) => s.held)
  const stage = useExperience((s) => s.interactionStage)
  const setHeld = useExperience((s) => s.setHeld)
  const setStage = useExperience((s) => s.setInteractionStage)
  const addTea = useExperience((s) => s.addTea)
  const setHoveredObject = useExperience((s) => s.setHoveredObject)
  const [hovered, setHovered] = useState(false)
  const lid = useRef<THREE.Group>(null)
  const reducedMotion = useReducedMotion()
  const teaColour = useMemo(() => new THREE.Color('#849153').lerp(new THREE.Color('#8a7942'), steepElapsed / STEEP_DURATION), [steepElapsed])

  useFrame((_, delta) => {
    if (!lid.current) return
    const lidOff = activeStep === 'addLeaves' || activeStep === 'pourWater'
    // When removed, the lid rests on the tray rather than floating beside the pot.
    const target = lidOff ? new THREE.Vector3(...kyusuLidRest) : new THREE.Vector3(0, .43, 0)
    const easing = 1 - Math.exp(-delta * (reducedMotion ? 14 : 4))
    lid.current.position.lerp(target, easing)
    lid.current.rotation.z = THREE.MathUtils.lerp(lid.current.rotation.z, 0, easing)
  })

  return (
    <GuidedPour
      name="kyusu"
      enabled={activeStep === 'pourTea'}
      held={held}
      stage={stage}
      completed={cupFill >= .98}
      home={kyusuHome}
      readyPose={kyusuReady}
      spoutAnchor={kyusuSpout}
      targetAnchor={cupOpening}
      pourRotation={-.64}
      targetRadius={.28}
      streamColor="#9a874c"
      onHeldChange={setHeld}
      onStageChange={setStage}
      onPour={(delta) => addTea(delta * .72)}
      onHoverChange={(value) => { setHovered(value); setHoveredObject(value ? 'kyusu' : null) }}
    >
      <mesh castShadow><latheGeometry args={[kyusuBodyProfile, 32]} /><meshStandardMaterial color={clay} roughness={.72} /></mesh>
      <mesh position={[0, .39, 0]} castShadow><cylinderGeometry args={[.26, .32, .13, 24]} /><meshStandardMaterial color="#514f3b" /></mesh>
      <group name="kyusu-lid" ref={lid} position={[0, .43, 0]}>
        <mesh castShadow><cylinderGeometry args={[.24, .29, .16, 24]} /><meshStandardMaterial color="#aa9a79" /></mesh>
        <mesh position={[0, .12, 0]} castShadow><cylinderGeometry args={[.12, .16, .1, 20]} /><meshStandardMaterial color={clay} /></mesh>
      </group>
      <mesh position={[-.72, .08, 0]} rotation={[0, 0, Math.PI / 2]} castShadow><cylinderGeometry args={[.11, .18, .75, 18]} /><meshStandardMaterial color={clay} /></mesh>
      <mesh position={[.52, .12, 0]} rotation={[0, 0, -Math.PI / 2]} castShadow><coneGeometry args={[.19, .65, 18]} /><meshStandardMaterial color={clay} /></mesh>
      {Array.from({ length: leafScoops * 5 }).map((_, index) => <mesh key={index} position={[(index % 3 - 1) * .07, .43 + (index % 2) * .012, (Math.floor(index / 3) - .5) * .045]} rotation={[0, index * .8, (index % 2 ? .25 : -.2)]}><boxGeometry args={[.09, .012, .025]} /><meshStandardMaterial color="#46552c" roughness={1} /></mesh>)}
      <mesh position={[0, .25, 0]} scale={[1, Math.max(.02, fill * (1 - cupFill) * .12), 1]}><cylinderGeometry args={[.34, .34, .18, 24]} /><meshStandardMaterial color={teaColour} transparent opacity={.76} emissive={hovered ? '#282517' : '#000000'} /></mesh>
      <Steam active={activeStep === 'steeping' || activeStep === 'pourTea'} />
    </GuidedPour>
  )
}

function Cup() {
  const group = useRef<THREE.Group>(null)
  const { camera, gl } = useThree()
  const activeStep = useExperience((s) => s.activeStep)
  const cupFill = useExperience((s) => s.cupFill)
  const drinkProgress = useExperience((s) => s.drinkProgress)
  const stage = useExperience((s) => s.drinkStage)
  const setStage = useExperience((s) => s.setDrinkStage)
  const addDrink = useExperience((s) => s.addDrink)
  const setHoveredObject = useExperience((s) => s.setHoveredObject)
  const [hovered, setHovered] = useState(false)
  const reducedMotion = useReducedMotion()
  const home = useMemo(() => new THREE.Vector3(...cupHome), [])

  const select = () => {
    if (activeStep !== 'drink') return
    if (stage === 'idle') setStage('approaching')
    else if (stage === 'ready') setStage('drinking')
  }

  useEffect(() => {
    const down = (event: KeyboardEvent) => {
      if (activeStep !== 'drink' || !isSceneShortcut(event)) return
      if (event.code === 'Enter' && stage === 'idle') { event.preventDefault(); setStage('approaching') }
      if (event.code === 'Space' && stage === 'ready') { event.preventDefault(); setStage('drinking') }
      if (event.code === 'Escape' && !['idle', 'returning', 'completed'].includes(stage)) setStage('returning')
    }
    const stop = () => { if (useExperience.getState().drinkStage === 'drinking' && useExperience.getState().drinkProgress < .98) setStage('ready') }
    const keyUp = (event: KeyboardEvent) => { if (event.code === 'Space') stop() }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', keyUp)
    window.addEventListener('pointerup', stop)
    window.addEventListener('blur', stop)
    return () => {
      window.removeEventListener('keydown', down)
      window.removeEventListener('keyup', keyUp)
      window.removeEventListener('pointerup', stop)
      window.removeEventListener('blur', stop)
    }
  }, [activeStep, setStage, stage])

  useFrame((_, delta) => {
    if (!group.current) return
    const smoothing = 1 - Math.exp(-delta * (reducedMotion ? 14 : 4.5))
    const aspect = camera instanceof THREE.PerspectiveCamera ? camera.aspect : 1
    const drinkPose = camera.localToWorld(new THREE.Vector3(.12, -.18, aspect < .9 ? -2.8 : -1.85))
    if (stage === 'approaching') {
      group.current.position.lerp(drinkPose, smoothing)
      if (group.current.position.distanceTo(drinkPose) < .018) setStage('ready')
    } else if (stage === 'ready') {
      group.current.position.lerp(drinkPose, smoothing)
      group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, 0, smoothing)
    } else if (stage === 'drinking') {
      group.current.position.lerp(drinkPose, smoothing)
      // Positive X rotation brings the near rim toward the seated camera.
      group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, .48, 1 - Math.exp(-delta * 3.2))
      addDrink(Math.min(delta, .05) * .82)
    } else if (stage === 'returning') {
      group.current.position.lerp(home, smoothing)
      group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, 0, smoothing)
      if (group.current.position.distanceTo(home) < .018 && Math.abs(group.current.rotation.x) < .015) {
        group.current.position.copy(home)
        group.current.rotation.set(0, 0, 0)
        setStage('completed')
      }
    } else if (stage === 'idle') {
      group.current.position.copy(home)
      group.current.rotation.set(0, 0, 0)
    }
  })

  return (
    <group
      ref={group}
      position={cupHome}
      name="cup"
      onPointerDown={(event) => { event.stopPropagation(); if (event.button === 0) { select(); gl.domElement.setPointerCapture(event.pointerId) } }}
      onPointerEnter={(event) => { event.stopPropagation(); if (activeStep === 'drink') { setHovered(true); setHoveredObject('cup'); gl.domElement.style.cursor = 'pointer' } }}
      onPointerLeave={() => { setHovered(false); setHoveredObject(null); gl.domElement.style.cursor = 'default' }}
    >
      <mesh castShadow><cylinderGeometry args={[.32, .25, .52, 24, 1, true]} /><meshStandardMaterial color="#d1c7ad" roughness={.83} side={THREE.DoubleSide} emissive={hovered ? '#383329' : '#000000'} /></mesh>
      <mesh position={[0, -.25, 0]}><cylinderGeometry args={[.25, .25, .035, 24]} /><meshStandardMaterial color="#b6ab91" /></mesh>
      <mesh position={[0, -.04, 0]} scale={[1, Math.max(.01, cupFill * (1 - drinkProgress)), 1]}><cylinderGeometry args={[.235, .235, .34, 24]} /><meshStandardMaterial color="#8d7940" transparent opacity={.82} /></mesh>
    </group>
  )
}

function Caddy() {
  const lid = useRef<THREE.Mesh>(null)
  const [hovered, setHovered] = useState(false)
  const activeStep = useExperience((s) => s.activeStep)
  const caddyOpen = useExperience((s) => s.caddyOpen)
  const scoopStage = useExperience((s) => s.scoopStage)
  const openCaddy = useExperience((s) => s.openCaddy)
  const startScoop = useExperience((s) => s.startScoop)
  const setHoveredObject = useExperience((s) => s.setHoveredObject)
  const enabled = activeStep === 'addLeaves'
  const reducedMotion = useReducedMotion()

  useEffect(() => {
    const keyDown = (event: KeyboardEvent) => {
      if (event.code === 'Escape' && activeStep === 'addLeaves' && useExperience.getState().scoopStage !== 'idle') {
        useExperience.getState().cancelScoop()
      }
      if (event.code !== 'Enter' || !isSceneShortcut(event) || activeStep !== 'addLeaves') return
      event.preventDefault()
      if (!useExperience.getState().caddyOpen) openCaddy()
      else startScoop()
    }
    window.addEventListener('keydown', keyDown)
    return () => window.removeEventListener('keydown', keyDown)
  }, [activeStep, openCaddy, startScoop])

  useFrame((_, delta) => {
    if (!lid.current) return
    const easing = 1 - Math.exp(-delta * (reducedMotion ? 14 : 5))
    lid.current.position.y = THREE.MathUtils.lerp(lid.current.position.y, caddyOpen ? .68 : .35, easing)
    lid.current.position.x = THREE.MathUtils.lerp(lid.current.position.x, caddyOpen ? -.62 : 0, easing)
    lid.current.rotation.z = THREE.MathUtils.lerp(lid.current.rotation.z, caddyOpen ? -.35 : 0, easing)
  })

  return (
    <group
      position={caddyHome}
      name="caddy"
      onClick={(event) => { event.stopPropagation(); if (enabled && !caddyOpen) openCaddy() }}
      onPointerEnter={(event) => { event.stopPropagation(); if (enabled) { setHovered(true); setHoveredObject(caddyOpen ? 'teaScoop' : 'teaCaddy') } }}
      onPointerLeave={() => { setHovered(false); setHoveredObject(null) }}
    >
      <mesh castShadow><cylinderGeometry args={[.35, .39, .65, 24]} /><meshStandardMaterial color="#373d32" metalness={.1} roughness={.5} emissive={hovered && !caddyOpen ? '#25301e' : '#000000'} /></mesh>
      <mesh position={[0, .28, 0]}><cylinderGeometry args={[.29, .29, .035, 24]} /><meshStandardMaterial color="#526034" roughness={1} /></mesh>
      <mesh name="caddy-lid" ref={lid} position={[0, .35, 0]} castShadow><cylinderGeometry args={[.37, .37, .12, 24]} /><meshStandardMaterial color="#454d3e" /></mesh>
      <mesh position={[0, .05, .39]}><planeGeometry args={[.27, .36]} /><meshBasicMaterial color="#ded4b7" /></mesh>
      {enabled && !caddyOpen && hovered && <Html center position={[0, .95, 0]} distanceFactor={7}><div className="object-label">OPEN THE CADDY</div></Html>}
      {enabled && caddyOpen && scoopStage === 'idle' && hovered && <Html center position={[0, 1.05, 0]} distanceFactor={7}><div className="object-label">SELECT THE SCOOP</div></Html>}
    </group>
  )
}

function TeaScoop() {
  const group = useRef<THREE.Group>(null)
  const reducedMotion = useReducedMotion()
  const [hovered, setHovered] = useState(false)
  const activeStep = useExperience((s) => s.activeStep)
  const caddyOpen = useExperience((s) => s.caddyOpen)
  const leafScoops = useExperience((s) => s.leafScoops)
  const stage = useExperience((s) => s.scoopStage)
  const startScoop = useExperience((s) => s.startScoop)
  const setStage = useExperience((s) => s.setScoopStage)
  const depositLeaves = useExperience((s) => s.depositLeaves)
  const finishScoop = useExperience((s) => s.finishScoop)
  const setHoveredObject = useExperience((s) => s.setHoveredObject)
  const home = useMemo(() => new THREE.Vector3(...scoopHome), [])
  const aboveCaddy = useMemo(() => new THREE.Vector3(-1.55, .72, -1), [])
  const pickup = useMemo(() => new THREE.Vector3(caddyHome[0], caddyHome[1] + .42, caddyHome[2]), [])
  const exitCaddy = useMemo(() => new THREE.Vector3(-1.55, .82, -1), [])
  const clearCaddy = useMemo(() => new THREE.Vector3(-1.02, .82, -.72), [])
  const wideArc = useMemo(() => new THREE.Vector3(-.65, .92, -1.35), [])
  const deposit = useMemo(() => new THREE.Vector3(0, kyusuOpening[1] + .15, -1.65), [])
  const enabled = activeStep === 'addLeaves' && caddyOpen && stage === 'idle' && leafScoops < 2

  useFrame((_, delta) => {
    if (!group.current) return
    const speed = 1 - Math.exp(-delta * (reducedMotion ? 16 : 5.8))
    if (stage === 'toCaddyAbove') {
      group.current.position.lerp(aboveCaddy, speed)
      group.current.rotation.z = THREE.MathUtils.lerp(group.current.rotation.z, .8, speed)
      if (group.current.position.distanceTo(aboveCaddy) < .018) setStage('intoCaddy')
    } else if (stage === 'intoCaddy') {
      group.current.position.lerp(pickup, speed)
      group.current.rotation.z = THREE.MathUtils.lerp(group.current.rotation.z, .8, speed)
      if (group.current.position.distanceTo(pickup) < .018) setStage('outOfCaddy')
    } else if (stage === 'outOfCaddy') {
      group.current.position.lerp(exitCaddy, speed)
      if (group.current.position.distanceTo(exitCaddy) < .018) setStage('toPot')
    } else if (stage === 'cancelLift') {
      group.current.position.lerp(exitCaddy, speed)
      if (group.current.position.distanceTo(exitCaddy) < .018) setStage('cancelClear')
    } else if (stage === 'cancelClear') {
      group.current.position.lerp(clearCaddy, speed)
      if (group.current.position.distanceTo(clearCaddy) < .018) setStage('returning')
    } else if (stage === 'toPot') {
      const target = group.current.position.x < -.7 ? wideArc : deposit
      group.current.position.lerp(target, speed)
      group.current.rotation.z = THREE.MathUtils.lerp(group.current.rotation.z, .25, speed)
      if (target === deposit && group.current.position.distanceTo(deposit) < .018) depositLeaves()
    } else if (stage === 'returning') {
      group.current.position.lerp(home, speed)
      group.current.rotation.z = THREE.MathUtils.lerp(group.current.rotation.z, 0, speed)
      if (group.current.position.distanceTo(home) < .018) {
        group.current.position.copy(home)
        group.current.rotation.set(0, 0, 0)
        finishScoop()
      }
    }
  })

  return (
    <group
      ref={group}
      position={scoopHome}
      name="scoop"
      rotation={[0, 0, 0]}
      onClick={(event) => { event.stopPropagation(); if (enabled) startScoop() }}
      onPointerEnter={(event) => { event.stopPropagation(); if (enabled) { setHovered(true); setHoveredObject('teaScoop') } }}
      onPointerLeave={() => { setHovered(false); setHoveredObject(null) }}
    >
      <mesh position={[.34, SCOOP_HANDLE_Y, 0]} rotation={[0, 0, Math.PI / 2]} castShadow><cylinderGeometry args={[.025, .035, .72, 12]} /><meshStandardMaterial color="#c1aa78" roughness={.75} emissive={hovered ? '#453b25' : '#000000'} /></mesh>
      <mesh position={[-.04, 0, 0]} scale={[1.45, .35, .8]} castShadow><sphereGeometry args={[.13, 16, 10]} /><meshStandardMaterial color="#bca572" roughness={.8} /></mesh>
      {['outOfCaddy', 'toPot'].includes(stage) && Array.from({ length: 4 }).map((_, index) => <mesh key={index} position={[-.08 + index * .035, .055, 0]} rotation={[0, index, .2]}><boxGeometry args={[.06, .012, .02]} /><meshStandardMaterial color="#42522b" /></mesh>)}
      {enabled && hovered && <Html center position={[.2, .42, 0]} distanceFactor={7}><div className="object-label">ADD SCOOP {leafScoops + 1} OF 2</div></Html>}
    </group>
  )
}

function Steam({ active }: { active: boolean }) {
  const reducedMotion = useReducedMotion()
  const particles = useRef<THREE.Group>(null)
  useFrame(({ clock }) => {
    if (!particles.current) return
    particles.current.visible = active && !reducedMotion
    particles.current.children.forEach((particle, index) => {
      const t = (clock.elapsedTime * .18 + index * .2) % 1
      particle.position.set(Math.sin(t * 8 + index) * .06, .52 + t * .72, Math.cos(t * 6 + index) * .045)
      particle.scale.setScalar(.35 + t * .7)
    })
  })
  return <group ref={particles} visible={false}>{Array.from({ length: 5 }).map((_, index) => <mesh key={index}><sphereGeometry args={[.035, 8, 8]} /><meshBasicMaterial color="#e5e1d2" transparent opacity={.14} depthWrite={false} /></mesh>)}</group>
}

function SteepingSystem() {
  const accumulator = useRef(0)
  const tickSteep = useExperience((s) => s.tickSteep)
  useFrame((_, delta) => {
    if (useExperience.getState().activeStep !== 'steeping' || document.hidden) { accumulator.current = 0; return }
    accumulator.current += Math.min(delta, .1)
    if (accumulator.current >= .1) {
      tickSteep(accumulator.current)
      accumulator.current = 0
    }
  })
  return null
}

function RecoveryGuard() {
  const recoverInteraction = useExperience((s) => s.recoverInteraction)
  useEffect(() => {
    const recover = () => recoverInteraction()
    const visibility = () => { if (document.hidden) recoverInteraction() }
    window.addEventListener('blur', recover)
    window.addEventListener('pointercancel', recover)
    document.addEventListener('visibilitychange', visibility)
    return () => {
      window.removeEventListener('blur', recover)
      window.removeEventListener('pointercancel', recover)
      document.removeEventListener('visibilitychange', visibility)
    }
  }, [recoverInteraction])
  return null
}

function Kettle() {
  const [localHover, setLocalHover] = useState(false)
  const held = useExperience((s) => s.held)
  const activeStep = useExperience((s) => s.activeStep)
  const waterFill = useExperience((s) => s.waterFill)
  const stage = useExperience((s) => s.interactionStage)
  const setHoveredObject = useExperience((s) => s.setHoveredObject)
  const setHeld = useExperience((s) => s.setHeld)
  const setStage = useExperience((s) => s.setInteractionStage)
  const addWater = useExperience((s) => s.addWater)

  return (
    <GuidedPour
      name="kettle"
      enabled={activeStep === 'pourWater'}
      held={held}
      stage={stage}
      completed={waterFill >= .98}
      home={kettleHome}
      readyPose={kettleReady}
      spoutAnchor={kettleSpout}
      targetAnchor={kyusuOpening}
      pourRotation={-.72}
      onHeldChange={setHeld}
      onStageChange={setStage}
      // A single deliberate hold should complete the pour after the vessel settles into its tilt.
      onPour={(delta) => addWater(delta * .78)}
      onHoverChange={(hovered) => { setLocalHover(hovered); setHoveredObject(hovered ? 'kettle' : null) }}
    >
      <mesh castShadow><cylinderGeometry args={[.46, .53, .95, 24]} /><meshStandardMaterial color={copper} metalness={.48} roughness={.3} emissive={localHover ? '#403224' : '#000000'} emissiveIntensity={.5} /></mesh>
      <mesh position={[0, .53, 0]} castShadow><cylinderGeometry args={[.31, .39, .13, 24]} /><meshStandardMaterial color={charcoal} roughness={.36} /></mesh>
      <mesh position={[.58, .18, 0]} rotation={[0, 0, -Math.PI / 2]} castShadow><coneGeometry args={[.18, .78, 20]} /><meshStandardMaterial color={copper} metalness={.4} roughness={.33} /></mesh>
      <mesh position={[-.45, .35, 0]} rotation={[0, 0, .25]} castShadow><torusGeometry args={[.46, .065, 10, 24, Math.PI]} /><meshStandardMaterial color={charcoal} /></mesh>
    </GuidedPour>
  )
}

function CameraRig() {
  const { camera, gl, size } = useThree()
  const entered = useExperience((s) => s.entered)
  const reducedMotion = useReducedMotion()
  const pointer = useRef({ down: false, x: 0, y: 0, yaw: 0, pitch: 0 })

  useEffect(() => {
    camera.position.set(0, 1.45, 3.8)
    camera.lookAt(0, -.1, -1.3)
    const el = gl.domElement
    const interactionIsIdle = () => {
      const state = useExperience.getState()
      return !state.held && state.scoopStage === 'idle' && ['idle', 'completed'].includes(state.drinkStage) && (state.interactionStage === 'idle' || state.interactionStage === 'completed')
    }
    const down = (e: PointerEvent) => {
      if (e.button === 0 && !useExperience.getState().hoveredObject && interactionIsIdle()) pointer.current = { ...pointer.current, down: true, x: e.clientX, y: e.clientY }
    }
    const move = (e: PointerEvent) => {
      if (!pointer.current.down) return
      // R3F object handlers and this native canvas listener see the same press.
      // Consult the store synchronously so the first movement cannot leak into camera look.
      if (!interactionIsIdle()) { pointer.current.down = false; return }
      pointer.current.yaw = THREE.MathUtils.clamp(pointer.current.yaw - (e.clientX - pointer.current.x) * .0014, -.42, .42)
      pointer.current.pitch = THREE.MathUtils.clamp(pointer.current.pitch - (e.clientY - pointer.current.y) * .0011, -.18, .2)
      pointer.current.x = e.clientX; pointer.current.y = e.clientY
    }
    const up = () => { pointer.current.down = false }
    el.addEventListener('pointerdown', down); window.addEventListener('pointermove', move); window.addEventListener('pointerup', up); window.addEventListener('blur', up)
    return () => { el.removeEventListener('pointerdown', down); window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); window.removeEventListener('blur', up) }
  }, [camera, gl])

  useFrame((_, delta) => {
    const { held, interactionStage, scoopStage, drinkStage } = useExperience.getState()
    if (held || scoopStage !== 'idle' || !['idle', 'completed'].includes(drinkStage) || !['idle', 'completed'].includes(interactionStage)) return
    const portrait = size.width / size.height < .9
    const fov = portrait ? 48 : 43
    const distance = Math.max(3.8, 2.65 / (Math.tan(THREE.MathUtils.degToRad(fov / 2)) * size.width / size.height) - 1.3)
    const smoothing = reducedMotion ? 1 : 1 - Math.exp(-delta * 8)
    camera.position.lerp(new THREE.Vector3(0, portrait ? 1.25 : 1.45, distance), smoothing)
    if (camera instanceof THREE.PerspectiveCamera) {
      camera.fov = fov
      camera.updateProjectionMatrix()
    }
    const orientation = new THREE.Quaternion().setFromEuler(new THREE.Euler((entered ? -.13 : -.29) + pointer.current.pitch, pointer.current.yaw, 0, 'YXZ'))
    camera.quaternion.slerp(orientation, smoothing)
  })
  return null
}

function Scene() {
  const { gl } = useThree()
  useEffect(() => {
    // Scene effects mount after suspended environment assets have loaded.
    gl.domElement.dataset.sceneReady = 'true'
    return () => { delete gl.domElement.dataset.sceneReady }
  }, [gl])
  return <><Room /><CameraRig /><RecoveryGuard />{import.meta.env.DEV && <SceneDiagnostics />}</>
}

function Interface() {
  const entered = useExperience((s) => s.entered)
  const activeStep = useExperience((s) => s.activeStep)
  const hoveredObject = useExperience((s) => s.hoveredObject)
  const held = useExperience((s) => s.held)
  const waterFill = useExperience((s) => s.waterFill)
  const cupFill = useExperience((s) => s.cupFill)
  const caddyOpen = useExperience((s) => s.caddyOpen)
  const leafScoops = useExperience((s) => s.leafScoops)
  const scoopStage = useExperience((s) => s.scoopStage)
  const steepElapsed = useExperience((s) => s.steepElapsed)
  const drinkProgress = useExperience((s) => s.drinkProgress)
  const drinkStage = useExperience((s) => s.drinkStage)
  const stage = useExperience((s) => s.interactionStage)
  const setEntered = useExperience((s) => s.setEntered)
  const restart = useExperience((s) => s.restartCeremony)
  const [sound, setSound] = useState(true)
  const step = ritualDefinition[activeStep]
  const focusScene = () => document.querySelector('canvas')?.focus()
  const progress = activeStep === 'addLeaves' ? leafScoops / 2 : activeStep === 'pourWater' ? waterFill : activeStep === 'steeping' ? steepElapsed / STEEP_DURATION : activeStep === 'pourTea' ? cupFill : activeStep === 'drink' ? drinkProgress : activeStep === 'complete' ? 1 : 0

  const copy = useMemo(() => {
    if (activeStep === 'addLeaves') {
      if (!caddyOpen) return ['OPEN THE CADDY', 'Select the tea caddy to reveal the sencha.']
      if (scoopStage !== 'idle') return ['MEASURING LEAVES', 'The scoop follows a careful path to the kyūsu.']
      if (leafScoops === 1) return ['ONE MORE SCOOP', 'Select the tea scoop once more.']
      return ['MEASURE THE LEAVES', 'Select the scoop to add two measures of sencha.']
    }
    if (activeStep === 'pourWater') {
      if (waterFill >= .98) return ['POUR COMPLETE', 'The kettle is returning to its place.']
      if (stage === 'approaching') return ['GUIDING THE KETTLE', 'The vessel is moving into a comfortable pouring position.']
      if (held || stage === 'pouring') return ['POURING WATER', 'Keep holding until the kyūsu is full.']
      if (stage === 'readyToPour' || stage === 'settling') return ['READY TO POUR', 'Press and hold the kettle to control the flow.']
      if (hoveredObject === 'kettle') return ['KETTLE', 'Select to bring it to the kyūsu.']
      return ['POUR THE WATER', 'Select the kettle. It will move gently into position.']
    }
    if (activeStep === 'steeping') return ['LET TIME PASS', 'Watch the colour deepen. Nothing is required of you.']
    if (activeStep === 'pourTea') {
      if (cupFill >= .98) return ['CUP FILLED', 'The kyūsu is returning to the tray.']
      if (stage === 'approaching') return ['GUIDING THE KYŪSU', 'The teapot is moving into position above the cup.']
      if (held || stage === 'pouring') return ['POURING TEA', 'Keep holding until the cup is filled.']
      if (stage === 'readyToPour' || stage === 'settling') return ['READY TO POUR', 'Press and hold the kyūsu to control the flow.']
      return ['POUR THE TEA', 'Select the kyūsu to bring it toward the cup.']
    }
    if (activeStep === 'drink') {
      if (drinkStage === 'approaching') return ['LIFTING THE CUP', 'The cup is moving toward you.']
      if (drinkStage === 'ready') return ['TAKE A SIP', 'Press and hold the cup for a quiet sip.']
      if (drinkStage === 'drinking') return ['A QUIET SIP', 'Hold for just a moment.']
      if (drinkStage === 'returning') return ['SETTING IT DOWN', 'The cup is returning to the tray.']
      return ['LIFT THE CUP', 'Select the cup when you are ready.']
    }
    if (activeStep === 'complete') return ['A QUIET CUP', 'The ritual is complete. Stay for a moment, or begin again.']
    return [step.title.toUpperCase(), step.instruction]
  }, [activeStep, caddyOpen, cupFill, drinkStage, held, hoveredObject, leafScoops, scoopStage, stage, step.instruction, step.title, waterFill])

  const controls = activeStep === 'addLeaves'
    ? [['CLICK / ENTER', caddyOpen ? 'SCOOP' : 'OPEN'], ['TWO', 'MEASURES']]
    : activeStep === 'pourWater'
      ? [['CLICK / ENTER', 'APPROACH'], ['HOLD / SPACE', 'POUR'], ['ESC', 'RETURN']]
      : activeStep === 'steeping'
        ? [['WAIT', `${Math.max(0, Math.ceil(STEEP_DURATION - steepElapsed))} SEC`]]
        : activeStep === 'pourTea'
          ? [['CLICK / ENTER', 'APPROACH'], ['HOLD / SPACE', 'POUR'], ['ESC', 'RETURN']]
          : activeStep === 'drink'
            ? [['CLICK / ENTER', 'LIFT'], ['HOLD / SPACE', 'SIP'], ['ESC', 'RETURN']]
            : [['RITUAL', 'COMPLETE']]

  return (
    <div className="interface">
      <header className="brand"><div className="mon">お</div><div><span>OJA</span><small>TEA RITUAL</small></div></header>
      <button className="sound" onClick={() => setSound(!sound)} aria-label="Toggle ambience">{sound ? <Volume2 /> : <VolumeX />}</button>

      {!entered ? <section className="entry">
        <p className="eyebrow">A QUIET CUP · PROTOTYPE 01</p>
        <h1>Stillness,<br /><em>steeped.</em></h1>
        <p className="intro">A small ritual in warm water, green leaves and time. Take a seat. There is nowhere else to be.</p>
        <button className="enter" onClick={() => { setEntered(true); focusScene() }}><span>ENTER THE ROOM</span><i>→</i></button>
        <p className="hint">HEADPHONES RECOMMENDED · CLICK &amp; DRAG TO LOOK</p>
      </section> : <>
        <div className={`reticle ${hoveredObject ? 'active' : ''}`}><span /></div>
        {activeStep === 'complete' && <div className="completion-wash"><span>一服</span></div>}
        <section key={`${activeStep}-${copy[0]}`} className={`guidance ${activeStep === 'complete' ? 'done' : ''}`} aria-live="polite">
          <div className="step">{String(step.index + 1).padStart(2, '0')} <span /> {step.label}</div>
          <h2>{copy[0]}</h2>
          <p>{copy[1]}</p>
          <div className="fill" role="progressbar" aria-label={`${step.label.toLowerCase()} progress`} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(progress * 100)}><i style={{ width: `${progress * 100}%` }} /></div>
          {activeStep === 'steeping' && <div className="timer">{String(Math.max(0, Math.ceil(STEEP_DURATION - steepElapsed))).padStart(2, '0')}<small>SECONDS</small></div>}
          {activeStep === 'complete' && <button className="reset" onClick={() => { restart(); focusScene() }}><RotateCcw size={15} /> Begin the ceremony again</button>}
        </section>
        <div className="controls">{controls.map(([key, action]) => <span key={key}><b>{key}</b> {action}</span>)}</div>
      </>}
      <div className="phase-mark">PHASE 2<br />CEREMONY STUDY</div>
    </div>
  )
}

export default function App() {
  return <main><Canvas onCreated={({ gl }) => { gl.domElement.tabIndex = 0; gl.domElement.setAttribute('aria-label', 'Tea ceremony scene') }} shadows dpr={[1, 1.7]} camera={{ fov: 43, near: .1, far: 30 }} gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}><Scene /></Canvas><Interface /></main>
}
