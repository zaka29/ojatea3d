import { expect, test, type Page, type TestInfo } from '@playwright/test'
import { kettleHome, kyusuHome, cupHome, scoopHome } from '../../src/sceneLayout'

type Scene = {
  objects: Record<string, { world: number[]; rotation: number[]; screen: [number, number] }>
  camera: { position: number[]; rotation: number[] }
  render: { calls: number; triangles: number }
  memory: { geometries: number; textures: number }
  frameMsMedian: number
  frameMsP95: number
}

async function scene(page: Page): Promise<Scene> {
  return JSON.parse((await page.locator('canvas').getAttribute('data-scene'))!)
}

const heading = (page: Page, name: string) => page.getByRole('heading', { name, exact: true })
const progress = async (page: Page) => Number(await page.getByRole('progressbar').getAttribute('aria-valuenow'))

async function enter(page: Page) {
  const started = Date.now()
  await page.goto('/')
  await expect(page.locator('canvas')).toHaveAttribute('data-scene-ready', 'true')
  await expect(page.locator('canvas')).toHaveAttribute('data-scene', /camera/)
  test.info().annotations.push({ type: 'scene-ready-ms', description: String(Date.now() - started) })
  await page.getByRole('button', { name: 'ENTER THE ROOM' }).click()
  await expect(heading(page, 'OPEN THE CADDY')).toBeVisible()
}

async function clickObject(page: Page, name: string) {
  const [x, y] = (await scene(page)).objects[name].screen
  await page.mouse.click(x, y)
}

async function leaves(page: Page, mouse = false) {
  if (mouse) await clickObject(page, 'caddy')
  else await page.keyboard.press('Enter')
  await expect(heading(page, 'MEASURE THE LEAVES')).toBeVisible()
  for (const next of ['ONE MORE SCOOP', 'POUR THE WATER']) {
    if (mouse) await clickObject(page, 'scoop')
    else await page.keyboard.press('Enter')
    await expect(heading(page, next)).toBeVisible({ timeout: 15_000 })
  }
}

async function approach(page: Page, name: string, mouse = false) {
  if (mouse) await clickObject(page, name)
  else await page.keyboard.press('Enter')
  await expect(heading(page, name === 'cup' ? 'TAKE A SIP' : 'READY TO POUR')).toBeVisible()
}

async function holdUntil(page: Page, name: string, next: string, mouse = false) {
  if (mouse) {
    const [x, y] = (await scene(page)).objects[name].screen
    await page.mouse.move(x, y)
    await page.mouse.down()
  } else await page.keyboard.down('Space')
  try { await expect(heading(page, next)).toBeVisible({ timeout: 15_000 }) }
  finally {
    if (mouse) await page.mouse.up()
    else await page.keyboard.up('Space')
  }
}

async function finish(page: Page, mouse = false) {
  await approach(page, 'kettle', mouse)
  await holdUntil(page, 'kettle', 'LET TIME PASS', mouse)
  await expect(heading(page, 'POUR THE TEA')).toBeVisible({ timeout: 30_000 })
  await approach(page, 'kyusu', mouse)
  await holdUntil(page, 'kyusu', 'LIFT THE CUP', mouse)
  await approach(page, 'cup', mouse)
  await holdUntil(page, 'cup', 'A QUIET CUP', mouse)
}

async function evidence(page: Page, info: TestInfo, name: string) {
  await page.screenshot({ path: info.outputPath(`${name}.png`) })
  await info.attach(name, { path: info.outputPath(`${name}.png`), contentType: 'image/png' })
  await info.attach(`${name}-metrics`, { body: JSON.stringify(await scene(page), null, 2), contentType: 'application/json' })
}

async function assertAtHome(page: Page) {
  const homes = { kettle: kettleHome, kyusu: kyusuHome, cup: cupHome, scoop: scoopHome }
  for (const [name, home] of Object.entries(homes)) {
    await expect.poll(async () => Math.hypot(...(await scene(page)).objects[name].world.map((value, i) => value - home[i]))).toBeLessThan(.02)
  }
}

for (const viewport of [
  { width: 1440, height: 900 }, { width: 1280, height: 720 }, { width: 1024, height: 768 },
  { width: 768, height: 1024 }, { width: 390, height: 844 },
]) {
  test(`presentation and selectable objects at ${viewport.width}×${viewport.height}`, async ({ page }, info) => {
    await page.setViewportSize(viewport)
    await enter(page)
    await page.getByRole('button', { name: 'Toggle ambience' }).focus()
    await page.keyboard.press('Enter')
    await expect(heading(page, 'OPEN THE CADDY')).toBeVisible()
    await page.locator('canvas').focus()
    // Let the camera finish its responsive framing before measuring object projections.
    await expect.poll(async () => {
      const { objects } = await scene(page)
      return ['caddy', 'scoop', 'kettle', 'kyusu', 'cup'].every(name => {
        const [x, y] = objects[name].screen
        return x > 30 && x < viewport.width - 30 && y > 90 && y < viewport.height - 90
      })
    }).toBe(true)
    const layout = await page.locator('.guidance').evaluate(el => {
      const guide = el.getBoundingClientRect()
      const controls = document.querySelector('.controls')!.getBoundingClientRect()
      return { inside: guide.left >= 0 && guide.right <= innerWidth, separate: guide.bottom <= controls.top || guide.right <= controls.left }
    })
    expect(layout).toEqual({ inside: true, separate: true })
    await evidence(page, info, `layout-${viewport.width}`)
  })
}

