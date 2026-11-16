# Python asset-authoring style guide

Use readable PEP 8 conventions, descriptive names, and type hints where practical for Blender construction and validation scripts.

Document the required Blender context and output paths. Preserve existing scenes and source assets; make destructive scene operations explicit and restrict isolated construction scripts to their intended background process.

Keep units, origins, semantic anchors, material assignments, and export collections explicit. Validate exported hierarchy, bounds, geometry, and resources, and visually inspect deliverables.

Use focused tests for executable validation logic and target coverage greater than 80% where instrumentation is available. Blender-dependent geometry and export behavior also need checks in Blender. No pytest or Python lint configuration is currently established.
