# Cooper project workflow

## Context and isolation

Read [the context index](../index.md), relevant living capability specs, and applicable style guides before planning work. Use the local Cooper skills under `.agents/skills/`.

Run `git troop` to inspect existing work. Start each task with `git agent-start <track_id>` and work inside `.worktrees/<track_id>`. Base branches on origin/main, or local main when the remote is unavailable. Verify the base when working offline. Do not modify feature code in the main workspace.

Workflow changes require a separate branch and pull request before returning to other active tracks. Use a dedicated RFC for major architectural initiatives; use ordinary tracks for focused changes.

## Plan and specification

Create a proposal, design, metadata, plan, and capability Spec Deltas under `.cooper/active/<track_id>/` before executable changes. Record added requirements with a plus prefix and removed requirements with a minus prefix, using GIVEN/WHEN/THEN scenarios.

Register the track in `.cooper/tracks.md`. Keep the plan current with pending, in-progress, and completed tasks and actual commit references. Update the stack definition before implementing an approved stack change.

Definitions and living specifications must stand alone. Do not embed ticket, issue, PR, track, decision, or open-question identifiers, or positional section references. Refer to exact heading names. Outside requirements and scenario steps, rationale may link frozen archives, approved or archived RFCs, or frozen contracts; open known gaps may cite their tracking tickets until resolved.

## TDD and quality

For executable changes, write a focused failing test, confirm the expected failure, implement the minimum passing behavior, then refactor and rerun relevant checks. Maintain coverage greater than 80%; report measured coverage and any tooling gap honestly.

Run `CI=true npm test` and `npm run build` for application changes. Run relevant Playwright scenarios when input, choreography, accessibility, or presentation changes. Asset work also requires geometry/export checks and visual inspection in the relevant environment.

Documentation-only changes require link, content, and diff verification. Do not invent application test or coverage results for documentation changes.

## Commits and task evidence

Use conventional commit messages. Attach task summaries with `git notes add -m "<actual task summary>" <commit>`. Record changed files, rationale, commands run, observed outcomes, and unresolved gaps. Never prefill successful results or user approvals.

## Phase verification

At phase completion:

1. Run `git fetch origin main` and inspect upstream workflow and living spec changes; integrate relevant updates before continuing.
2. Run appropriate automated checks and resolve failures.
3. For functional phases, present exact manual verification steps and expected outcomes through an interactive question tool and await the user's actual response.
4. Commit the checkpoint and attach an accurate verification note. Record its hash in the plan.
5. Push the branch with `git push origin <track_id>` and publish notes using the procedure below.

## Git Notes synchronization

Branch pushes do not publish notes. Before publishing local notes, check whether the remote notes ref exists:

```sh
git ls-remote --exit-code origin refs/notes/commits
```

An exit status of two means the ref is absent. For other failures, resolve the connection or authorization error rather than treating it as an absent ref.

If the remote ref exists, fetch it to a separate local ref and merge it:

```sh
git fetch origin +refs/notes/commits:refs/notes/cooper-remote
git notes --ref=commits merge refs/notes/cooper-remote
```

Resolve any notes conflicts before publishing. Then push without force:

```sh
git push origin refs/notes/commits
```

If another contributor updates remote notes first, fetch and merge again before retrying. Do not overwrite their notes.

## Review, merge, and cleanup

Review against the Spec Deltas, style guides, test evidence, and coverage target. Submit a pull request with the concrete behavior change, specification mapping, verification results, and remaining limitations.

Integrate approved Spec Deltas into living specs and archive the completed track as part of finalization so merged requirements stay current. After PR approval and merge, run `git agent-stop <track_id>`. Keep unmerged worktrees available for review.

Use interactive question tools for choices and required confirmations. Use dedicated file tools for writing and edits; do not create or modify files through shell pipes, stream editors, heredocs, or redirection.
