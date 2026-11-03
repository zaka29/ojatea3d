# Kettle — stainless steel and wood reference study

Created 3 November 2026 through Blender MCP using Blender 5.2.3 LTS, following the kyūsu and cup asset workflow. This is a standalone model study; the running ceremony still uses its procedural kettle.

## Design and scale

User-supplied dimensions are approximately 22 cm overall width, 16 cm body diameter, and 17.7 cm height with the handle upright. Supplied materials are 18-8 stainless steel for the body and wood for the handle.

The model follows the photographed cylindrical body, softened lower edge, sloping shoulder, charcoal exterior, bare stainless interior, short curved spout, removable lid, and overhead bail handle. Two wood grip halves sandwich the steel strap, with two visible rivets. The lid has a tapered wooden knob and a small pressure vent. The dark exterior is interpreted as a finish over the stainless body; the exact coating was not specified.

| Measurement | Model |
| --- | --- |
| Overall width, including hinges/spout | 225.7 mm |
| Body depth/diameter | 159.9 mm |
| Overall height, handle upright | 177.5 mm |
| Receiving opening, approximate diameter | 97 mm |

Dimensions are close references rather than a measured manufacturer replica. The comparison uses the same metre scale as the saved kyūsu and cup, with no scale adjustment applied to any of the three models. Capacity has not been calibrated or certified.

## Files and scenes

- `kettle-reference.blend`: editable source, packed wood maps, formed body, lid, hinged handle group, semantic anchors, and preview studios. Existing live scenes were preserved and their source files were not overwritten. Select `OjaTea | Steel kettle study` for the kettle or `OjaTea | Kettle kyusu cup proportions` for the comparison.
- `../../public/models/kettle-reference.glb`: only the kettle asset hierarchy, materials, and embedded wood maps. No studio, HDR, camera, lights, cup, or kyūsu is exported.
- `build_kettle.py`: construction source for Blender Python/MCP. Creates new scenes and refuses to overwrite existing kettle output. Formed profiles and boolean cuts are committed geometry; bevel modifiers remain editable. Preview cameras are configured by the script; render them through Blender. The script is not used by the website.
- `textures/`: generated 1024 × 512 wood base-colour and normal maps, also packed in the source and embedded in the GLB. Metal finishes use standard material values.
- `previews/kettle-hero.png`: assembled form, lid, upright handle, and spout.
- `previews/kettle-open.png`: detached lid, folded-back handle, and stainless interior.
- `previews/kettle-grip-detail.png`: wood grain, grip halves, rivets, and handle joints.
- `previews/kettle-with-teaware.png`: the three asset studies at their shared physical scale.
- `asset-metadata.json`: measured dimensions, geometry checks, anchors, and export size.
- `export-validation.json`: GLB structure checks and Blender round-trip import results.

The comparison scene links the saved export collections from `../kyusu/kyusu-reference.blend` and `../cup/cup-reference.blend`. Keep those files available at their relative paths for the comparison. The kettle geometry and GLB are independent of the preview links.

The studio uses the project's existing `../../public/environment/lebombo_1k.hdr` for readable stainless reflections, packed into this source file. See its existing [provenance notes](../../public/environment/README.md). It is excluded from the kettle GLB.

## Structure and materials

The body is a thin-walled closed shell with a real floor and open cavity. The hollow spout is fused into the body mesh and has a passage through the wall. Exterior and interior surfaces have different materials; the spout mouth has an exposed steel lip. The inner floor includes a shallow formed ring.

`kettle_root` is the asset root. `kettle_lid` contains the lid disc and wooden knob. `kettle_handle` contains the steel strap, both grip halves, and both grip rivets. Body-mounted hinge brackets/pins remain outside that moving group.

The handle pivot is on the line joining the hinge pins, at Blender Z=104 mm. Rotate it around local **X** to fold the handle; the same X axis is retained by the Y-up GLB. The saved/exported neutral pose has its lid seated and handle upright. The open render uses a temporary handle rotation and detached lid pose; these are not baked animations or calibrated ceremony movements.

Blender coordinates are metres, +Z up, spout +X, base Z=0. GLB coordinates are +Y up, spout +X, base Y=0. Exported semantic nodes:

| Node | Intended role |
| --- | --- |
| `kettle_anchor_base` | Surface contact at zero |
| `kettle_anchor_opening` | Receiving opening and approximate radius |
| `kettle_anchor_spout_tip` | Candidate runtime stream origin |
| `kettle_anchor_grip` | Wooden grip centre |
| `kettle_anchor_handle_pivot` | Bail hinge-axis reference |
| `kettle_anchor_lid_seat` | Seated lid reference |
| `kettle_anchor_pour_pivot` | Candidate body pivot, requiring app calibration |
| `kettle_anchor_liquid_surface` | Suggested liquid surface centre/radius |

No liquid, steam, input handling, or ceremony animation is included in the asset. The application should own those behaviours.

## Verification and remaining work

All 14 evaluated meshes have zero boundary/non-manifold edges. The GLB has 44,936 triangles, eight semantic anchors, two embedded wood maps, and separate lid/handle hierarchies. Its size is approximately 2.35 MB.

Structural checks passed for the GLB header, mesh normals, textured UVs, anchors, hierarchy, embedded textures, and exclusion of studio/reference objects. Blender round-trip import recovered all meshes, anchors, and full-resolution packed maps, with matching dimensions and a base at zero. Four previews were rendered and inspected. The construction script also passed a Python syntax check.

These checks cover the standalone model. Application build/ceremony tests were not rerun because runtime code was unchanged. Before integration, calibrate physical-to-scene scale, resting height, tilt/pour pivot, ready pose, stream tip, interaction bounds, and overhead-handle clearance. Validate water pouring, release/cancellation, return, and restart. Mesh/texture optimisation and representative-device profiling remain part of production acceptance.

## References

User-supplied photographs:

- `Miyaco-Classic-Stainless-Steel-Kettle-1.5L-Made-in-Japan.webp`: overall silhouette, shoulder, spout, and upright handle.
- `Miyaco-Classic-Stainless-Steel-Kettle-03.webp`: bare steel cavity, detached lid, and grip layout.
- `Miyaco-Classic-Stainless-Steel-Kettle-05.webp`: timber grip, two rivets, metal strap/hinge, and wooden knob.

The photographs remain outside the repository and are not sampled into textures. Geometry and texture maps were constructed for this project.
