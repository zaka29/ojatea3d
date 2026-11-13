# Room furnishings — shared composition study

Completed 13 November 2026. This scene stages the independently authored table, tray, tea box, kettle,
kyūsu, and cup at their common physical metre scale. It is a furnishing and
composition preview for the future room, not a runtime scene or finished room.

## Deliverables

- `assemble_setting.py`: creates a new Blender scene using asset collection instances.
- `room-setting-study.blend`: the shared scene, saved with its dependencies.
- `previews/room-setting-wide.png`: table structure and the complete tea setting.
- `previews/room-setting-tabletop.png`: the working surface and tea ware.
- `setting-metadata.json`: surface heights and instance positions.

The assembled scene keeps the table/tray and tea objects independently
replaceable. Collection instances retain the source transforms, material
assignments, and relative scale. Linked asset files remain in their sibling
folders under `assets/`; keep those files together when moving the study.

Run the construction source in an isolated background Blender process. It
rejects live-UI execution and clears only its isolated seed scene before linking
the source files. The original model files are never overwritten.

The table surface and tray service anchors determine vertical placement.
Tea ware is staged on the service surface using the assets' base-at-zero
convention. Positions are a visual layout study; guided pour paths, scoop
travel, lid-rest positions, input hit areas, and camera behaviour still require
application calibration.

Both previews were rendered in CPU Cycles and visually inspected. Static checks
passed for all four tea objects: bases are within 2 mm of the service surface,
outer footprints remain within the tray, and each stays in the main service
zone clear of the drainage channel. Surface height is 0.756 m above the floor.
The two lid-rest centres in the metadata are reserved layout suggestions, not
validated animation endpoints.

The tray, its drainage features, and the separate catch pan establish visual
design intent. There is no fluid simulation or functional drainage system in
this composition. Table legs and unphotographed construction details are
inferred. Final room architecture, wall treatments, and production lighting
are outside this study.

## Sources and rendering

The original asset notes retain reference filenames, inferred dimensions,
materials, geometry checks, and export/import results:

- [Tea box](../teabox/README.md)
- [Table and tray](../table-tray/README.md)
- [Kettle](../kettle/README.md)
- [Kyūsu](../kyusu/README.md)
- [Cup](../cup/README.md)

Preview lighting uses the project's existing locally bundled HDR, with
[provenance recorded here](../../public/environment/README.md). Studio lights,
camera, and floor are separate from the asset collections. No studio or
combined room GLB is added to the runtime application.
