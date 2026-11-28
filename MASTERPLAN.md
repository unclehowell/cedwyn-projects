# Great House Farm / Tŷ Mawr — Project Master Plan

**Programme:** Great House Farm (Tŷ Mawr), Llandough-juxta-Penarth and the Williams–Buckler family history  
**Control surface:** Project Office at `/projects/`  
**Status:** Active research and digital reconstruction programme  
**Version:** 1.0.0 · 28 November 2026

## 1. Mission

Build and maintain a source-led, chronologically accurate reconstruction of Great House Farm / Tŷ Mawr, its land, title and occupation history, and the Williams–Buckler family history. The programme brings archival research, public-record disclosure, evidence examination, mapping, correspondence and public-history outputs into one traceable process.

BucklerFamily.Estate is the public research and publication surface. It is not itself proof of a proposition: every material statement must lead back to an identifiable source, a neutral catalogue record or a clearly labelled interpretation.

## 2. Scope

Included:
- Great House Farm / Tŷ Mawr and Llandough-juxta-Penarth, with carefully disambiguated related places including Leckwith, Cogan and Penarth.
- Historical title, manorial, estate, land-use, family, planning, court, registry and public-administration records that bear on the defined research questions.
- Archives, public authorities, registries, libraries, museums, heritage bodies, broadcasters and other relevant record custodians.
- The evidence catalogue, chronology, parcel and place-name models, correspondence and disclosure history, maps, documentary, books and educational webapps.

Excluded:
- The separate DATRO security/technology project, its repositories, systems and all `*-datro` subdomains. They are not Project Office work, dependencies, deployment targets or migration targets.
- Unrelated commercial, financial, security or product-development work.
- Any claim that a disputed title, legal interpretation or historical hypothesis has already been established by a court or public authority when it has not.

## 3. Research principles

1. **Primary source first.** Preserve the original document, page, image or message and its provenance before writing a catalogue description or interpretation.
2. **Separate evidence from interpretation.** Keep the neutral description and transcript distinct from a versioned “our reading”.
3. **Show contrary material.** Record both supporting and contrary evidence. Do not hide an adverse record because it complicates a theory.
4. **Classify confidence accurately.** Use VERIFIED, REPORTED BY ANOTHER AGENT, INFERENCE and UNRESOLVED. Record who verified a point and against which source.
5. **Keep entities distinct.** Do not merge people, places, parcels, legal entities, dates or proceedings because labels look similar.
6. **Preserve history.** A correction creates a new version and a link to the prior one; it does not silently overwrite the earlier view.
7. **No legal overstatement.** Distinguish an institutional statement, an independent verification and an inference. Do not infer fraud, concealment, bad faith or deliberate destruction from a missing record, delay or inconsistent search result.

### Parcel discipline

The working parcel model must remain explicit in every affected catalogue entry, map, chronology and correspondence review:
- **A2:** Mary’s farmhouse and garden.
- **A1:** northern woodland associated with the wider A claim.
- **B:** eastern fields and their separate arrangements.
- **C:** provisional southern green.

Do not collapse these into one undifferentiated “farm” holding. In particular, the 1939 agreement/map DBDT123/7 is treated as Parcel B material, not evidence of a tenancy over A2. The 1955 possession-order description must not be extended to A2 without primary support. These are working research controls, not a judicial determination.

## 4. Systems of record

| System | Authoritative role |
|---|---|
| `unclehowell/bucklerfamily-estate` | Current central platform/build source and canonical catalogue source. `main` is the maintained source; `site` is generated publication output. Do not treat old `cedwyn` branches as current authority. |
| Dedicated `cedwyn-*` app repositories | Authoritative source for their respective webapps. The central build reads split-repository apps from their designated repositories. |
| Central evidence catalogue | Canonical record identity, neutral descriptions, source provenance, transcripts, links and versioned interpretations. Site and app indexes are derived read models. |
| HubSpot | Private authoritative task register, work ownership, due dates, recipient profiles, correspondence review and decision history. Do not create parallel task lists. |
| Gmail | Original correspondence, sent messages, received replies and attachments. A draft is not sent; an email logged to a CRM timeline is not automatically a task. |
| Hive | Agent roster, coordination, claims, handovers and review protocol. It is not a second task database. |
| Project Office | Portfolio, workstreams, milestones, dependencies, risks, acceptance criteria and public-safe progress summaries. |
| Cloudflare | Hosting, routing, runtime and durable automation. Existing production data stores must be preserved until a verified migration and rollback exist. |

