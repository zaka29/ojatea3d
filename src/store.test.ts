import { beforeEach, describe, expect, it } from 'vitest'
import { STEEP_DURATION, useExperience } from './store'

describe('connected ceremony store', () => {
  beforeEach(() => {
    useExperience.getState().restartCeremony()
  })

  it('requires the caddy and two completed scoop transfers', () => {
    useExperience.getState().startScoop()
    expect(useExperience.getState().scoopStage).toBe('idle')

    useExperience.getState().openCaddy()
    for (let index = 0; index < 2; index += 1) {
      useExperience.getState().startScoop()
      expect(useExperience.getState().scoopStage).toBe('toCaddyAbove')
      useExperience.getState().setScoopStage('toPot')
      useExperience.getState().depositLeaves()
      useExperience.getState().finishScoop()
    }
    expect(useExperience.getState()).toMatchObject({ leafScoops: 2, caddyOpen: false, activeStep: 'pourWater' })
  })

  it('ignores water transfer before the vessel is pouring', () => {
    useExperience.setState({ activeStep: 'pourWater', interactionStage: 'idle' })
    useExperience.getState().addWater(.5)
    expect(useExperience.getState().waterFill).toBe(0)
  })

  it('caps water fill and enters steeping after the kettle returns', () => {
    useExperience.setState({ activeStep: 'pourWater', interactionStage: 'pouring', held: true })
    useExperience.getState().addWater(2)
    expect(useExperience.getState()).toMatchObject({ waterFill: 1, held: false, interactionStage: 'returning' })
    useExperience.getState().setInteractionStage('completed')
    expect(useExperience.getState().activeStep).toBe('steeping')
  })

  it('advances to pour tea after the condensed steep', () => {
    useExperience.setState({ activeStep: 'steeping', steepElapsed: 0 })
    useExperience.getState().tickSteep(STEEP_DURATION)
    expect(useExperience.getState()).toMatchObject({ steepElapsed: STEEP_DURATION, activeStep: 'pourTea' })
  })

  it('fills the cup, drinks, and completes the ritual', () => {
    useExperience.setState({ activeStep: 'pourTea', interactionStage: 'pouring', cupFill: 0, held: true })
    useExperience.getState().addTea(2)
    expect(useExperience.getState()).toMatchObject({ cupFill: 1, interactionStage: 'returning', held: false })
    useExperience.getState().setInteractionStage('completed')
    expect(useExperience.getState().activeStep).toBe('drink')

    useExperience.getState().setDrinkStage('drinking')
    useExperience.getState().addDrink(2)
    expect(useExperience.getState()).toMatchObject({ drinkProgress: 1, drinkStage: 'returning' })
    useExperience.getState().setDrinkStage('completed')
    expect(useExperience.getState().activeStep).toBe('complete')
  })

  it('recovers safely when focus is lost mid-interaction', () => {
    useExperience.setState({ activeStep: 'pourWater', interactionStage: 'pouring', held: true })
    useExperience.getState().recoverInteraction()
    expect(useExperience.getState()).toMatchObject({ held: false, interactionStage: 'settling' })

    useExperience.setState({ activeStep: 'drink', drinkStage: 'drinking' })
    useExperience.getState().recoverInteraction()
    expect(useExperience.getState().drinkStage).toBe('ready')
  })

  it('restarts all ceremony progress', () => {
    useExperience.setState({ activeStep: 'steeping', caddyOpen: true, leafScoops: 2, waterFill: 1, steepElapsed: 8 })
    useExperience.getState().restartCeremony()
    expect(useExperience.getState()).toMatchObject({ activeStep: 'addLeaves', caddyOpen: false, leafScoops: 0, waterFill: 0, cupFill: 0, steepElapsed: 0, drinkProgress: 0 })
  })

  it('allows a cup cancelled before or during a sip to be lifted again', () => {
    useExperience.setState({ activeStep: 'drink', drinkStage: 'returning', drinkProgress: .3 })
    useExperience.getState().setDrinkStage('completed')
    expect(useExperience.getState()).toMatchObject({ activeStep: 'drink', drinkStage: 'idle', drinkProgress: .3 })
    useExperience.getState().setDrinkStage('approaching')
    expect(useExperience.getState().drinkStage).toBe('approaching')
  })

  it('lifts a cancelled scoop clear of the caddy without counting a deposit', () => {
    useExperience.getState().openCaddy()
    useExperience.getState().startScoop()
    useExperience.getState().setScoopStage('intoCaddy')
    useExperience.getState().cancelScoop()
    expect(useExperience.getState()).toMatchObject({ scoopStage: 'cancelLift', leafScoops: 0 })
    useExperience.getState().setScoopStage('returning')
    useExperience.getState().finishScoop()
    expect(useExperience.getState()).toMatchObject({ activeStep: 'addLeaves', leafScoops: 0, scoopStage: 'idle' })
  })

  it('rejects wrong-step, duplicate, and unheld transfers', () => {
    useExperience.getState().addTea(.5)
    useExperience.getState().addDrink(.5)
    useExperience.getState().depositLeaves()
    expect(useExperience.getState()).toMatchObject({ cupFill: 0, drinkProgress: 0, leafScoops: 0 })
    useExperience.setState({ activeStep: 'pourWater', interactionStage: 'pouring', held: false })
    useExperience.getState().addWater(.5)
    expect(useExperience.getState().waterFill).toBe(0)
    useExperience.setState({ scoopStage: 'toPot', activeStep: 'addLeaves' })
    useExperience.getState().depositLeaves()
    useExperience.getState().depositLeaves()
    expect(useExperience.getState().leafScoops).toBe(1)
  })

  it.each([-1, NaN, Infinity])('rejects invalid transfer amounts: %s', (amount) => {
    useExperience.setState({ activeStep: 'pourWater', interactionStage: 'pouring', held: true })
    useExperience.getState().addWater(amount)
    expect(useExperience.getState().waterFill).toBe(0)
    useExperience.setState({ activeStep: 'pourTea' })
    useExperience.getState().addTea(amount)
    expect(useExperience.getState().cupFill).toBe(0)
    useExperience.setState({ activeStep: 'drink', drinkStage: 'drinking' })
    useExperience.getState().addDrink(amount)
    expect(useExperience.getState().drinkProgress).toBe(0)
    useExperience.setState({ activeStep: 'steeping' })
    useExperience.getState().tickSteep(amount)
    expect(useExperience.getState().steepElapsed).toBe(0)
  })

  it('starts the tea gesture idle and ignores completion callbacks outside their step', () => {
    useExperience.setState({ activeStep: 'steeping', interactionStage: 'completed' })
    useExperience.getState().setDrinkStage('drinking')
    expect(useExperience.getState().drinkStage).toBe('idle')
    useExperience.getState().tickSteep(STEEP_DURATION)
    expect(useExperience.getState()).toMatchObject({ activeStep: 'pourTea', interactionStage: 'idle' })
  })
})