for (const scenario of [
  { name: 'desktop keyboard', mouse: false, viewport: { width: 1280, height: 720 }, reduced: false },
  { name: 'desktop mouse', mouse: true, viewport: { width: 1440, height: 900 }, reduced: false },
  { name: 'portrait keyboard with reduced motion', mouse: false, viewport: { width: 768, height: 1024 }, reduced: true },
]) {
  test(`full ceremony and physical reset: ${scenario.name}`, async ({ page }, info) => {
    const errors: string[] = []
    page.on('pageerror', error => errors.push(error.message))
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()) })
    await page.setViewportSize(scenario.viewport)
    await page.emulateMedia({ reducedMotion: scenario.reduced ? 'reduce' : 'no-preference' })
    await enter(page)
    await leaves(page, scenario.mouse)
    await finish(page, scenario.mouse)
    await assertAtHome(page)
    const first = await scene(page)
    await evidence(page, info, 'complete')
    await page.getByRole('button', { name: 'Begin the ceremony again' }).click()
    await expect(heading(page, 'OPEN THE CADDY')).toBeVisible()
    await expect.poll(() => progress(page)).toBe(0)
    await assertAtHome(page)
    if (scenario.name !== 'desktop keyboard') {
      expect(errors).toEqual([])
      await evidence(page, info, 'reset')
      return
    }
    await leaves(page, scenario.mouse)
    await finish(page, scenario.mouse)
    await assertAtHome(page)
    const second = await scene(page)
    // Fresh leaf meshes are expected; geometries/textures must not accumulate per ceremony.
    expect(second.memory.geometries).toBeLessThanOrEqual(first.memory.geometries + 2)
    expect(second.memory.textures).toBeLessThanOrEqual(first.memory.textures + 1)
    expect(errors).toEqual([])
    await evidence(page, info, 'repeat-complete')
  })
}

test('interruptions, mixed input, focus loss, and resize recover without skipping steps', async ({ page }, info) => {
  await enter(page)
  await clickObject(page, 'kettle')
  await page.keyboard.press('Space')
  await expect(heading(page, 'OPEN THE CADDY')).toBeVisible()
  await page.keyboard.press('Enter')
  await page.keyboard.press('Enter')
  await expect(heading(page, 'MEASURING LEAVES')).toBeVisible()
  await page.keyboard.press('Enter') // repeated input during motion must not deposit twice
  await expect.poll(async () => {
    const [x, y] = (await scene(page)).objects.scoop.world
    return x < -1.5 && y < .4 && y > .19
  }).toBe(true)
  await page.keyboard.press('Escape')
  await expect(heading(page, 'MEASURE THE LEAVES')).toBeVisible()
  for (const next of ['ONE MORE SCOOP', 'POUR THE WATER']) {
    await page.keyboard.press('Enter')
    await expect(heading(page, next)).toBeVisible({ timeout: 15_000 })
  }
  await page.keyboard.press('Enter')
  await page.keyboard.press('Escape') // cancel during approach
  await expect.poll(async () => Math.abs((await scene(page)).objects.kettle.world[1] - kettleHome[1])).toBeLessThan(.015)
  await approach(page, 'kettle')
  const before = (await scene(page)).camera
  const [x, y] = (await scene(page)).objects.kettle.screen
  await page.mouse.move(x, y)
  await page.mouse.down()
  await page.mouse.move(x + 30, y + 30, { steps: 5 })
  await expect.poll(() => progress(page)).toBeGreaterThan(5)
  await page.mouse.up()
  await expect(heading(page, 'READY TO POUR')).toBeVisible()
  const partial = await progress(page)
  expect(partial).toBeLessThan(100)
  expect((await scene(page)).camera).toEqual(before)
  await page.keyboard.down('Space')
  await expect(heading(page, 'POURING WATER')).toBeVisible()
  await page.evaluate(() => window.dispatchEvent(new Event('blur')))
  await page.keyboard.up('Space')
  await expect(heading(page, 'READY TO POUR')).toBeVisible()
  await holdUntil(page, 'kettle', 'LET TIME PASS')
  // Exercise the browser visibility event without editing application state.
  await page.evaluate(() => {
    Object.defineProperty(document, 'hidden', { configurable: true, value: true })
    document.dispatchEvent(new Event('visibilitychange'))
  })
  const resting = await progress(page)
  await page.waitForTimeout(500)
  expect(await progress(page)).toBe(resting)
  await page.evaluate(() => {
    delete (document as unknown as Record<string, unknown>).hidden
    document.dispatchEvent(new Event('visibilitychange'))
  })
  await expect(heading(page, 'POUR THE TEA')).toBeVisible({ timeout: 30_000 })
  await approach(page, 'kyusu')
  await page.setViewportSize({ width: 768, height: 1024 })
  await page.keyboard.press('Escape')
  await expect.poll(async () => (await scene(page)).objects.kyusu.world[1]).toBeLessThan(-.2)
  await approach(page, 'kyusu')
  await page.keyboard.down('Space')
  await expect.poll(() => progress(page)).toBeGreaterThan(5)
  await page.keyboard.up('Space')
  await expect(heading(page, 'READY TO POUR')).toBeVisible()
  await holdUntil(page, 'kyusu', 'LIFT THE CUP')
  await page.keyboard.press('Enter')
  await page.keyboard.press('Escape')
  await expect(heading(page, 'LIFT THE CUP')).toBeVisible()
  await approach(page, 'cup')
  await page.keyboard.down('Space')
  await expect.poll(() => progress(page)).toBeGreaterThan(5)
  await page.evaluate(() => window.dispatchEvent(new Event('blur')))
  await page.keyboard.up('Space')
  await expect(heading(page, 'TAKE A SIP')).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(heading(page, 'LIFT THE CUP')).toBeVisible()
  await approach(page, 'cup')
  await evidence(page, info, 'portrait-sip')
  await holdUntil(page, 'cup', 'A QUIET CUP')
  await assertAtHome(page)
})
