# Tea box — charcoal caddy reference study

Completed 13 November 2026 in Blender 5.2.3 LTS, using the Blender MCP background/CLI execution tool because the live addon server was unavailable. This standalone study follows the supplied tea-box photographs; the app's procedural caddy is unchanged.

## Design and scale

The study interprets a tall cylindrical caddy with a fine charcoal granular finish, a brown exposed rim/inner wall, a hollow floor and cavity, and a separate circular removable lid. The lid has a rounded arched loop grip, a fitted underside insert, and a narrow pale sealing ring inferred from the photographs. No exact clay, coating, or sealing material was supplied, so those material identities are visual interpretations.

Dimensions are inferred and proportioned to the earlier tea ware:

| Measurement | Model |
| --- | --- |
| Maximum body diameter | 90.3 mm |
| Body/rim height | Approximately 100.4 mm |
| Closed overall height including loop | 125.6 mm |
| Opening diameter | Approximately 82 mm |

The base is rebased to zero after subdivision. Open-lid preview placement is a temporary presentation pose, not a calibrated runtime motion.

## Files

- `teabox-reference.blend`: editable caddy, named parts, packed maps, semantic anchors, and studio. Scene: `OjaTea | Charcoal tea box study`. Export collection: `TEABOX | Export asset`.
- `../../public/models/teabox-reference.glb`: only the caddy root, five meshes, separate lid hierarchy, materials, anchors, and embedded textures. Studio objects are excluded.
- `build_teabox.py`: self-contained Blender Python construction source. It creates a new scene, guards against overwriting existing outputs, exports the asset, renders previews, measures mesh bounds, and writes only its own scene/dependencies to the source file. It does not execute in the website.
- `textures/teabox_charcoal_basecolor.png` and `textures/teabox_charcoal_normal.png`: generated 1024 × 1024 maps; packed in the source and embedded in the GLB. The photographs are not sampled into these textures.
- `previews/teabox-closed.png`: assembled silhouette, loop grip, and finish.
- `previews/teabox-open.png`: separate lid, pale underside seal, opening, and inner wall.
- `asset-metadata.json`: measured dimensions, anchors, triangle/resource counts, and edge checks.
- `export-validation.json`: GLB structure and Blender round-trip import results.

Existing scenes and asset files were preserved. The tea-box source is compact and self-contained; it has no linked dependency on the other tea-ware sources.

## Hierarchy and anchors

`teabox_root` is the asset root. `teabox_body` is its hollow shell. `teabox_lid` is an independently movable transform containing `teabox_lid_disc`, `teabox_lid_insert`, `teabox_lid_seal`, and `teabox_lid_loop`. Move the lid group as a whole to retain the fit between those pieces.

Blender coordinates use metres, +Z up, and base Z=0. GLB uses +Y up and base Y=0.

| Node | Intended role |
| --- | --- |
| `teabox_anchor_base` | Resting contact at the origin |
| `teabox_anchor_opening` | Receiving opening centre and approximate radius |
| `teabox_anchor_lid_seat` | Seated lid transform reference |
| `teabox_anchor_grip` | Lid loop grip/presentation point |
| `teabox_anchor_scoop_entry` | Clearance waypoint above the opening |

The asset contains no tea leaves, input handlers, animation, or ceremony state. The application should supply those behaviours and use the anchors for calibration.

## Verification and remaining work

All five evaluated meshes have zero boundary and non-manifold edges. The exported GLB has 36,884 triangles, five semantic anchors, and two embedded maps, at approximately 3.86 MB. Structural checks passed for the header, named nodes, mesh count, texture embedding, and studio exclusion. Blender round-trip import recovered all meshes, all anchors, both full-resolution packed image buffers, the measured height, and a base at zero. Closed and open preview renders were visually inspected after the charcoal refinement.

Before application integration, calibrate scale, home height, hit area, lid-rest placement, lid opening/closing poses, scoop entry/deposit paths, and safe cancellation clearance. Rendering optimisation and representative-device profiling remain part of production acceptance. App tests were not rerun because no runtime code changed.

## Reference provenance

User-supplied images:

- `teabox 1.webp`: hollow body, exposed rim/interior, detached lid, and pale underside seal.
- `teabox 2.webp`: closed silhouette and upright loop grip.
- `teabox 3.webp`: open body, lid face, loop shape, and granular surface detail.

These photographs remain outside the repository and runtime asset. Geometry and maps were constructed for this project.
