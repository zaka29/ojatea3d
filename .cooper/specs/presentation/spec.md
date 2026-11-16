# Presentation

## Ceremony guidance

GIVEN the ceremony is visible
WHEN its active step or progress changes
THEN the interface presents the current instruction and relevant progress or timer.

GIVEN the visitor enters or restarts
WHEN the transition completes
THEN the scene receives keyboard focus.

## Responsive layout and motion

GIVEN the viewport changes between desktop and narrow portrait dimensions
WHEN the interface and camera adapt
THEN guidance and controls remain available and scene framing responds to the viewport.

GIVEN reduced motion is requested
WHEN the scene animates
THEN guided movement is shortened and decorative dust and steam are suppressed without skipping ceremony steps.

## Scene resources

GIVEN the scene loads
WHEN its environment is requested
THEN the required HDR is served from the bundled local environment resource.

GIVEN optional web fonts are unavailable
WHEN interface text renders
THEN system font fallbacks remain available.

## Baseline limits

Responsive presentation does not establish complete touch control support. The sound button changes interface state; audio playback is not part of the implemented capability.