The Project Office reads HubSpot task metadata and the catalogue’s public-safe data. It does not become the authority for private task bodies, source correspondence or evidence.

## 5. Programme workstreams

### A. Repository and platform retirement
- Complete the controlled migration away from `unclehowell/cedwyn`.
- Move every active Worker source, workflow, fallback and scheduled job to a maintained successor location.
- Inventory every Pages project, route, Worker, binding, D1 database, KV namespace, Durable Object, R2 bucket, webhook and consumer.
- Export and compare persistent state before any data migration.
- Retain production routing and rollback until all acceptance tests pass.
- Keep DATRO and every `*-datro` hostname outside the workstream and unchanged.

### B. Evidence and catalogue
- Preserve each source in its original form; calculate a content hash and record capture details.
- Extract pages, text, dates, actors, references, maps and document relationships.
- Build neutral catalogue records first; add versioned interpretations only as a separate layer.
- Link records to people, institutions, places, parcels, legal proceedings and chronology events.
- Detect duplicates and conflicting metadata without deleting the original source.
- Maintain a visible queue of uncatalogued sources and unresolved extraction errors.

### C. Disclosure and records access
- Identify a specific documentary gap before creating a request.
- Resolve the correct legal custodian and the correct route for each information category: FOIA, EIR, SAR, court access, archive/library access, ordinary enquiry, complaint or preservation enquiry.
- Check statutory coverage, published policy, existing correspondence, prior requests, deadlines, transfer history, fees and review routes.
- Do not duplicate a question already answered, withdrawn or active under another reference.
- Keep the current operating limit of **no more than two new statutory disclosure requests per day**.
- Maintain a **zero-spend** rule: no paid copies, appointments, bookings, reproduction orders or fees without a separate owner decision. If a fee or paid service is proposed, hold the item.
- Record each requested item’s outcome precisely: disclosed, partly disclosed, withheld, not held, not located, never created, transferred, destroyed/disposed of, outside scope, fee/clarification, publicly available, acknowledgement only or overdue.

Recipient-facing material must follow the current Hive JOIN contract and `THREE-HAT-FOI-GUARDRAILS.md`: full thread continuity, exact-version review, three analytical hats, fourth-excuse sweep, CSSCPSG and the actual active-seat review requirement. No immediate-send path is permitted. Where the authorised scheduling capability or review evidence cannot be verified, retain the canonical draft privately and mark it blocked; do not claim it was sent.

### D. Chronology, title and historical reconstruction
- Reconcile dates, references, persons, entities, legal events and parcel identities against primary sources.
- Distinguish application dates, registration dates, execution dates, decision dates and publication dates.
- Preserve the A1/A2/B/C parcel distinction and the evidence supporting each boundary or relationship.
- Maintain a hypothesis register with what would support, weaken or falsify each proposition.
- Record uncertainty and contrary evidence in the public-facing account where material.

### E. Public outputs
- Regenerate affected catalogue pages, chronology views, map layers, app feeds, documentary material and book editions from the same controlled records.
- Never expose private HubSpot content, private correspondence, personal data, secret tokens, draft legal strategy or unreviewed submissions.
- Publish only approved public-safe records and versioned interpretations.
- Retain prior release versions and a changelog so visitors can see what changed and why.

### F. Operations and quality
- Track milestones, blockers, owners, deadlines, work age, dependencies and evidence of completion.
- Detect broken routes, stale app data, failed scheduled jobs, missing source links and build regressions.
- Require mobile-width checks, link checks, accessibility checks, source references and smoke tests before publication.
- Roll back a failed deployment to the last known-good artifact rather than publishing a partially built site.

## 6. Autonomous operating loop — target architecture

The intended loop is event-driven and resumable:

1. **Capture:** receive an authenticated email, a disclosure attachment, an archive item, a source discovery, a repository event or a monitoring alert.
2. **Preserve:** keep the original in its system of record; record its source ID, received/capture time, content hash and privacy classification.
3. **Classify:** match the event to an existing person, institution, request, catalogue record, parcel, chronology event and Project Office workstream. Quarantine uncertain matches.
4. **Claim:** acquire a single expiring job lease so two agents cannot perform the same write or external action.
5. **Examine:** use specialist agents for extraction, source verification, duplicate checks, counter-evidence, recipient/regime analysis and editorial review.
6. **Record:** append the event and provenance; create or update the authoritative HubSpot task where work is required; update the catalogue through its controlled write path.
7. **Rebuild:** regenerate only the affected derived indexes and app views; run their tests.
8. **Publish:** deploy only public-safe, tested output. Keep the prior release available for rollback.
9. **Learn:** create the next precise research question from the remaining evidence gap, not from speculation.

