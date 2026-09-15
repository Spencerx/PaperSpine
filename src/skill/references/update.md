# PaperSpine5 Suite Update Routing

This playbook separates PaperSpine5 suite lifecycle authority from the legacy
PaperSpine 4 component updater. Update requests never start intake, research,
or writing, and normal paper runs never perform an implicit update preflight.

## Stable upgrade from V1--V4 to the current release

Natural-language requests such as “更新到最新版”, “从 V3 更新到 V5” and
“修复并升级 PaperSpine” route to the stable `paperspine-updater/1` bootstrap
shipped in the candidate at `release/stable_updater.py` (Windows shortcut:
`release/stable-update.cmd`). It detects the existing canonical `paper-spine`
Skill, recognizes both the current managed pointer and older V1--V4
standalone layouts, and never executes the old updater. The direct bundle or
official HTTPS channel is checked before any candidate code runs; a direct ZIP
must be accompanied by its SHA-256.

The bootstrap stages and probes the new release, snapshots the old Skill,
switches the one discovery directory, and records a hash-bound receipt. Only
after the real launcher probe passes is the old active code removed from the
discovery directory. The old tree remains in the updater transaction archive
for rollback and recovery. Explicit `--data-root` values and the existing
PaperSpine task/data directories are retained byte-for-byte; no data directory
is deleted or silently used as a working directory. If the update is
interrupted, `recover` restores the pre-update Skill only when its hash still
matches the snapshot; unexpected user changes are preserved and reported.

The stable protocol deliberately separates binary replacement from task-state
migration. Each new suite supplies its own protocol adapter. V5 can preserve
V1--V4 files and register them for migration, while a future V6+ adapter reads
the same envelope and migrates directly from the canonical preserved data (it
does not require installing V4 or V5 in sequence). `task_schema_migrated` is
reported truthfully; an update receipt is not evidence that a paper task has
been scientifically resumed.

Use the read-only preflight first:

```text
python <candidate>/release/stable_updater.py detect \
  --skill-root <canonical-paper-spine-root>
```

Then pass the exact official channel or bundle and confirm the mutation:

```text
python <candidate>/release/stable_updater.py apply \
  --source <official-channel-or-exact.zip> \
  --sha256 <64-lowercase-hex-for-a-direct-zip> \
  --skill-root <canonical-paper-spine-root> \
  --control-root <stable-control-root> \
  --data-root <existing-paper-data-root> --yes
```

The bootstrap is the only long-lived update entrypoint. Versioned adapters
may change their internal bundle layout, but they must continue to implement
the stable request/response envelope and pass the same prepare/probe and
rollback tests.

## Suite authority

The update object is the exact PaperSpine5 suite identified by
`suite-manifest.json`: product ID, product version, channel, build ID, component
versions, state writers/readers, API compatibility, and content hashes. A
component version such as PaperSpine 4.0 is not the suite version.

For the current deterministic candidate, suite doctor and lifecycle operations
are exposed only by the exact bundle's `release/release_cli.py`. They require an
explicit profile root; install/update also require an exact verified bundle.
Never discover, guess, or default to a real user profile.

Read-only inspection:

```text
python <exact-suite>/release/release_cli.py doctor \
  --profile-root <explicit-profile-root> \
  [--bundle <exact-candidate-bundle.zip>]
```

Explicit update after a PASS preflight and user confirmation:

```text
python <exact-suite>/release/release_cli.py update \
  --profile-root <explicit-profile-root> \
  --bundle <exact-candidate-bundle.zip> \
  --operation-id <unique-id> \
  --confirm
python <exact-suite>/release/release_cli.py reload \
  --profile-root <explicit-profile-root> \
  --operation-id <unique-reload-id>
```

The lifecycle must verify compatibility and content before mutation, take a
pre-snapshot, activate one suite discovery object, emit a reload marker, and
return a typed receipt. A failed mutation must restore the snapshot or report
rollback failure/residue explicitly. Installation never authorizes external
submission or closes manuscript readiness.

If the selected host does not expose this exact suite lifecycle, stop and state
that suite update authority is unavailable on that surface. Do not substitute
another cached Skill, a public RC, an arbitrary marketplace entry, or the
component updater.

## Legacy PaperSpine 4 component updater

`src/scripts/paperspine_update.py` and installed copies at paths such as
`paper-spine\scripts\paperspine_update.py` or
`paper-spine/scripts/paperspine_update.py` remain testable compatibility tools
for an explicitly requested, manual PaperSpine 4 component maintenance task.
They are not invoked by a normal launch or resume, cannot update the
PaperSpine5 plugin/Product Kernel/Web runtime/suite manifest, and must never be
reported as a PaperSpine5 suite update.

Only when the user explicitly requests maintenance of that legacy component,
use its manual/offline validation modes. Do not use `--auto`, enable its legacy
automatic-update policy, or treat its host copies as the active suite object.
Preserve project artifacts and report the operation as component-only.

## Standalone Skill managed-suite residue

The standalone updater may recognize an exact pointer-bound managed suite with
source-bound CPython `__pycache__/*.pyc` as a safe predecessor. A read-only
`skill-update-check` reports the residue count, bytes, and path digest; orphan,
foreign, tampered, unknown, indexed-drift, or reparse content blocks without
mutation. Confirmed upgrade archives the exact residue under the Skill update
control root before candidate placement. Later failure and explicit rollback
restore both the predecessor projection and the archived bytes from hash-bound
typed receipts. This installed-prestate compatibility never permits residue in
a new candidate or relaxes `verify-bundle`.

## Permission and claims

- A check is read-only; an update requires explicit confirmation and the exact
  bundle/profile object.
- Do not touch a user marketplace, personal Skill directory, or public plugin
  entry from this component playbook unless the user explicitly authorizes that
  separate host operation.
- Do not claim W7/C7 release closure from simulated-profile evidence. A real
  host install/reload/uninstall must be verified separately against the same
  build and receipt contracts.
- `external_action_authorized` remains false throughout lifecycle operations.
