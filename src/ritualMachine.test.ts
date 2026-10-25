import { describe, expect, it } from 'vitest'
import { canUseObject, nextRitualStep, ritualSteps } from './ritualMachine'

describe('ritual machine contract', () => {
  it('advances through the ceremony in order', () => {
    expect(ritualSteps.map(nextRitualStep)).toEqual([
      'addLeaves', 'pourWater', 'steeping', 'pourTea', 'drink', 'complete', 'complete',
    ])
  })

  it('only enables the required object for a step', () => {
    expect(canUseObject('pourWater', 'kettle')).toBe(true)
    expect(canUseObject('pourWater', 'kyusu')).toBe(false)
    expect(canUseObject('pourTea', 'kyusu')).toBe(true)
  })
})
