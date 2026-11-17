# Guided interaction

## Input and choreography

GIVEN the required object is available
WHEN the visitor selects it with a pointer or Enter
THEN its guided action begins.

GIVEN a pouring vessel or cup is ready
WHEN the visitor holds the primary pointer action or Space
THEN pouring or sipping progresses while its action conditions hold.

GIVEN a held action is released
WHEN pouring settles or sipping pauses
THEN the visitor may resume the unfinished action.

GIVEN the visitor presses Escape during an active gesture
WHEN the object returns safely
THEN unfinished scoop deposits are not counted and an unfinished sip remains resumable.

## Recovery and focus

GIVEN an action is held
WHEN the window loses focus, the document becomes hidden, or a pointer is cancelled
THEN held transfer stops and the interaction can recover.

GIVEN a keyboard event repeats, uses shortcut modifiers, or targets a native interactive control
WHEN scene shortcuts process input
THEN the scene leaves that event to its normal behavior.

GIVEN object choreography is active
WHEN camera input occurs
THEN camera manipulation does not interfere with the object gesture.
