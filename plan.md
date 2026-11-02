# OjaTea — Visual identity plan

Updated: 2 November 2026. Status: proposed visual direction and geometry/behaviour separation plan; initial standalone kyūsu model study created, application integration pending.

## Phase 1 — Define the visual direction and palette

This is the first stage of the broader **Phase 3 — Visual identity** roadmap, corresponding to step 3.1 in [the visual identity plan](docs/phase-3-visual-identity.md). It does not restart the application's development phases.

The goal is a practical visual brief for the room, tea ware, materials, lighting, and interface. Use [design.md](design.md) as the implementation baseline: a seated, first-person sencha ritual with guided object movement, a quiet completion state, and desktop-first input. The deliverables below are planned work; this document establishes the starting decisions.

### 1.1 — Establish the direction

**Proposed direction: a quiet tea room in warm afternoon light.**

Build on the prototype's earthy greens, warm wood, cream ceramic, and restrained copper. The space should feel intimate, cared for, and inviting. Objects should have believable proportions and tactile surfaces, with subtle handmade variation. Keep the room visually simple so the visitor can immediately read the next action.

Use these principles to judge every visual choice:

- **The ritual leads:** the kyūsu, cup, kettle, caddy, and scoop remain the scene's clearest objects.
- **Materials carry the detail:** fine wood grain, ceramic texture, and restrained wear give surfaces character.
- **Light creates depth:** a soft directional source defines rims, spouts, handles, and contact with the tray.
- **Space creates calm:** leave breathing room around the tea setting and interface.
- **Feedback stays clear:** focus, selection, instructions, and preparation progress remain easy to recognise.

Deliverable: a short direction statement and a checklist for judging references and assets.

### 1.2 — Assemble a focused reference board

Collect approximately eight to twelve references, grouped by purpose:

| Reference group | What to look for | Decision it supports |
| --- | --- | --- |
| Room and composition | Intimate seated viewpoint, simple wall treatment, diffused window light, sparse decoration | Room proportions, background detail, negative space |
| Tea ware | Side-handled kyūsu, open ceramic cup, functional kettle, lidded caddy, bamboo scoop | Silhouettes, proportions, material relationships |
| Surface detail | Matte clay, warm ceramic glaze, fine wood grain, paper/plaster, aged copper | Texture scale, roughness, restrained imperfections |
| Light and atmosphere | Warm directional light, readable shadows, gentle background falloff | Light direction, warmth, exposure |

Annotate each reference with the specific feature to borrow and record its source. References guide the design; downloadable production assets require their own licence review. Keep visual choices appropriate to the existing sencha sequence without claiming historical reconstruction.

Deliverable: one annotated board with a clear preferred direction. Reference gathering is pending.

### 1.3 — Set the working palette

Use the following as the initial palette. Existing colours are retained where they already support the direction; the lighter wall and muted text colours are proposed refinements. These values are design targets, not new application tokens yet.

| Colour | Hex | Intended role |
| --- | --- | --- |
| Deep forest | `#20271F` | Page background, dark interface surfaces, room shadow reference |
| Moss | `#44483C` | Recesses, subdued room accents |
| Leaf green | `#526034` | Caddy detail and tea-leaf reference |
| Warm timber | `#6D513A` | Table base colour |
| Bamboo | `#9B8664` | Tray and scoop colour family |
| Clay | `#AA795B` | Proposed kyūsu body colour |
| Ceramic cream | `#D1C7AD` | Cup exterior and rim |
| Warm plaster | `#B6AD96` | Proposed light-facing wall/paper surface |
| Rice paper | `#F0EBDC` | Primary interface text |
| Muted parchment | `#C5C0B2` | Proposed supporting text on dark backing |
| Tea gold | `#D8C497` | Focus, progress, key controls, restrained emphasis |
| Infused tea | `#8D7940` | Starting reference for liquid colour |

Keep forest and moss in the background, warm wood through the middle of the scene, and cream/clay around the ritual's focal area. Reserve tea gold for meaningful interface emphasis. The cup's light interior should make liquid level and tea colour easy to see.

Review 3D colours under the actual renderer, tone mapping, and lights: a material's hex value will not match a flat interface swatch on screen. Check text and focus visibility against the final composited background, including bright window areas. Give essential guidance a reliable dark backing where needed; avoid relying on low-opacity text or colour alone to convey state.

Deliverable: a palette sheet showing colour roles, material samples, and legible interface combinations.

### 1.4 — Define the material family and object silhouettes

| Asset | Proposed appearance | Functional visual requirement |
| --- | --- | --- |
| Kyūsu | Reference-led squat body in dark iron-brown clay, recessed lid, short tapered spout, flared side handle wrapped in pale cord | Hollow body and open spout; removable lid with small knob/vent; side handle sits roughly perpendicular to the spout |
| Cup | Cream ceramic with a softly varied glaze and modest foot | Open interior, readable rim, visible tea surface, convincing close view during sipping |
| Kettle | Restrained aged copper with a charcoal handle | Clear spout tip and grip; highlights reveal shape without overwhelming the cup and pot |
| Caddy | Deep moss finish with a simple cream label | Lid/body separation and scoop entry are easy to read |
| Scoop | Pale bamboo with fine directional grain | Bowl and handle remain distinct at the seated camera distance |
| Table | Medium warm wood, low sheen, broad quiet grain | Supports clear object silhouettes and contact shadows |
| Tray | Slightly lighter bamboo/wood than the table | Visible usable surface and enough space for detached lids and guided movement |
| Room | Warm plaster/paper, darker timber framing, one restrained plant | Background depth and atmosphere while preserving clear views of the tea setting |

