# OjaTea — Visual identity plan

Updated: 25 October 2026. Status: proposed direction, ready for visual exploration.

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
| Kyūsu | Matte warm clay, subtle surface variation, dark interior | Side handle and spout read clearly; lid is a separate part; opening stays visible during leaf and water transfer |
| Cup | Cream ceramic with a softly varied glaze and modest foot | Open interior, readable rim, visible tea surface, convincing close view during sipping |
| Kettle | Restrained aged copper with a charcoal handle | Clear spout tip and grip; highlights reveal shape without overwhelming the cup and pot |
| Caddy | Deep moss finish with a simple cream label | Lid/body separation and scoop entry are easy to read |
| Scoop | Pale bamboo with fine directional grain | Bowl and handle remain distinct at the seated camera distance |
| Table | Medium warm wood, low sheen, broad quiet grain | Supports clear object silhouettes and contact shadows |
| Tray | Slightly lighter bamboo/wood than the table | Visible usable surface and enough space for detached lids and guided movement |
| Room | Warm plaster/paper, darker timber framing, one restrained plant | Background depth and atmosphere while preserving clear views of the tea setting |

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

## Next stage

After the visual brief, separate procedural geometry from behaviour and establish the import contract. Prove the workflow with two interchangeable cup models before producing the complete scene, following [steps 3.2–3.4](docs/phase-3-visual-identity.md).

This planning stage covers visual decisions and review artifacts. Model production, asset loading, behaviour refactoring, new liquid effects, sound, and touch-control implementation retain their existing roadmap positions in [design.md](design.md).
