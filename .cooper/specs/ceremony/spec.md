# Ceremony

## Ordered preparation

GIVEN a visitor enters the room
WHEN the ceremony begins
THEN preparation starts with the leaves and proceeds through water, steeping, tea, drinking, and completion.

GIVEN the leaf preparation step is active
WHEN the caddy is open and two scoop deposits have completed and the scoop returns
THEN the caddy closes and water preparation becomes active.

GIVEN water or tea is being poured
WHEN normalized fill reaches the completion threshold and the vessel returns home
THEN the ceremony advances to steeping or drinking respectively.

## Steeping and completion

GIVEN steeping is active
WHEN twenty simulation seconds accumulate while the document is visible
THEN tea pouring becomes available.

GIVEN the visitor completes the sip
WHEN the cup returns home
THEN the ceremony reaches completion and waits for restart.

## Guards and reset

GIVEN a transfer action has the wrong ceremony step, stage, or invalid numeric amount
WHEN it is submitted
THEN preparation progress does not increase.

GIVEN the visitor restarts
WHEN the reset action runs
THEN preparation progress, held state, and interaction stages reset and the visitor remains in the room at leaf preparation.
