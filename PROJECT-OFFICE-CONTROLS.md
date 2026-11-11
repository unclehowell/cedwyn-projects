# BucklerFamily.estate — research and continuity control protocol

**Status:** Operating baseline proposed for Executive review  
**Prepared:** 11 November 2026  
**Scope:** Wales research and disclosure, historical reconstruction, public evidence catalogue, dependent digital outputs and the separate conditional case-reopening gate.

This is a control protocol. It does not state that any allegation has been established, that a legal threshold has been met, or that any authority has acted unlawfully.

## 1. Operating principle

The programme is a source-led reconstruction and disclosure project. Routine work should continue without the Executive supervising every search, ingestion or reconciliation step. Autonomy remains bounded by evidence quality, privacy, UK information-rights procedures, project scope and explicit stop gates.

**The system may discover, classify, compare, draft, test and prepare. It may not autonomously allege, report, litigate, pay, publish disputed personal material or take irreversible action.**

## 2. Main research flywheel

1. Discover records, maps, registers, catalogues, planning documents and relevant institutions across the full Llandough–Leckwith landscape.
2. Qualify the custodian, date, parcel identity, legal access route, known reference and whether the enquiry is genuinely new.
3. Prepare a focused FOIA, EIR, statutory HER-access or archive enquiry. Keep distinct request/review lanes separate.
4. Track reference, sent date, statutory or stated deadline, extension, fee, review route, owner and next action in HubSpot.
5. Preserve original replies and attachments with provenance. Never replace a source with a summary.
6. Catalogue artefacts and relationships; record what each source establishes and what remains uncertain.
7. Challenge chronology, parcel reconstruction and title propositions against contrary records and alternative explanations.
8. Update parcel histories, maps, timelines and public explanation only where evidence supports the change.
9. Release only after provenance, privacy, rights, accessibility, build, link and independent-review checks.
10. Recycle each verified answer into the next precise missing-record or custodian search.

A request is not a result. An acknowledgement is not disclosure. An institutional statement is not independent proof of the underlying historical fact. A catalogue entry is not inspection of the original record.

## 3. Nested threshold-watch flywheel — private and non-allegational

This loop monitors whether new material may become legally significant. It is subordinate to the reconstruction project and separate from public reporting.

**A — Observation:** record a dated discrepancy or potentially material omission using neutral language. Do not label it fraud, concealment, collusion or misconduct.

**B — Source test:** authenticate the record; capture provenance; distinguish original, copy, derivative, recollection, institutional assertion and inference.

**C — Identity test:** prove that the relevant person, organisation, title, parcel, boundary, date and event are the same subject. Similar names, nearby land, a shared agent or an overlapping map are not enough.

**D — Corroboration:** seek genuinely independent primary evidence where available. Log supporting and contradictory records, missing material and source limitations. Copies of one source are not independent corroboration.

**E — Alternative-explanation challenge:** test administrative error, ordinary record loss, changed terminology, legal process, mistaken identity, timing, innocent explanation and competing interpretations. An unresolved alternative keeps the candidate open.

**F — Legal relevance map:** state the exact legal test, each required limb, evidence mapped to that limb, what is missing, the relevant time/limitation rule and the proper remedy. Do not assume an irregularity proves intent or reopens a concluded case.

**G — Independent challenge:** a reviewer who did not originate the candidate tests sources, logic, parcel identity, contradictions, legal test and conclusion. “Not established” must remain an available outcome.

**H — Executive decision:** only the Executive may decide whether to seek professional legal advice or authorise an external step. An automation may prepare a private evidence pack; it may not send a report, allegation, complaint alleging fraud/concealment or legal filing.

Candidate states: observation; source-checked; identity-checked; corroboration-pending; challenged; legal-review-pending; Executive-decision. Also permit: not-supported; duplicate; wrong-parcel; alternative-explanation-supported; indeterminate.

No item advances merely because it is old, emotionally important, suspicious, repeated by multiple agents or described as “close”. The case-reopening workstream remains **STANDBY** until every legal limb is evidenced and the Executive expressly authorises it. No notification to police, regulators, courts, government or media is authorised by this protocol.

## 4. Evidence rules

Every factual proposition must carry a stable artefact ID and citation; issuer, author and date; repository and retrieval date; page, folio, plan, title or message location where available; parcel/geographic identity confidence; evidence type; corroboration and contradictions; missing records and alternative explanations; and a clear status: established by this source, supported, contested, unresolved or not supported.

