# Technology stack

## Browser application

- TypeScript with strict checking and ES2022 output.
- React and React DOM for UI and component lifecycle.
- Vite and npm for development and static production builds.
- Three.js, React Three Fiber, and Drei for WebGL rendering and scene helpers.
- Zustand for ritual state; render-loop interpolation for guided motion.
- Plain CSS and Lucide React for interface styling and icons.

Dependency declarations live in [package.json](../../package.json); resolved versions live in [package-lock.json](../../package-lock.json). Runtime state is in memory. There is no backend or database.

## Asset authoring

Blender Python supports separately authored tea-ware and room studies on asset feature branches. These studies are not integrated into the browser baseline. Blender construction scripts require their intended Blender environment; they are not website runtime scripts.

## Tests and build

| Command | Purpose |
| --- | --- |
| `npm ci` | Install locked dependencies |
| `npm test` | Run Vitest unit tests |
| `npm run build` | Run TypeScript checks and Vite production build |
| `npm run test:e2e` | Run Playwright Chromium tests |
| `npm run dev` | Start Vite locally |

Playwright starts Vite on port 4173 and uses one worker to avoid competing WebGL contexts. Browser installation is a prerequisite for browser tests.

## Quality target and current gaps

New executable work follows Red/Green/Refactor and targets coverage greater than 80%. Coverage instrumentation and enforcement are not configured; test success is not a coverage measurement.

There is no configured linter, formatter, CI workflow, or production deployment in the baseline. Type checking is part of the build. Python testing and lint tools are not configured. Add tooling through a planned track rather than claiming it already exists.
