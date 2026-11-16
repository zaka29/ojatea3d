# OjaTea — Visual identity plan

Updated: 14 November 2026. Status: standalone tea-ware and furnishing studies reviewed; working asset brief prepared. Phase 1 now uses the built setting as its baseline; room/scoop blockouts and seated scene/UI studies remain. Application integration and geometry/behaviour separation remain pending.

## Phase 1 — Consolidate the built tea setting and resolve the room/UI direction

This is roadmap step 3.1, **Visual brief**, within the broader [Phase 3 visual identity roadmap](docs/phase-3-visual-identity.md). The baseline is now the authored tea setting, rather than a new search for a style. Preserve the seated, first-person sencha sequence in [design.md](design.md).

**Current baseline:** four tea vessels and separate table/tray assets have editable Blender sources, GLB exports, materials, anchors and inspected previews. They have been staged together at physical metre scale. The app still uses procedural objects. The scoop, room shell and plant have no external asset study yet.

**Phase outcome:** a concrete handoff specifying what to retain from those assets, what remains to design, and how to judge the setting with the interface. Asset import, movement calibration and final renderer acceptance follow in later stages.

### 1.1 — Retain the built material family

**Direction established:** dark iron-brown clay, oatmeal ceramic, charcoal steel and charcoal caddy on a dark inlaid timber tray, supported by a weathered plank table. Pale cord, wood grips and bamboo provide small lighter accents. Build the room around this setting.

Use these decisions for subsequent work:

- Keep the kyūsu squat, side-handled and cord-wrapped; retain its dark clay finish and recessed lid.
- Keep the cup rounded and handleless, with oatmeal speckles, a fine brown rim and exposed-clay foot.
- Keep the kettle charcoal outside and stainless inside, with the riveted wooden bail grip. The earlier copper proposal is retired.
- Keep the tea box plain charcoal with a loop lid and pale underside seal. The earlier green labelled caddy is retired.
- Keep the weathered table distinct from the smoother, darker tray. Retain the tray's offset pale inlay, channel and separate pan; do not add a raised perimeter rim.
- Add a pale bamboo scoop and a restrained plaster/timber room. Keep decorative detail outside the tea-object silhouettes and guidance area.

**Status:** direction recorded. No new vessel style search is required. Detailed source-photo annotations and modelling decisions remain in the linked asset READMEs below.

### 1.2 — Use the existing studies as the reference set

The [shared tabletop study](assets/room-setting/previews/room-setting-tabletop.png) is the starting material/composition reference. The [wide study](assets/room-setting/previews/room-setting-wide.png) shows furniture structure. Neither establishes the seated camera or the finished room.

| Reference | Retain | Remaining decision |
| --- | --- | --- |
| [Kyūsu notes and previews](assets/kyusu/README.md) | Body/handle/spout relationship, cord, recessed vented lid, dark mineral clay | Check dark iron-brown appearance under runtime light |
| [Cup notes and previews](assets/cup/README.md) | Oatmeal glaze, brown lip, rounded hollow body, shallow foot | Keep glaze detail visible without the cup washing out |
| [Kettle notes and previews](assets/kettle/README.md) | Charcoal shell, bare steel cavity and pouring lip, independent bail/lid, riveted grip | Readable dark silhouette and overhead clearance |
| [Tea-box notes and previews](assets/teabox/README.md) | Plain charcoal cylinder, brown interior, separate loop lid and pale seal | Scoop size/access and detached-lid space |
| [Table/tray notes and previews](assets/table-tray/README.md) | Weathered planks, dark rounded slab, pale inlay/channel and catch pan | Reduce distracting reflections if they persist in the running scene |

**Remaining reference task:** select a seated room/window reference and a bamboo-scoop reference, annotate the feature to borrow and record source provenance. Assemble these alongside the existing previews in one review sheet. Do not collect an arbitrary new set of eight to twelve tea-ware images. Existing photographs remain visual references outside runtime packages; third-party production assets need their own licence review.

### 1.3 — Set the working palette

Separate authored material appearance from flat interface colours. The built textures and PBR materials define the tea ware and furniture; do not tint them to match the prototype's old colour table.

