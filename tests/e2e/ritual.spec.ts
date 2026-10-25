import { expect, test } from '@playwright/test'

test('welcomes the visitor and enters the tea room', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle('OjaTea — A Quiet Cup')
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Stillness,steeped.')
  await page.getByRole('button', { name: 'ENTER THE ROOM' }).click()
  await expect(page.getByRole('heading', { name: 'OPEN THE CADDY' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'ENTER THE ROOM' })).toBeHidden()
  await expect(page.locator('canvas')).toBeVisible()
})

test('opens the caddy and animates two scoops with the keyboard', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto('/')
  await expect(page.locator('canvas')).toHaveAttribute('data-scene-ready', 'true', { timeout: 30_000 })
  await page.getByRole('button', { name: 'ENTER THE ROOM' }).click()
  // Move focus off the entry button before exercising the scene's keyboard controls.
  await page.locator('canvas').click({ position: { x: 10, y: 10 } })
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: 'MEASURE THE LEAVES', exact: true })).toBeVisible()
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: 'ONE MORE SCOOP' })).toBeVisible({ timeout: 15_000 })
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: 'POUR THE WATER', exact: true })).toBeVisible({ timeout: 15_000 })
  expect(errors).toEqual([])
})
