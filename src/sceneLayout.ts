import { Vector2 } from 'three'

export const TRAY_CENTER_Y = -.57
export const TRAY_THICKNESS = .018
export const TRAY_SURFACE_Y = TRAY_CENTER_Y + TRAY_THICKNESS / 2
export const restOnTray = (localBottom: number) => TRAY_SURFACE_Y - localBottom
type Point3 = [number, number, number]

// Rest pivots are derived from each model's actual lowest point. Phase 3 models
// should supply their base/foot bounds here rather than retuning scene heights.
export const kettleHome: Point3 = [-1.05, restOnTray(-.475), -2.35]
export const kyusuHome: Point3 = [0, restOnTray(-.34), -1.65]
export const cupHome: Point3 = [1.45, restOnTray(-.2675), -.85]
export const caddyHome: Point3 = [-1.55, restOnTray(-.325), -1]
export const scoopHome: Point3 = [-1.02, restOnTray(-.13 * .35), -.72]
export const SCOOP_HANDLE_Y = -.13 * .35 + .035
export const kyusuOpening: Point3 = [0, kyusuHome[1] + .45, -1.65]
export const cupOpening: Point3 = [1.45, cupHome[1] + .28, -.85]
export const kettleReady: Point3 = [-.72, kyusuOpening[1] + .59, -1.65]
export const kyusuReady: Point3 = [.67, cupOpening[1] + .63, -.85]
export const kyusuLidRest: Point3 = [.8, TRAY_SURFACE_Y - kyusuHome[1] + .08, .16]

// A flat foot avoids hiding the bottom of a complete sphere inside the tray.
export const kyusuBodyProfile = [
  [0, -.34], [.22, -.34], [.3, -.31], [.44, -.16],
  [.5, .02], [.45, .22], [.32, .39], [.26, .39],
].map(([radius, height]) => new Vector2(radius, height))
