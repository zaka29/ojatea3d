# Kyūsu — reference-inspired Blender study

Created 2 November 2026 through the connected Blender MCP server, using Blender 5.2.3 LTS. This is a standalone visual asset study; the running ceremony still uses its existing procedural pot.

## Files

- `kyusu-reference.blend`: editable model, packed textures, separate lid hierarchy, semantic anchors, and a preview studio. The previously open startup scene is preserved as `Scene`; use `OjaTea | Kyusu reference study` for this asset.
- `../../public/models/kyusu-reference.glb`: GLB with only the model, named parts, anchors, and embedded PBR textures. Preview lights, camera, floor, and original startup objects are excluded.
- `build_kyusu.py`: construction source, intended for execution inside Blender. It creates a new scene and refuses to overwrite an existing source asset. Work on a copy for another iteration. Boolean joins/vent cuts are committed meshes; the spout-join bevel and cord simplification remain editable modifiers.
- `textures/`: generated 1024 × 1024 clay base-colour and tangent-space normal maps, also packed into the Blender file and embedded in the GLB. The cord and burnished handle use simple material values.
- `previews/kyusu-closed.png` and `previews/kyusu-open.png`: inspected studio renders. Open-lid positioning is a presentation pose; the saved asset/export use the seated lid pose.
- `asset-metadata.json`: dimensions, anchors, triangle count, and mesh checks.
- `export-validation.json`: structural GLB checks and Blender round-trip import results.

## Shape and materials

The supplied photographs guide the squat rounded body, low circular foot, recessed lid, small knob and vent, short hollow spout, and perpendicular side handle with a flared terminal. The shaft has a modelled, twisted pale-cord wrap. A continuous inner wall and floor provide a real open cavity. The spout has a passage into the body; it is fused into the body mesh. Throwing rings on the lid remain individual meshes for editing.

The clay uses generated mineral flecks and fine normal detail. It is a visual interpretation of the iron-brown reference finish. No source photograph was sampled into a texture. This is an initial surface/shape study rather than a measured replica or a final production asset.

## Scale and hierarchy

Dimensions are inferred: approximately 136 mm body diameter, 80.5 mm to the body rim, and 94 mm to the knob top. Blender uses metres, +Z up, spout +X, handle -Y, and base at Z=0. GLB uses +Y up, spout +X, handle +Z, and base at Y=0.

`kyusu_root` is the asset root. `kyusu_lid` is a separate transform containing disc, knob, and throwing rings, with its pivot at the seated lid position. Body, side handle, and cord remain separate mesh objects. Move the whole lid through its parent, not the disc alone.

Exported semantic empty nodes:

| Node | Purpose |
| --- | --- |
| `anchor_base` | Surface contact at the model origin |
| `anchor_opening` | Receiving opening; approximate radius 36 mm |
| `anchor_spout_tip` | Stream origin at the spout mouth |
| `anchor_grip` | Handle grip reference |
| `anchor_lid_seat` | Seated lid transform reference |
| `anchor_liquid_surface` | Suggested surface centre at 50 mm height; liquid geometry is not included |
| `anchor_pour_pivot` | Candidate body-centred pivot at 40 mm height; not a calibrated ceremony pivot |

## Verification and remaining work

Both closed and detached-lid views were rendered and visually checked. All ten evaluated mesh objects had zero boundary/nonmanifold edges. The GLB has 72,896 triangles, two embedded textures, seven anchors, and a separate lid hierarchy. Header, mesh attributes, texture embedding, and studio exclusion checks passed. Importing the exported GLB into a separate Blender scene recovered ten meshes, seven anchors, and both full-resolution packed image buffers.

The GLB is approximately 5.31 MB. It retains close-view study detail; mesh/texture reduction and representative-device profiling are still needed before treating it as production-ready. No app build or ceremony tests were needed for this standalone asset creation, and no runtime integration claim is made.

Before integration, calibrate the asset to `sceneLayout.ts`, including physical-to-scene scale, root/pour pivot, receiving opening, liquid bounds, lid-rest pose, ready pose, tilt, handle clearance, and hit area. The perpendicular handle differs from the prototype's opposite-handle arrangement. Validate both pours and scoop travel with the new shape. An internal sieve/strainer and manufacturer-specific details are not reconstructed from these exterior photographs.

## Reference provenance

User-supplied photographs:

- `il_1588xN.8076310506_8lxw.webp`: underside/base and wrapped handle.
- `il_1588xN.8124230271_hmw0.webp`: open pot and detached lid.
- `il_1588xN.8124230291_9s4r.webp`: assembled pot, spout, lid, and handle.

Original listing/creator details were not supplied. The photographs stay outside the repository and runtime export. The model geometry and texture maps were constructed for this project.
