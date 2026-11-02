# Cup — oatmeal ceramic reference study

Created 2 November 2026 in Blender 5.2.3 LTS through Blender MCP, following the kyūsu workflow. This is a standalone visual asset; the running ceremony still uses the procedural cup.

## Design and dimensions

The user supplied three photographs and these specifications: ceramic, oatmeal colour, 6 cm tall, 180 ml capacity. The model interprets the rounded handleless body, slightly narrowed mouth, modest foot, fine glaze speckles, and narrow iron-brown rim. The inner wall and floor form a real cavity; the lip is rounded, and the underside has an exposed-clay contact ring.

| Measurement | Model |
| --- | --- |
| Height | Approximately 59.9 mm |
| Maximum diameter | Approximately 78.1 mm |
| Interior opening diameter | Approximately 65.8 mm |
| Estimated brim capacity | 177.6 ml |
| Estimated fill at provisional liquid anchor | 151.0 ml, leaving headroom |

Brim capacity is estimated from 600 horizontal ray samples of the evaluated interior, integrated as circular cross sections. Subtle asymmetry and the simplified measurement method make this approximate. It is close to the requested nominal 180 ml. The model uses the same physical metre scale as the existing kyūsu, with no scaling applied to either object in the comparison render.

## Files

- `cup-reference.blend`: editable cup with its subdivision modifier, packed maps, preview studio, and a second scene for comparison. Previously open scenes are preserved; use `OjaTea | Oatmeal cup study` for the cup and `OjaTea | Cup and kyusu proportions` for the pair.
- `../../public/models/cup-reference.glb`: only the cup mesh, root, anchors, materials, and embedded textures; no studio, camera, lights, or kyūsu.
- `build_cup.py`: Blender Python construction source. Creates new scenes, preserves existing work, and refuses to overwrite existing cup output. It sets up previews; render them through Blender. It does not run in the website.
- `textures/cup_oatmeal_basecolor.png`: generated glaze colour, mineral flecks, and brown lip transition.
- `textures/cup_oatmeal_normal.png`: subtle tangent-space surface texture.
- `previews/cup-hero.png`: elevated view of the glaze, rim, and interior.
- `previews/cup-front.png`: front silhouette and foot.
- `previews/cup-with-kyusu.png`: proportion/material comparison at shared physical scale.
- `asset-metadata.json`: dimensions, estimated capacities, anchors, geometry checks, and file size.
- `export-validation.json`: GLB structure and Blender import verification results.

The comparison scene links the saved `../kyusu/kyusu-reference.blend` export collection rather than changing the live kyūsu scene. Keep that relative file available when opening the comparison. The cup model and exported GLB are independent of that preview link. The cup source file was saved under a new path; the existing kyūsu source was not overwritten.

## Material and hierarchy

The glazed body uses two generated 2048 × 512 maps, laid out to retain small speckles around the circumference. Both maps are packed into the source and embedded into the GLB. Glaze and exposed foot are two material slots on one mesh. A restrained clear coat gives the surface a ceramic sheen. Photos are not sampled into the maps.

`cup_root` is the asset root; `cup_body` is its mesh child. Blender uses +Z up, GLB uses +Y up, and the evaluated base is rebased to zero for surface contact. The remaining semantic children are:

| Anchor | Purpose |
| --- | --- |
| `cup_anchor_base` | Surface contact at the origin |
| `cup_anchor_opening` | Receiving opening and approximate radius |
| `cup_anchor_liquid_surface` | Suggested centre/radius for a liquid surface with headroom |
| `cup_anchor_sip_edge` | Candidate drinking point at the +X side of the rim |
| `cup_anchor_grip` | Body-centred grip/presentation reference |

No liquid mesh is baked into the asset. The future runtime wrapper will attach dynamic liquid and interaction behaviour using calibration data.

## Verification and next steps

The evaluated cup shell has 28,160 triangles and zero boundary/non-manifold edges. The 2.89 MB GLB contains one mesh with two material primitives, five anchors, and two embedded maps. GLB header, attributes, hierarchy, embedding, and studio exclusion checks passed. Blender round-trip import recovered the mesh, all five anchors, both full-resolution image buffers, the expected height, and a base at zero.

The hero, front, and proportion views were rendered and inspected. These checks cover the standalone asset. No application code was changed; ceremony tests were not rerun and the new model is not yet integrated.

Next, calibrate physical-to-scene scale, receiving radius, home position, sip pose/orientation, liquid bounds, and hit area. Verify pouring, sipping, return, interruption recovery, and restart in the app. Mesh/texture optimisation and representative-device profiling are still required for production acceptance.

## References

User-supplied files:

- `1451-1_c5212-b-800px.webp`: upright cup, tilted cup, interior, and relative proportions.
- `1451-11_c5212-front.webp`: front shape, glaze, brown rim, and base ring.
- `c5212-detail-1080px.webp`: opening, interior, glaze speckles, and rim detail.

The photographs remain outside the repository. Geometry and texture maps were constructed for this project; exact manufacturer replication is not claimed.