| Material family | Current target | Source of truth |
| --- | --- | --- |
| Kyūsu | Dark iron-brown mineral clay with pale natural-fibre cord | Kyūsu source materials/textures and reference notes |
| Cup | Oatmeal speckled glaze, narrow iron-brown lip, exposed-clay foot | Cup source materials/textures and reference notes |
| Kettle | Matte charcoal exterior, bright stainless interior/lip, warm wood grip/knob | Kettle source materials and wood maps |
| Tea box | Fine charcoal texture, darker brown rim/interior, pale lid seal | Tea-box source materials/textures |
| Table / tray | Weathered timber / darker warm walnut-coloured slab with pale inlay | Separate table/tray wood maps and materials |
| Scoop | Pale directional bamboo | To be authored against the caddy opening |
| Room | Warm plaster/paper, dark timber frame, muted green plant | To be demonstrated in the room study |

Retain these explicit UI/environment targets for the next sample; they are not implemented theme tokens:

| Role | Hex | Use |
| --- | --- | --- |
| Deep forest | `#20271F` | Page and reliable guidance-panel backing |
| Moss | `#44483C` | Recesses and subdued room accents |
| Leaf green | `#526034` | Leaves and restrained plant accents |
| Warm plaster | `#B6AD96` | Starting wall/paper colour under the key light |
| Rice paper | `#F0EBDC` | Essential interface text |
| Muted parchment | `#C5C0B2` | Supporting text on dark backing |
| Tea gold | `#D8C497` | Keyboard focus, progress and key controls |
| Infused tea | `#8D7940` | Starting liquid reference, reviewed inside the oatmeal cup |

The old `#AA795B` kyūsu and single-colour timber/ceramic swatches are superseded by the authored materials. Evaluate their screen appearance under runtime tone mapping and lights before changing textures.

**Remaining deliverable:** one sheet combining the authored material crops with these UI swatches and a guidance/focus sample over both a dark and a bright scene region. Essential text should reach 4.5:1 contrast and focus indicators 3:1 against adjacent colours; measure the composited backing rather than an isolated swatch. Pair state colours with labels or shape changes.

### 1.4 — Hand off the existing assets and specify the missing ones

| Asset | Existing dimensions / structure | Preserve and validate later | Status |
| --- | --- | --- | --- |
| Kyūsu | Squat body, hollow cavity/open spout, separate recessed lid, perpendicular flared cord-wrapped handle | Opening/spout/liquid/lid-seat anchors; receiving and pouring alignment; handle sweep and lid-rest clearance | Standalone source/GLB complete; integration pending |
| Cup | About 59.9 mm high × 78.1 mm wide; approximately 178 ml brim capacity | Hollow interior, rounded lip, base/opening/liquid/sip anchors; provisional 151 ml liquid anchor leaves headroom and does not prescribe serving volume | Standalone source/GLB complete; integration and second variant pending |
| Kettle | About 226 × 160 × 177.5 mm with handle upright; separate lid and hinged bail | Open steel cavity/spout, pointed pouring lip, lid seat and hinge axis; tilt, stream endpoint and overhead clearance | Standalone source/GLB complete; integration pending |
| Tea box / caddy | About 90 mm diameter, 100 mm to opening, 126 mm overall; hollow body and separate lid group | Keep loop, disc, insert and seal together; opening/scoop-entry/lid-seat anchors; full scoop access | Standalone source/GLB complete; integration pending |
| Table | About 1.60 × 0.849 m; surface 0.72 m above floor | Separate root/surface anchor; retain documented inferred legs, aprons and stretchers | Standalone source/GLB complete; integration pending |
| Tray / pan | 0.84 × 0.44 × 0.036 m; independent pan, 0.20 m open study offset | Service/channel/pan anchors; spare lid positions; keep vessel feet off channel. Drainage is visual, with no fluid simulation | Standalone source/GLB complete; integration pending |
| Scoop | Pale bamboo, shallow bowl and narrow handle; dimensions not established | Author a proportion study that enters the approximately 82 mm caddy opening and clears its rim; define bowl, grip and leaf attachment points | External study needed |
| Room shell | Warm plaster/paper with dark timber frame; dimensions not established | Independent root, floor/origin, window reference; derive dimensions from seated camera and movement envelopes | Room study needed |
| Plant | One muted green plant in a quiet container | Independent decorative root outside tea silhouettes and movement paths | Final external study needed |

Keep Blender sources, asset-only GLBs, packed/baked PBR maps, named moving parts, semantic anchors, metadata and checked previews together. Use metres, +Z up in Blender and +Y up in GLB, with base-at-zero contact. Preserve existing node names; later manifest mappings can resolve differences between assets. Do not bake liquid, leaves, steam, input or ritual transitions into models.

**Status:** written asset brief prepared in [docs/asset-brief.md](docs/asset-brief.md). Existing exports have standalone validation, not production performance acceptance. Set resource/texture budgets in roadmap 3.3 before expanding production.

