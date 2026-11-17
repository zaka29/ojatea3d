# Scene geometry

## Resting surfaces

GIVEN an object's local bottom is known
WHEN its home height is calculated
THEN that bottom rests on the shared tray surface.

GIVEN a removable lid is placed beside its vessel
WHEN it reaches its resting pose
THEN its base aligns with the intended resting surface.

## Validated pouring

GIVEN a source spout and receiving opening
WHEN transfer is evaluated
THEN flow requires sufficient tilt, horizontal alignment within the receiving radius, and a spout above the opening within the permitted height.

GIVEN a visible pour stream
WHEN its validity is determined
THEN the stream uses the same spatial predicate as liquid transfer.

## Model boundaries

The baseline uses procedural geometry and normalized liquid progress. Replacement assets require calibration of scale, local base, spout, opening, home and ready poses, lid placement, and liquid bounds before runtime acceptance.
