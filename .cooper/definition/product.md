# OjaTea 3D

## Vision

Offer a calm, seated, first-person sencha ceremony in a browser. Visitors prepare and drink a cup through deliberate, guided actions in an atmospheric tea room.

## Audience and journey

The primary audience is visitors seeking a short interactive tea experience. Desktop mouse and keyboard are the supported primary inputs. Narrow and portrait layouts provide responsive presentation; full touch interaction remains future work.

The visitor enters the room, opens the caddy, transfers two scoops of leaves, pours water into the kyūsu, waits for steeping, pours tea into the cup, takes a sip, and may restart.

## Implemented capabilities

- Ordered ceremony progression with guarded preparation actions and normalized fill progress.
- Guided approach and return, hold-to-pour and hold-to-sip, cancellation, and interruption recovery.
- Responsive instructions, ceremony progress, restart, and reduced-motion preferences.
- Procedural tea ware, shared resting-surface geometry, and spatial pour validation.

## Quality and boundaries

Preserve readable instructions, keyboard operation, safe interruption recovery, and consistent object placement. Treat representative-device performance and wider browser acceptance as pending validation.

The application is a static browser experience with in-memory state. Reloading resets the ceremony. Audio playback, production model integration, full touch controls, backend services, accounts, persistence, and hosting configuration are outside the implemented baseline.
