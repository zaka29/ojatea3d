# Table and tray — room furnishing study

Created from the two user-supplied table/tray photographs using Blender 5.2.3 LTS in an isolated background process. The live Blender session and the existing tea-ware source files were not changed. These are standalone furnishing assets for the future room setting; the application still uses its procedural table and tray.

## Reference direction

The table is warm, darkened weathered plank timber with irregular grain, knots, seasoning checks, and one small worn edge notch. The photographs show the tabletop but do not establish the leg design. Four sturdy timber legs, aprons, and low stretchers are deliberately restrained inferred structure.

The tray is a dark walnut-coloured rectangular slab with rounded corners, a narrow pale timber inlay offset toward one side, and a long recessed drainage channel alongside it. A separate low-profile charcoal catch pan pulls out underneath, following the open-pan photograph. There is no raised perimeter rim. Two small drain holes connect the channel to the pan cavity; functional flow is not simulated.

The photographs guide the form and finish. Dimensions, wood species/finish interpretation, support construction, and drain details are inferred. The source images are not bundled or sampled into the generated textures.

## Scale and placement contract

| Asset | Inferred dimensions | Contact/surface anchors |
| --- | --- | --- |
| Table | 1.60 m long × 0.8486 m deep × 0.72 m tall | Base Z=0; tabletop Z=0.72 m |
| Tray | 0.84 m long × 0.44 m deep × 0.036 m tall | Base Z=0; service surface Z=0.036 m |
| Catch pan | Approximately 0.73 × 0.356 m | Closed in the neutral exported pose; 0.20 m preview extension |

All coordinates are metres. Blender uses +Z up; GLB uses +Y up. Both exported asset roots have their base at zero. To assemble in Blender, place the table at the floor and the tray root at Z=0.72 m. Tea objects then rest at world Z=0.756 m, plus any calibrated local base correction. The equivalent Y-up GLB placements use the same values on Y.

Exact source collections for linking/instancing:

- `TABLE | Export asset`, rooted at `table_root`.
- `TRAY | Export asset`, rooted at `tray_root`.

Anchors:

| Node | Blender local position | Purpose |
| --- | --- | --- |
| `table_anchor_base` | `(0, 0, 0)` | Floor contact |
| `table_anchor_surface` | `(0, 0, 0.72)` | Level tabletop |
| `tray_anchor_base` | `(0, 0, 0)` | Contact with the table |
| `tray_anchor_surface` | `(0, 0, 0.036)` | Level tea-service surface |
| `tray_anchor_pan_closed` | `(0, 0, 0)` | Closed pan offset |
| `tray_anchor_pan_open` | `(0, 0.20, 0)` | Open pan preview offset |
| `tray_anchor_channel` | `(0, -0.102, 0.0305)` | Channel floor centre |

The large clear service zone is X `[-0.39, 0.39]`, Y `[-0.075, 0.195]`. A separate narrow foreground strip is X `[-0.39, 0.39]`, Y `[-0.19, -0.13]`. The inlay is at Y=-0.122 m; the 10 mm channel is centred at Y=-0.102 m. Keep vessel feet and scoop travel clear of the channel. The rounded outer edge is outside the conservative service bounds.

`tray_catch_pan` is the independent moving parent for pan shell and front flange. It translates along local **+Y** in Blender, equivalent to **-Z** in the Y-up GLB. Side guides run parallel to this travel, and supports are outside the pan's horizontal travel envelope. The open-pan render is a temporary pose; the saved source and GLB retain the pan closed. Runtime drawer interaction is not implemented here.

## Files

- `table-tray-reference.blend`: editable geometry, retained bevel modifiers, packed texture maps, independent table/tray collections, studios, and combined furnishing preview.
- `../../public/models/table-reference.glb`: table geometry, materials, and anchors only.
- `../../public/models/tray-reference.glb`: tray, separate catch-pan hierarchy, materials, and anchors only.
- `build_table_tray.py`: reproducible Blender construction source. Normally refuses to overwrite outputs. An explicit `ALLOW_REBUILD=True` in the execution namespace is reserved for deliberate study revisions. It resets only its isolated process, never the live UI.
- `textures/`: generated 1536 × 768 base-colour and tangent-space normal maps for aged table wood and walnut tray wood. Maps are packed in the source and embedded in the relevant GLB.
- `previews/table-hero.png`: complete table and inferred leg structure.
- `previews/tray-closed.png`: surface, inlay, and channel.
- `previews/tray-pan-open.png`: independently extended catch pan.
- `previews/table-and-tray.png`: tray positioned on the table at the shared physical scale.
- `asset-metadata.json`: dimensions, anchors in both axis conventions, service bounds, pan travel, mesh checks, and export sizes.
- `export-validation.json`: structural GLB and Blender round-trip checks.

The previews use CPU Cycles at 32 samples with denoising. The locally bundled `lebombo_1k.hdr` provides restrained environment reflections; its existing [provenance notes](../../public/environment/README.md) apply. The HDR and studio objects are excluded from both furnishing GLBs.

## Verification and integration limits

The table contains 15 evaluated mesh objects and 3,156 triangles. The tray contains 10 evaluated mesh objects and 5,640 triangles. Every evaluated mesh has zero boundary and non-manifold edges. Export checks cover the asset-only hierarchies, normal attributes, UVs for textured materials, embedded maps, semantic anchors, and triangle totals. Blender round-trip imports verify object/anchor/image counts and physical bounds. Four previews were rendered and visually inspected, including the open drawer framing and the flush inlay.

The furnishing geometry is ready for composition studies. Application placement, camera framing, object home/ready poses, pouring/scoop clearance, interaction bounds, mobile framing, and representative-device performance still require integration validation. No app behaviour was changed and ceremony tests were not rerun.

## Source photographs

- `table and tray.webp`: rounded walnut board, offset inlay/channel, dark pull-out pan, aged timber tabletop.
- `table and tray 2.webp`: warm finish, board thickness, working tea-service arrangement, and tabletop wear.

The reference photographs remain outside the repository. The study does not recreate the visible people, the pictured tea ware, or the original listing's watermark.
