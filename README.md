# OjaTea 3D

## Development

```sh
npm ci
npm run dev
```

## Testing

Unit tests use Vitest; browser tests use Playwright and start Vite automatically on port 4173.

```sh
npm test
npx playwright install chromium
npm run test:e2e
npm run test:e2e:ui
npm run test:e2e:debug
npm run test:e2e:report
```

The Chromium suite covers the complete ceremony with mouse and keyboard input, repeat/restart, interruption recovery, reduced motion, and five viewport sizes (1440×900 through a 390×844 presentation fallback). Tests wait for the real scene to load and operate real input and animation; no hooks skip ritual states. Development-only, read-only scene telemetry verifies object positions and records renderer counts and frame timings.

The existing environment HDR is bundled in `public/environment`, so scene loading no longer depends on an external asset host. Google Fonts remains optional; the CSS includes system fallbacks. The tests start and stop their own Vite server on port 4173. One worker avoids competing WebGL contexts and keeps baseline measurements comparable.

Run the focused Phase 2C suite with `npm run test:e2e -- phase2c`. The full keyboard repeat test takes roughly two minutes because it performs every gesture and both real 20-second steeps. Screenshots, scene metrics, and startup timing annotations are saved in the HTML/JSON reports. Frame timings from automated Chromium are a regression baseline, not a production FPS certification.

Failed tests save screenshots in `test-results/`; the first retry records a trace. Locally, use `npm run test:e2e -- --retries=1` to capture a retry trace. Reports and results are ignored by Git.

For CI:

```sh
npm ci
npx playwright install --with-deps chromium
npm test
npm run test:e2e
```

Upload `playwright-report/` and `test-results/` as artifacts, including when tests fail.

## Browser exploration with Playwright MCP

To connect an MCP-compatible client, configure a server with command `npx` and arguments `["@playwright/mcp@latest", "--isolated"]`. Start `npm run dev -- --host 127.0.0.1 --port 4173 --strictPort`, then ask the agent to explore `http://127.0.0.1:4173`. MCP browser exploration is separate from the committed regression suite; turn reproducible findings into tests in `tests/e2e/`.
