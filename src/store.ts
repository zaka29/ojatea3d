import { create } from 'zustand'
import { type RitualStep } from './ritualMachine'

export type InteractionStage = 'idle' | 'approaching' | 'readyToPour' | 'pouring' | 'settling' | 'returning' | 'completed'
export type ScoopStage = 'idle' | 'toCaddyAbove' | 'intoCaddy' | 'outOfCaddy' | 'toPot' | 'cancelLift' | 'cancelClear' | 'returning'
export type DrinkStage = 'idle' | 'approaching' | 'ready' | 'drinking' | 'returning' | 'completed'

export const STEEP_DURATION = 20

type ExperienceState = {
  entered: boolean
  activeStep: RitualStep
  hoveredObject: string | null
  held: boolean
  caddyOpen: boolean
  leafScoops: number
  scoopStage: ScoopStage
  waterFill: number
  cupFill: number
  steepElapsed: number
  drinkProgress: number
  drinkStage: DrinkStage
  interactionStage: InteractionStage
  setEntered: (entered: boolean) => void
  setHoveredObject: (object: string | null) => void
  openCaddy: () => void
  startScoop: () => void
  setScoopStage: (stage: ScoopStage) => void
  depositLeaves: () => void
  finishScoop: () => void
  cancelScoop: () => void
  setHeld: (held: boolean) => void
  setInteractionStage: (stage: InteractionStage) => void
  addWater: (amount: number) => void
  addTea: (amount: number) => void
  tickSteep: (seconds: number) => void
  setDrinkStage: (stage: DrinkStage) => void
  addDrink: (amount: number) => void
  recoverInteraction: () => void
  restartCeremony: () => void
}

const ceremonyDefaults = {
  hoveredObject: null,
  held: false,
  caddyOpen: false,
  leafScoops: 0,
  scoopStage: 'idle' as ScoopStage,
  waterFill: 0,
  cupFill: 0,
  steepElapsed: 0,
  drinkProgress: 0,
  drinkStage: 'idle' as DrinkStage,
  interactionStage: 'idle' as InteractionStage,
}

export const useExperience = create<ExperienceState>((set) => ({
  entered: false,
  activeStep: 'introduction',
  ...ceremonyDefaults,
  setEntered: (entered) => set({ entered, activeStep: entered ? 'addLeaves' : 'introduction', ...ceremonyDefaults }),
  setHoveredObject: (hoveredObject) => set({ hoveredObject }),
  openCaddy: () => set((state) => state.activeStep === 'addLeaves' ? { caddyOpen: true } : state),
  startScoop: () => set((state) => {
    if (state.activeStep !== 'addLeaves' || !state.caddyOpen || state.scoopStage !== 'idle' || state.leafScoops >= 2) return state
    return { scoopStage: 'toCaddyAbove', hoveredObject: null }
  }),
  setScoopStage: (scoopStage) => set({ scoopStage }),
  depositLeaves: () => set((state) => {
    if (state.activeStep !== 'addLeaves' || state.scoopStage !== 'toPot') return state
    return { leafScoops: Math.min(2, state.leafScoops + 1), scoopStage: 'returning' }
  }),
  finishScoop: () => set((state) => {
    if (state.scoopStage !== 'returning') return state
    return state.leafScoops >= 2
      ? { scoopStage: 'idle', caddyOpen: false, activeStep: 'pourWater', interactionStage: 'idle', hoveredObject: null }
      : { scoopStage: 'idle' }
  }),
  cancelScoop: () => set((state) => {
    if (state.activeStep !== 'addLeaves' || ['idle', 'returning', 'cancelLift', 'cancelClear'].includes(state.scoopStage)) return state
    return { scoopStage: 'cancelLift' }
  }),
  setHeld: (held) => set({ held }),
  setInteractionStage: (interactionStage) => set((state) => {
    if (state.activeStep !== 'pourWater' && state.activeStep !== 'pourTea') return state
    if (interactionStage === 'completed' && state.activeStep === 'pourWater' && state.waterFill >= .98) {
      return { interactionStage, activeStep: 'steeping', steepElapsed: 0, hoveredObject: null }
    }
    if (interactionStage === 'completed' && state.activeStep === 'pourTea' && state.cupFill >= .98) {
      return { interactionStage: 'idle', activeStep: 'drink', hoveredObject: null }
    }
    return { interactionStage }
  }),
  addWater: (amount) => set((state) => {
    if (state.activeStep !== 'pourWater' || state.interactionStage !== 'pouring' || !state.held || !Number.isFinite(amount) || amount <= 0) return state
    const nextFill = Math.min(1, state.waterFill + amount)
    const waterFill = nextFill >= .98 ? 1 : nextFill
    return {
      waterFill,
      held: waterFill >= .98 ? false : state.held,
      interactionStage: waterFill >= .98 ? 'returning' : 'pouring',
    }
  }),
  addTea: (amount) => set((state) => {
    if (state.activeStep !== 'pourTea' || state.interactionStage !== 'pouring' || !state.held || !Number.isFinite(amount) || amount <= 0) return state
    const nextFill = Math.min(1, state.cupFill + amount)
    const cupFill = nextFill >= .98 ? 1 : nextFill
    return {
      cupFill,
      held: cupFill >= .98 ? false : state.held,
      interactionStage: cupFill >= .98 ? 'returning' : 'pouring',
    }
  }),
  tickSteep: (seconds) => set((state) => {
    if (state.activeStep !== 'steeping' || !Number.isFinite(seconds) || seconds <= 0) return state
    const steepElapsed = Math.min(STEEP_DURATION, state.steepElapsed + seconds)
    return steepElapsed >= STEEP_DURATION
      ? { steepElapsed, activeStep: 'pourTea', interactionStage: 'idle' }
      : { steepElapsed }
  }),
  setDrinkStage: (drinkStage) => set((state) => {
    if (state.activeStep !== 'drink') return state
    if (drinkStage === 'completed' && state.activeStep === 'drink' && state.drinkProgress >= .98) {
      return { drinkStage, activeStep: 'complete', hoveredObject: null }
    }
    if (drinkStage === 'completed') return { drinkStage: 'idle' }
    return { drinkStage }
  }),
  addDrink: (amount) => set((state) => {
    if (state.activeStep !== 'drink' || state.drinkStage !== 'drinking' || !Number.isFinite(amount) || amount <= 0) return state
    const nextProgress = Math.min(1, state.drinkProgress + amount)
    const drinkProgress = nextProgress >= .98 ? 1 : nextProgress
    return { drinkProgress, drinkStage: drinkProgress >= .98 ? 'returning' : 'drinking' }
  }),
  recoverInteraction: () => set((state) => ({
    held: false,
    hoveredObject: null,
    interactionStage: state.interactionStage === 'pouring' ? 'settling' : state.interactionStage,
    drinkStage: state.drinkStage === 'drinking' ? 'ready' : state.drinkStage,
  })),
  restartCeremony: () => set({ entered: true, activeStep: 'addLeaves', ...ceremonyDefaults }),
}))
