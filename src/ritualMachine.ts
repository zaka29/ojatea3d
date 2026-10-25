export const ritualSteps = ['introduction', 'addLeaves', 'pourWater', 'steeping', 'pourTea', 'drink', 'complete'] as const

export type RitualStep = (typeof ritualSteps)[number]
export type RitualObject = 'none' | 'teaCaddy' | 'teaScoop' | 'kettle' | 'kyusu' | 'cup'

export type RitualStepDefinition = {
  index: number
  label: string
  title: string
  instruction: string
  requiredObject: RitualObject
  target?: RitualObject
  completion: string
  next: RitualStep | null
}

export const ritualDefinition: Record<RitualStep, RitualStepDefinition> = {
  introduction: { index: 0, label: 'ARRIVAL', title: 'A quiet cup', instruction: 'Enter the room and settle at the table.', requiredObject: 'none', completion: 'Room entered', next: 'addLeaves' },
  addLeaves: { index: 1, label: 'LEAVES', title: 'Measure the leaves', instruction: 'Place two scoops of sencha into the kyūsu.', requiredObject: 'teaScoop', target: 'kyusu', completion: 'Two scoops deposited', next: 'pourWater' },
  pourWater: { index: 2, label: 'WATER', title: 'Pour the water', instruction: 'Guide the kettle and fill the kyūsu.', requiredObject: 'kettle', target: 'kyusu', completion: 'Kyūsu volume reaches target', next: 'steeping' },
  steeping: { index: 3, label: 'STEEP', title: 'Let time pass', instruction: 'Watch the colour deepen as the tea rests.', requiredObject: 'none', completion: 'Steeping timer elapsed', next: 'pourTea' },
  pourTea: { index: 4, label: 'TEA', title: 'Pour the tea', instruction: 'Guide the kyūsu and fill the cup.', requiredObject: 'kyusu', target: 'cup', completion: 'Cup volume reaches target', next: 'drink' },
  drink: { index: 5, label: 'DRINK', title: 'Take the cup', instruction: 'Lift the cup and take a quiet sip.', requiredObject: 'cup', completion: 'Drink pose completed', next: 'complete' },
  complete: { index: 6, label: 'COMPLETE', title: 'A quiet moment', instruction: 'Rest with the finished cup.', requiredObject: 'none', completion: 'Completion moment viewed', next: null },
}

export function nextRitualStep(step: RitualStep): RitualStep {
  return ritualDefinition[step].next ?? step
}

export function canUseObject(step: RitualStep, object: RitualObject) {
  return ritualDefinition[step].requiredObject === object
}