### 1.5 — Resolve the seated room composition and lighting

Use the [furnishing study metadata](assets/room-setting/setting-metadata.json) as a scale reference. Its table-plus-tray surface is 0.756 m above the floor. Its four vessel bases are within 2 mm of the service surface and their static footprints pass service-zone checks. Those physical coordinates are not calibrated application positions.

Retain the arrangement: kettle left/rear, kyūsu near centre, cup right, caddy behind/within reach, scoop in an accessible clear service area. Reserve independent tea-box and kyūsu lid-rest footprints. Keep feet and scoop travel off the drainage channel.

**Next study:** place the existing assets plus a scoop blockout in a simple room shell. Start with warm plaster/paper, dark timber framing and one diffused window upper-left/front. Add gentle fill and contact shadows. Keep the existing HDR provisional. Do not model more decoration until the working surface, dark vessels and guidance are readable.

Produce a paired contact sheet at **1440×900 desktop** and **390×844 portrait**, using the seated application camera as the starting point. Show entry, leaf transfer, water pour, tea pour, held-cup sip and completion. Mark the entry-copy area, lower guidance/progress area, controls, light direction, lid-rest areas and moving-object envelopes. Use pose blockouts where motion is not integrated; label them as such.

Acceptance for this study:

- All required objects and the current action remain visible at both aspect ratios.
- Held-cup and pour poses leave guidance and controls unobscured.
- Caddy/kyūsu lids clear the scoop and vessels; kettle bail and kyūsu handle clear the room and neighbouring objects throughout the proposed paths.
- The cup retains oatmeal/rim detail; kyūsu reads dark iron-brown; kettle and caddy separate from the background; tray reflections do not dominate.
- Reduced-motion presentation retains the same information without decorative motion.

**Status:** elevated furnishing study exists; seated room, portrait and ritual-pose contact sheets remain to be made. Actual motion and material/light acceptance follow after integration.

### 1.6 — Demonstrate the interface over this setting

Retain Manrope for guidance/controls, Newsreader italic for entry/completion, and DM Mono for short labels/timers, with system fallbacks. Start essential guidance at 14–16 px and secondary labels at 12 px in the sample; check at both target viewports. Replace the prototype's faint 8–11 px guidance where it carries essential information.

Create three panels over the composition study:

| State | Required content and treatment |
| --- | --- |
| Entry | Restrained brand, expressive title, short ritual description and explicit start action; clear keyboard focus |
| Active ritual | Step label, action instruction, input hint and progress/timer on reliable dark backing; selected-object label and focus sample |
| Completion | Quiet completion message and explicit restart action using the same type, backing, border and focus language |

Use the UI colours from 1.3. Show the brightest background behind a panel as well as the darker tabletop case. Public copy describes the ritual rather than development phase numbers. Keep the current mark provisional until its meaning is verified; sound-control details remain with the sound phase.

**Status:** prototype typography exists; these scene-backed, legible UI samples remain to be made.

### 1.7 — Review the direction and prepare the asset brief

The [asset brief](docs/asset-brief.md) records the current review and technical handoff. The built tea ware and furniture establish the baseline; their style does not need to be chosen again. Review the remaining room, scoop, lighting and UI decisions against that baseline.

Completion checklist:

- [x] Record the built material family and retire conflicting generic proposals.
- [x] Identify existing sources, previews, dimensions, separate parts and anchors.
- [x] Specify the missing scoop, room and decoration studies.
- [x] Record open interiors, lid separation and movement-clearance requirements.
- [ ] Assemble existing previews plus the selected room/scoop references into one annotated review sheet with source notes.
- [ ] Demonstrate material/UI palette and measured text/focus contrast on scene backing.
- [ ] Produce the paired seated desktop/portrait contact sheets specified in 1.5.
- [ ] Show entry, active ritual and completion UI over the chosen setting.
- [ ] Record the resulting room/light/UI decisions and carry unresolved runtime checks into integration.

**Next concrete work:** make the room/scoop blockout and paired composition contact sheets, then add the UI/material review sheet. Phase 1 closes when those artifacts resolve the remaining design choices. It does not require final assets for the room/plant, calibrated animation, a new loader, or production performance certification.

Carry the existing [Phase 2C focused browser verification gap](docs/phase-2c-qa.md) into the start of Phase 2. Final material, light and movement acceptance remains in the running scene after import.

## Phase 2 — Separate geometry from interaction behaviour

