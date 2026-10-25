# Phase 3 — Visual identity

Planning date: 24 October 2026. Status: proposed; no asset-loading infrastructure has been implemented by this plan.

## Outcome

Make every tea object, the table/tray, and the room replaceable with externally authored assets. Keep ceremony behaviour in application code, and move appearance into models, materials, textures, and a shared theme configuration.

The current procedural scene is the working reference. `src/App.tsx` contains both geometry and behaviour; `src/sceneLayout.ts` supplies shared resting heights and opening positions. Preserve the ritual store and guided interaction flow while introducing asset boundaries.

## Small delivery steps

| Step | Work | Completion check |
| --- | --- | --- |
| 3.1 — Visual brief | Choose references, palette, ceramic finish, wood grain, room style, light direction, and UI typography. Produce one palette/material board and a target scene composition. Treat the current earthy palette as a starting proposal. | One agreed direction with a list of required assets. |
| 3.2 — Separate appearance and behaviour | Extract room, table, and individual object modules from `App.tsx`. Keep selection, guided motion, state, and liquid effects in behaviour wrappers; place visible geometry inside replaceable visual children. | Existing procedural scene looks and behaves the same; relevant build, unit, and ceremony checks pass. |
| 3.3 — Define the asset contract | Introduce a typed asset manifest, GLB loader, procedural fallback, loading/error states, and validation for required parts and anchors. Document scale, orientation, pivots, bounds, and material names. | Missing or invalid assets produce a clear diagnostic and a usable fallback. |
| 3.4 — Prove one replacement | Import a simple externally authored cup, calibrate its base, rim, liquid interior, pickup/sip pose, and hit area. Swap between two cup variants through configuration. | Both variants complete pouring, sipping, return, and restart without changing ceremony logic. |
| 3.5 — Replace tea ware incrementally | Integrate caddy and removable lid, scoop, kettle, then kyūsu and removable lid. Recheck each object's interaction before the next replacement. | Every object can be independently selected in the manifest; lids, stream endpoints, liquid and return poses align. |
| 3.6 — Import the environment | Add separate room and table/tray assets. Separate decorative geometry from interactive surfaces. Configure room origin, table/tray surface, object layout, and camera framing. | Two compatible environment variants can be selected; objects rest on the tray and all guided paths remain clear. |
| 3.7 — Materials, textures, and colours | Add named material slots, texture sets, and shared theme tokens. Support authored finishes and optional tint overrides. Connect UI colours, fog, lights, and liquid colours to the same direction. | A palette or finish variant can be selected without editing mesh components. |
| 3.8 — Lighting and composition | Tune runtime lights, HDR environment, exposure, shadows, and camera against the chosen materials. Compare desktop and portrait views, including a vessel held near the camera. | Main objects and instructions remain legible, with consistent material appearance across ritual states. |
| 3.9 — Acceptance and handoff | Validate exports, licences, missing textures, load failures, asset sizes, renderer counts, and representative-device performance. Run the complete ceremony and compare screenshots. Document the replacement workflow. | A second asset can be exported, registered, and used by following the guide; build and regression checks pass. |

Sequence: 3.1 → 3.2 → 3.3 → 3.4, then incremental tea ware and environment production, followed by the final material/lighting and acceptance passes. Establish material names and provisional export budgets during 3.3, before producing the full set.

## External design workflow

Use GLB (glTF 2.0) as the runtime exchange format. Keep editable source files separately; export runtime files into `public/models/`. Blender is a suitable reference authoring/export workflow. Assets made in other tools or purchased from libraries can enter the same pipeline after conversion and calibration.

```text
Editable design source → export/convert to GLB → validate and optimise
                      → register asset and calibration → preview → ceremony checks
```

GLB can carry meshes, standard PBR materials, textures, and animations. Arbitrary authoring-tool shaders do not transfer automatically: bake unsupported procedural materials into image textures. Keep dynamic ceremony lights and camera control in the app; do not automatically activate imported cameras or lights. An HDR provides illumination/reflections and does not replace room geometry.