Cloudflare Workflows, Queues and Durable Objects are proposed runtime components. They are **not yet represented as a live estate-wide orchestration service**. The existing D1/KV/R2/DO resources are not interchangeable and must not be repurposed without a data and rollback plan. A scheduled health check is not an AI agent run; each real agent seat requires its own verified runner and schedule.

### Event record minimum

Every event should carry: stable event ID; event type; source system and source ID; original URL or mailbox/thread reference; occurred-at and ingested-at timestamps; actor; related entity/record/task/request IDs; content hash; privacy class; provenance; processing state; idempotency key; and links to superseding or correcting events. Original evidence is immutable; indexes and summaries are rebuildable.

## 7. Agent roles and work boundaries

| Role | Permitted autonomous work |
|---|---|
| Intake and triage | Match authenticated incoming items, detect duplicates, route to the correct workstream and quarantine uncertainty. |
| Archivist | Preserve and extract public or authorised source material; produce transcripts with page-level provenance. |
| Researcher | Search for identifiable records, log positive and negative results, and propose source-linked research tasks. |
| Evidence examiner | Test claims, chronology, parcel identity and contrary material; never promote an inference to a verified fact. |
| Disclosure officer | Check recipient, regime, scope, prior correspondence, deadlines and no-fee limits; prepare and track requests within the approved policy. |
| Project controller | Update HubSpot tasks, dependencies, milestones, blockers and completion evidence. |
| Publisher/developer | Update app source, run tests, build preview and publish public-safe derived output under change control. |

No role may invent a reviewer identity, impersonate the owner, use another seat’s credentials, bypass Hive's exact-version gates, expose private information or spend money.

## 8. Delivery milestones

| Milestone | Completion evidence |
|---|---|
| P0 — Retirement control | Successor source and live dependency inventory; no unowned Worker/cron/fallback; data exports and rollback evidence; production smoke tests; updated migration-control register. |
| P1 — Private intake | Authenticated inbound route; MIME and sender validation; idempotent receipt; private retry/dead-letter handling; successful HubSpot read-back. |
| P2 — Evidence ledger | Append-only event schema; immutable source storage; provenance and hash validation; correction/supersession history; replay and duplicate tests. |
| P3 — Research and disclosure | Recipient profiles; regime classification; daily request limit; no-fee gate; exact-version review and deadline tracking; reply/attachment matching. |
| P4 — Project execution | HubSpot-backed tasks and milestone updates; job leases; clear owners and measurable acceptance criteria; stale-work detection. |
| P5 — Continuous publication | A catalogue change updates the correct affected apps; private data is excluded; CI, preview, accessibility, source-link and rollback tests pass. |
| P6 — Autonomous operation | Each active agent seat has a verified runner and schedule; workflows resume from incoming events; exception dashboard reports only work requiring an owner decision. |

Milestones may be marked complete only with a surviving commit, workflow run, resource ID, successful read-back, live URL or equivalent external proof. A plan, PR or accepted HTTP request is not proof of production operation.

## 9. Success measures

- Every published material claim has a source and an evidence classification.
- No original source is silently overwritten or detached from its provenance.
- No duplicate active task or disclosure request for the same unresolved item.
- No more than two new statutory disclosure requests per day.
- No spend or paid service without a separate owner decision.
- No private correspondence or personal data in public indexes, build artifacts or repository logs.
- Every app update is traceable to a source event and commit.
- Every production release has passing tests and a rollback target.
- The owner sees exceptions, material discoveries and decisions—not routine copying, indexing or status chasing.

## 10. Current operating rule

This is the Great House Farm Project Office, not a general-purpose software release machine. It plans and measures the research programme. The evidence catalogue remains the factual foundation; HubSpot remains the private task register; Gmail remains the source mailbox; Hive remains the agent coordination and review system. New automation must connect these existing records rather than creating competing ones.

The programme is prospective research and public-interest reconstruction. It is not legal advice and does not represent a finding of any court.