Keep Parcel A/A1/A2, Parcel B, provisional C, VG41 and the wider Leckwith/Cedwyn landscape distinct unless a source proves a connection. Never convert a working theory into a legal boundary or title fact. Never alter a source's date, quotation, attribution, author or scope to improve the narrative.

## 5. UK policy and procedure framework

- **FOIA 2000:** identify whether the holder is a public authority; track the statutory clock, exemptions, advice and assistance, refusal notice, internal review and ICO route as applicable.
- **EIR 2004:** classify the information, not merely the institution or subject line; apply the relevant exceptions and public-interest test; record EIR form/format, charging and review provisions separately from FOIA.
- **Historic Environment (Wales) Act 2023:** use the statutory HER access and guidance route as well as any applicable FOIA/EIR route. Distinguish the statutory HER from a trust's wider corporate or project archive.
- **Data protection:** minimise personal data; keep private witness/family/contact material out of public indexes; check redactions before publication.
- **Records management:** use the section 46 Code of Practice, the actual holder's retention schedule and recorded disposal/transfer arrangements. A preservation request is not proof that a hold has been accepted.
- **Archive practice:** distinguish catalogue search, physical inspection, copy order, access restrictions, copyright and the actual document inspected.

Ask for the narrowest useful record and an index/reference list before inviting a broad search. Before accepting a charge, check the legal route, published schedule, unit calculation and inspection/electronic alternatives.

## 6. Single sources of truth

| System | Authority |
|---|---|
| HubSpot | Private research, request/deadline tracking, recipient-facing drafts and review tasks |
| GitHub | Canonical versioned engineering source, public-safe issues, pull requests, changelog and tests |
| Hive | Reviewer coordination, turn-taking, leases and handover; not a second task database |
| Gmail | Original correspondence and the Executive's sending channel after the review gate |
| Public websites | Approved, cited, privacy-checked outputs only |
| Automations | Scheduled controls and bounded research jobs; every run reports exact coverage and checkpoint |

Search for the canonical task/issue before creating another. Preserve prior notes and provenance. Never publish email bodies, private task bodies, contact data, legal advice, private candidate reviews or raw CRM content.

## 7. Freshness, checkpoints and failure behaviour

- Every derived file records generation time, source scope, pagination coverage and source count.
- Task inventories must confirm distinct IDs against the returned total. Partial page sets are never described as complete.
- Portfolio percentages come from stage acceptance evidence, not task counts. The 30 October HubSpot snapshot remains historical until a like-for-like query is reconciled.
- A status panel older than its declared freshness window says STALE or UNVERIFIED; it must not display stale values as current.
- Each automation run writes a checkpoint before moving to the next workstream: last successful cursor/page, source timestamp, completed sections, failed connector and next action.
- Break large sweeps into bounded resumable slices. Do not repeat a full scan after failure without first recording recovery state.
- Retry a transient failure once. If an integration fails again or two scheduled runs fail consecutively, enter safe mode: preserve the last known-good release, freeze dependent publication and outbound preparation, record the error and raise it for Executive attention.
- NO_UPDATE is valid only where inputs were verified and no change was found. It is not interchangeable with failure or incomplete coverage.

## 8. Change control and release

1. Reuse existing issues and inspect the current source branch.
2. Create a short-lived branch from the canonical split repository.
3. Make a small, reversible change and retain the before-state.
4. Run static integrity tests and the full site build where practical.
5. Open a pull request with files changed, test evidence, risk and rollback.
6. Obtain review. Do not merge or deploy autonomously.
7. After an authorised merge, check the Pages build, deployment ID, production route, HTTP response and rendered content separately.
8. Update the versioned change record only after verification.

A green source check is not proof of deployment. A successful deployment is not proof that the intended route is serving the correct page.

## 9. Human attention budget

Interrupt the Executive only for a decision outside the mandate; a material evidence conflict; an actual statutory deadline/refusal/fee decision requiring owner action; repeated integration failure or privacy/security incident; or a proposed irreversible, paid, legal or outward action.

Routine catalogue searching, response ingestion, deduplication, evidence tagging, source comparison, private drafting and test generation should continue within these limits without repeated prompts.

## 10. Public reporting

Publish the current mandate, date/scope of snapshots, verified progress, genuine blockers and control rules. Do not publish private candidate reviews, unsupported allegations, personal contact information, internal legal analysis, confidential task text or raw CRM data. When evidence is stale or unresolved, say so.

**Current stop state (11 November 2026):** case-reopening remains on standby. No trigger event is accepted as established, no fraud/concealment finding is made and no external allegation/report is authorised.
