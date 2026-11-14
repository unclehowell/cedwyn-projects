# Cedwyn Project Office

Dedicated source repository for the Project Office webapp published from the projects/public directory.

## Start here

- PROJECT-OFFICE-CONTROLS.md — operating protocol, research flywheel, private threshold-watch gate, freshness/checkpoint rules and release controls.
- projects/public/index.html — Project Office home page.
- projects/public/estate/pid/ — tailored Project Initiation Documentation.
- projects/public/estate/stage-plans/ — stage baseline and exit controls.
- projects/public/data/ — derived and date-stamped public data only.
- projects/quality-gate.mjs — fast static integrity checks run on pull requests and main changes.
- projects/check.mjs — Cloudflare Pages build check and wider estate build checks.
- APP-README.md — application and rights notes.

## Source and release

The dedicated repository is the declared source for the Project Office route (unclehowell/cedwyn-projects, split-repo mode). The old unclehowell/cedwyn projects branch is a legacy mirror, not the canonical source. Do not edit that branch to change this app.

Changes should be made on a short-lived branch and opened as a pull request to main. Do not merge or deploy autonomously. A passing integrity check is not a full site build; a merge is not proof of production deployment; and a deployment is not proof that the intended public route serves the correct content. Record and verify each state separately.

## Data and privacy

Never put Gmail bodies, HubSpot task bodies, personal contact information, legal advice, private trigger-review candidates or unredacted source documents in this public repository. Publish only approved, sourced, privacy-reviewed material. A stale snapshot remains labelled with its true as-of date and must not be silently replaced with an incomparable query total.

## Legacy material

MASTERPLAN.md is retained as a historical DATRO-era file for provenance only. It is not the active design or authority for this repository.