#### Kyūsu reference study — 2 November 2026

The three supplied photographs establish the kyūsu's specific direction, refining the earlier generic warm-clay proposal:

- A squat, rounded body with a broad shoulder, restrained foot, and circular open interior.
- Dark iron-brown, unglazed-looking clay with fine mineral speckling and subtle throwing marks.
- A recessed, gently dished removable lid with a small upright knob, concentric rings near the knob, and a small pressure vent.
- A short, upward-pointing tapered spout with a visible hollow mouth.
- A side handle at roughly a right angle to the spout, narrow through the grip and flared at the end, with pale natural-fibre cord around the shaft.

An initial editable Blender study and standalone GLB export now exist. See [the asset notes](assets/kyusu/README.md), [closed-lid preview](assets/kyusu/previews/kyusu-closed.png), and [open-lid preview](assets/kyusu/previews/kyusu-open.png). The study interprets the visible features; dimensions are inferred from photographs. It is not integrated into the ceremony, and its scale, poses, clearance, and runtime optimisation remain to be calibrated.

Reference filenames: `il_1588xN.8076310506_8lxw.webp` (underside/base and handle), `il_1588xN.8124230271_hmw0.webp` (open body and separate lid), and `il_1588xN.8124230291_9s4r.webp` (assembled three-quarter view). The photographs are visual references only and are not bundled into the runtime asset or used as textures.

Use subtle imperfections at the scale visible in normal play. Avoid oversized grain, heavy damage, bright metallic trim, or decorative details that obscure functional parts. Review the cup and kyūsu interiors early because the camera sees inside them.

Design these as independent assets suitable for external authoring and later import. Keep room, table, tray, tea objects, and removable lids separately addressable. Detailed texture/export specifications and anchor calibration belong to the next implementation stages.

Deliverable: one material and silhouette sheet with notes for each asset.

### 1.5 — Establish room composition and lighting

Keep the existing seated viewpoint and working arrangement as the starting composition. Position the kyūsu near the centre, cup to the visitor's right, kettle toward the left/rear, and caddy/scoop within clear reach. Preserve enough space for both pours, scoop travel, detached lids, and the cup's camera-relative sip pose.

Use a diffused window as the apparent main light source, aligned with a soft warm light from the upper left/front. Maintain gentle fill so dark objects remain readable. Keep the brightest background region away from critical instructions and use contact shadows to ground each object. Treat the existing HDR as a temporary lighting reference to evaluate against the new room.

Prepare composition studies for entry, preparation, pouring, sipping, and completion. Include desktop landscape and narrow portrait framing. Reserve quiet areas for the entry copy and lower guidance; ensure the held cup does not crowd the interface. Continue to respect reduced-motion preferences when presenting atmosphere.

Deliverable: a desktop composition study and a portrait companion, with light direction and interface zones marked.

### 1.6 — Align typography and interface treatment

Retain the current type family roles as the starting point:

- **Manrope:** instructions, controls, and general interface text.
- **Newsreader italic:** expressive entry and completion moments.
- **DM Mono:** short step labels, timers, and compact control hints.

Keep essential instructions comfortably readable at supported viewport sizes; do not copy the prototype's smallest label sizes into the final direction without review. Use rice-paper text, tea-gold focus/emphasis, thin borders, and dark translucent surfaces with sufficient backing. Preserve visible keyboard focus and explicit action labels. Maintain system font fallbacks.

Review the current brand mark as a provisional element. Use simple typography and a restrained mark; any culturally specific symbol or lettering should have a verified meaning before adoption. Public-facing labels should describe the ritual rather than development phase numbers. Audio control treatment can be finalised when sound functionality is implemented in its planned phase.

Deliverable: a small interface style sample covering entry, current-step guidance, progress, focus, and completion.

### 1.7 — Review the direction and prepare the asset brief

Bring the palette, materials, composition, and interface samples together into one reviewable scene study. Record decisions and any unresolved visual questions in this document. A static study can establish direction; final material and lighting acceptance must happen in the running scene after assets are integrated.

Completion checklist:

- [ ] Direction statement and annotated reference board are complete.
- [ ] Palette roles are clear, with readable text/focus combinations demonstrated.
- [ ] Each tea object has a silhouette and material brief.
- [ ] Room, table, tray, and decoration are defined as independent assets.
- [ ] Desktop and portrait studies preserve object visibility and interface space.
- [ ] Entry, active ritual, and completion share a consistent visual language.
- [ ] Asset brief identifies separate lids, open interiors, and movement clearance needs.
- [ ] The chosen direction and remaining questions are recorded before full asset production.

## Phase 2 — Separate geometry from interaction behaviour

This stage corresponds to step 3.2 of the broader visual identity roadmap. Its outcome is the existing procedural scene organised so a model can later be replaced without rewriting input, movement, or ceremony rules. Preserve the current appearance during this refactor; the Phase 1 palette remains a proposal for later visual work.

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