This phase provides a developer/designer asset workflow: replace files and update configuration. A visitor-facing upload tool or visual scene editor would be a separate feature.

## Replacement contract

Each asset entry should contain its file URL, scale/orientation correction, local base height, named parts, anchor mapping, interaction bounds, material overrides, and any required pose calibration. Validate the exported result in app coordinates: +Y up, consistent documented scene units, and a stable root transform. Calibrate to the existing scene before attempting any global unit conversion.

| Asset | Required information |
| --- | --- |
| Cup | Base, rim/opening centre and radius, liquid interior, sip orientation, hit area |
| Kyūsu | Base, spout tip, opening centre and radius, removable lid/root and seating pose, liquid interior, tilt pivot |
| Kettle | Base, spout tip, tilt pivot, opening/visible interior if applicable |
| Caddy | Base, opening, lid/root and seating pose, scoop entry clearance |
| Scoop | Rest bounds, bowl/deposit point, handle/grip orientation, clearance envelope |
| Table/tray | Surface anchor, usable bounds, origin and object layout compatibility |
| Room | Origin, usable space, camera/look limits, decoration clearance and material slots |

Prefer named empty nodes in the authored model for anchors; support explicit local-coordinate metadata when a third-party asset lacks them. Keep lids as independently addressable nodes. Derive world-space pour targets from transformed local anchors rather than keeping the current hard-coded spout offsets.

The behaviour wrapper owns movement and input. A small interaction proxy provides a predictable hit area independent of decorative mesh detail. Dynamic liquid, steam, streams, hover feedback, and leaf deposits remain runtime elements attached to the asset's anchors. Open cups and pots need convincing interior geometry; sealed marketplace meshes may require editing.

Replacement is straightforward when assets obey the same contract. A wider pot, differently directed spout, or taller table requires configuration and clearance validation; changing the file alone cannot guarantee compatible motion. Include ready poses, pour angle, detached lid position, and scoop waypoints in calibration where necessary. Validate anchors in tilted/held poses as well as at rest.

## Room, textures, and palette

Keep room architecture, table, tray, and decoration independently replaceable. Let an environment configuration bind the room to surface anchors, layout, camera, lighting, fog, and background. A radically different room may need its own layout preset.

Use named material slots such as `ceramic.body`, `wood.table`, `wall.plaster`, and `metal.kettle`. Author base colour, roughness, metalness, normal, and optional occlusion maps externally. Colour-only variants can use neutral base textures plus tint values; already coloured textures will multiply with the tint, so use alternate texture sets for substantially different finishes. Clone materials before per-instance edits to avoid changing other models sharing a loaded asset.

Put UI colours and typography in shared CSS tokens; expose matching 3D palette and lighting values through theme configuration. Palette changes should be central edits. Detailed wood grain, glaze variation, labels, and wear should come from authored textures rather than more geometry code.

## Scope and acceptance

- First implementation slice: 3.2–3.4, ending with two swappable cup assets. This proves the pipeline before investing in the complete asset set.
- Close the outstanding focused Phase 2C browser verification gap before accepting behavioural refactoring; the existing QA report describes the deferred checks.
- Keep runtime assets local and record source, author, licence, attribution requirements, and modifications for third-party assets.
- Set provisional download, texture-resolution, triangle, and draw-call budgets during the pilot, using measured production-build behaviour on representative hardware. Do not treat automated Chromium timings as hardware certification.
- Validate required anchors, parts, and bounds with focused tests. Use existing browser coverage for full ceremony, interruption/recovery, repeat/restart, reduced motion, and viewport framing. Add checks for fallback/loading failures and variant alignment.
- Full liquid simulation, new tactile effects, sound, comprehensive touch controls, and an in-app design editor remain outside this phase. Basic asset-loading reliability and optimisation belong here even though broader delivery work is planned for Phase 7.

## Export references

- [Three.js: loading 3D models](https://threejs.org/manual/pages/loading-3d-models.html)
- [Blender: glTF 2.0 export and materials](https://docs.blender.org/manual/en/4.2/addons/import_export/scene_gltf2.html)
- [Khronos glTF registry](https://registry.khronos.org/glTF/)