This stage corresponds to step 3.2 of the broader visual identity roadmap. Its outcome is the existing procedural scene organised so a model can later be replaced without rewriting input, movement, or ceremony rules. Preserve the current appearance during this refactor; the authored material direction and Phase 1 UI targets are applied only in the later integration/visual passes.

### 2.1 — Record the baseline and ownership boundaries

Start with the outstanding focused browser checks listed in [the Phase 2C QA report](docs/phase-2c-qa.md), then record the current scene at entry, leaf transfer, both pours, sipping, and completion. Use existing tests and diagnostics as the behavioural reference.

Assign each responsibility a single owner:

| Layer | Owns | Boundary |
| --- | --- | --- |
| Ritual state | Store actions, step guards, fill/sip/steep progress, recovery and restart | Retain `store.ts` and ritual metadata; models never advance the ceremony |
| Object behaviour | Pointer/keyboard input, selection, hover state, outer movement refs, lid choreography, progress callbacks | Reads store state and passes explicit visual props; retains current event guards and cleanup |
| Visual model | Static geometry, materials, shadows, local mesh offsets, hover appearance | Receives props and named part refs; no store imports, input listeners, or ceremony transitions |
| Runtime effects | Liquid, leaf deposits, steam, pour-stream rendering | Receives presentation values and attachment transforms; never independently decides whether transfer is allowed |
| Scene composition | Room/table placement, lights, camera, atmosphere, lifecycle and diagnostics | Composes independent modules without hiding object behaviour inside furniture geometry |

Deliverable: baseline evidence and an agreed ownership map. Keep existing object names and telemetry meanings intact so tests continue to observe the same objects.

### 2.2 — Establish a small module structure

Use the following target layout, adding files only as their contents are extracted:

```text
src/
  scene/
    Scene.tsx                 # composition and scene-ready lifecycle
    SceneLighting.tsx         # lights, HDR, background and fog
    SceneAtmosphere.tsx       # decorative particles; reduced-motion handling
    CameraRig.tsx
    RecoveryGuard.tsx
    SteepingSystem.tsx
    models/
      RoomModel.tsx
      TableModel.tsx
      TrayModel.tsx
      CupModel.tsx
      CaddyModel.tsx
      ScoopModel.tsx
      KettleModel.tsx
      KyusuModel.tsx
    objects/
      Cup.tsx
      Caddy.tsx
      TeaScoop.tsx
      Kettle.tsx
      Kyusu.tsx
    effects/
      VesselLiquid.tsx
      TeaLeaves.tsx
      Steam.tsx
  components/
    GuidedPour.tsx            # retain existing shared pour controller
  sceneLayout.ts             # shared placement and calibration
```

Keep `App.tsx` responsible for application entry, canvas configuration, and the interface. Moving the interface into its own file is optional housekeeping, not a prerequisite. Do not introduce a generic interaction engine or a new animation library.

Deliverable: modules with explicit imports and no circular dependencies. Dependency direction is scene composition → behaviour wrappers → models/effects; models do not import wrappers or the store.

### 2.3 — Extract the cup as the first complete example

Move the existing cup behaviour intact into `scene/objects/Cup.tsx`. It continues to own the animated root group, camera-relative sip pose, pointer capture, keyboard handlers, hover state, and drink-stage transitions. Extract only the ceramic meshes into `CupModel.tsx`; pass hover appearance as a prop. Render the liquid as a separate visual child driven by the existing fill/drink values.

Use the original root pivot and local coordinates. Do not add a transformed parent or recenter the model: that would change resting height, pour alignment, and sipping. Confirm selection, hold/release, partial-sip cancellation, return, and restart before using this split as the pattern for other objects.

Deliverable: one fully separated procedural cup with unchanged interaction and appearance. Imported cup variants remain the later asset-pipeline milestone.

### 2.4 — Extract the other tea objects incrementally

| Order | Extraction | Specific checks |
| --- | --- | --- |
| Caddy | Body/lid visuals into the model; open/close input and lid movement remain in its wrapper | Lid seats correctly, clears scoop entry, and closes at the same ritual point |
| Scoop | Handle/bowl into the model; carried leaves into an effect; waypoints and deposits remain in the wrapper | Two deposits, safe cancellation lift/clear/return, and unchanged home contact |
| Kettle | Body/handle/spout into the model; wrapper continues to configure `GuidedPour` | Source spout, ready pose, tilt, stream, and fill progression remain aligned |
| Kyūsu | Body/handle/spout/lid visuals into the model; liquid/leaves/steam into effects | Lid rests on tray, both receiving and pouring openings align, and steep colour/progress stay unchanged |

The behaviour wrapper owns each moving lid's group/ref and frame updates. Supply the lid geometry as a separate exported part or explicit slot, so geometry can change without taking ownership of its motion. Preserve current lid parenting during this extraction; changing how a detached lid follows its vessel is a separate behavioural change.

Keep `GuidedPour` responsible for vessel input and motion. Its existing children boundary already supports replaceable visuals. Preserve the single `canPour` predicate shared by transfer and stream visibility; do not duplicate pour rules inside a model or effect.

Deliverable: all five objects have separate procedural visuals and behaviour, verified one at a time.

### 2.5 — Separate the room and supporting surfaces

Extract architecture/decoration, table, and tray visuals from the current `Room`/`Table` functions. Move lights, HDR, background/fog, particles, and contact shadows into appropriate scene-level composition modules. Keep contact shadows attached to the configured tray surface.

Compose tea objects and `SteepingSystem` directly in the scene rather than mounting them inside `TableModel`. Preserve the original world transforms when removing nested groups, including any identity groups used by diagnostics. Keep the existing HDR path, lighting values, camera behaviour, and reduced-motion settings.

Deliverable: removing or replacing furniture visuals does not unmount the ritual controllers or change object coordinates.

### 2.6 — Make presentation inputs explicit

Define small, typed props per model/effect rather than passing the store or its action functions. Pass hover appearance, liquid amount/colour, leaf count/visibility, and steam activity only where needed. Models may calculate visual presentation from these props; only behaviour wrappers submit progress or transition actions.

Keep placement and behavioural calibration in `sceneLayout.ts`: resting heights, openings, spout offsets, ready poses, pour angles, lid seating/rest transforms, and scoop clearance points. Move currently embedded values there only where doing so improves the boundary, preserving their exact values. Geometry-specific data such as `kyusuBodyProfile` belongs beside its procedural model; retain explicitly documented matching bounds for layout calculations.

Use stable refs for animated parts and avoid React state updates on every frame. Ensure every transform has one writer: the outer controller moves the object, a lid controller moves its lid group, and visual children remain in local coordinates. Extract shared effect code only when shapes and behaviour genuinely match; separate cup/pot liquid renderers are acceptable.

Keep current mesh-based hit testing during this refactor. Independent interaction proxies, imported-node anchor resolution, loaders, asset manifests, fallback/error handling, and material variant management belong to step 3.3. The separation should make those additions possible without implementing them here.

Deliverable: documented visual props, part refs, and calibration ownership, with no model-to-store dependency.

### 2.7 — Verify and document the result

Run `npm run build` and `npm test`, then the relevant existing browser scenarios while each object is extracted. At the end, run the full Chromium ceremony suite once; repeat only when a subsequent change or failure warrants it. Review matching screenshots for material appearance, shadows, labels, liquids, lid seating, and contact with the tray.

Use existing diagnostics to compare home positions, pour endpoints, and renderer resource counts across restart. Investigate unexpected geometry/material duplication or new frame work. This extraction should not make new performance claims or change the pending representative-hardware profiling requirements.

Completion checklist:

- [ ] Outstanding baseline browser checks have been resolved or any remaining gap is explicitly documented.
- [ ] `App.tsx` composes the scene without containing tea-object geometry or choreography.
- [ ] Each model is independent of the ritual store, input listeners, and transition actions.
- [ ] Behaviour wrappers own moving roots and lid transforms with no competing writers.
- [ ] Runtime effects receive presentation inputs and share existing transfer validation.
- [ ] Room, table, and tray visuals are separate from object/controller lifetime.
- [ ] Mesh coordinates, pivots, calibration values, object names, and telemetry remain compatible.
- [ ] Mouse/keyboard flow, interruption recovery, reduced motion, portrait framing, and repeat/restart pass.
- [ ] Build, unit tests, full browser results, and visual comparison are recorded.
- [ ] `design.md` describes the implemented module structure and replacement boundary.

Suggested implementation commits: cup split; remaining tea-object splits in reviewable increments; environment/composition extraction; final documentation and verification. Keep every commit buildable. This planning update is a documentation-only commit.

## Next stage

After the visual brief, separate procedural geometry from behaviour and establish the import contract. Prove the workflow with two interchangeable cup models before producing the complete scene, following [steps 3.2–3.4](docs/phase-3-visual-identity.md).

This planning stage covers visual decisions and review artifacts. Model production, asset loading, behaviour refactoring, new liquid effects, sound, and touch-control implementation retain their existing roadmap positions in [design.md](design.md).
