#!/usr/bin/env python3
"""Deterministic PRINCE2 baseline builder for PRG-2027-FOI (issue #29).

Reads   projects/public/2027-foi-programme/programme.json
Writes  the same file (schema 1.1.0) and patches index.html in place.

Idempotent: re-running on its own output gives the same result. Every date,
priority, product link, predecessor and % complete is derived here from the
tier table and the milestone windows below, so another agent can change one
rule and rebuild rather than hand-edit 1,408 tasks.

Run from the repo root:  python3 tools/build_2027_plan.py
"""
import datetime as dt
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIR = ROOT / "projects/public/2027-foi-programme"
JP, HP = DIR / "programme.json", DIR / "index.html"
BUILT = "2026-11-26"

# ---------------------------------------------------------------- calendar
BANK_HOLIDAYS = {  # England and Wales
    "2026-12-25", "2026-12-28",
    "2027-01-01", "2027-03-26", "2027-03-29", "2027-05-03", "2027-05-31",
    "2027-08-30", "2027-12-27", "2027-12-28",
}
D = dt.date.fromisoformat


def wd(x):
    return x.weekday() < 5 and x.isoformat() not in BANK_HOLIDAYS


def roll(x):
    while not wd(x):
        x += dt.timedelta(days=1)
    return x


def add_wd(x, n):
    x = roll(x)
    while n > 0:
        x += dt.timedelta(days=1)
        if wd(x):
            n -= 1
    return x


def wd_between(a, b):
    n, x = 0, a
    while x <= b:
        n += wd(x)
        x += dt.timedelta(days=1)
    return n


def split(a, b, parts):
    """Split [a,b] into `parts` consecutive working-day windows."""
    tot = wd_between(a, b)
    out, s = [], roll(a)
    for i in range(parts):
        size = round(tot * (i + 1) / parts) - round(tot * i / parts)
        e = add_wd(s, max(size - 1, 0))
        if i == parts - 1:
            e = b
        out.append((s, e))
        s = add_wd(e, 1)
    return out


# ---------------------------------------------------------------- tiers
TIERS = {
    1: dict(name="Tier 1 · Primary record holders", wave="Wave 1", priority="High",
            mode="planned",
            why="Hold or are most likely to hold the primary title, estate, court, registration or survey records for Parcel A and Parcel B. Run first.",
            lanes=["sp27-01", "sp27-03", "sp27-05", "sp27-08", "sp27-09", "sp27-10", "sp27-11",
                   "sp27-16", "sp27-17", "sp27-24", "sp27-26", "sp27-31", "sp27-44", "sp27-47",
                   "sp27-88"],
            M={"M0": ("2027-01-04", "2027-01-22"), "M1": ("2027-01-25", "2027-02-26"),
               "M2": ("2027-03-01", "2027-06-30"), "M3": ("2027-07-01", "2027-10-29")}),
    2: dict(name="Tier 2 · Secondary and successor holders", wave="Wave 2", priority="Medium",
            mode="planned",
            why="Successor firms, utilities, specialist archives and public bodies that may hold copies, plans, imagery or files. Run once Wave 1 requests are out.",
            lanes=["sp27-02", "sp27-04", "sp27-12", "sp27-13", "sp27-14", "sp27-15", "sp27-19",
                   "sp27-22", "sp27-23", "sp27-28", "sp27-30", "sp27-32", "sp27-36", "sp27-40",
                   "sp27-42", "sp27-48", "sp27-50", "sp27-51", "sp27-52", "sp27-53", "sp27-57",
                   "sp27-58", "sp27-59", "sp27-60", "sp27-61", "sp27-63", "sp27-64", "sp27-70",
                   "sp27-71", "sp27-73", "sp27-74", "sp27-75", "sp27-79", "sp27-85", "sp27-87"],
            M={"M0": ("2027-02-01", "2027-02-26"), "M1": ("2027-03-01", "2027-04-30"),
               "M2": ("2027-05-04", "2027-08-31"), "M3": ("2027-09-01", "2027-11-26")}),
    3: dict(name="Tier 3 · Review, oversight and representation routes", wave="On trigger",
            priority="Trigger", mode="trigger",
            why="Regulators, ombudsmen, reviewers and elected representatives. M0 reconciles live 2026 cases in January; M1–M3 open only when a Tier 1 or Tier 2 lane raises a documented exception that needs this route.",
            lanes=["sp27-06", "sp27-07", "sp27-18", "sp27-20", "sp27-21", "sp27-29", "sp27-33",
                   "sp27-34", "sp27-35", "sp27-37", "sp27-38", "sp27-39", "sp27-45", "sp27-49",
                   "sp27-83"],
            M={"M0": ("2027-01-04", "2027-01-29"), "M1": ("2027-03-01", "2027-11-26"),
               "M2": ("2027-03-01", "2027-11-26"), "M3": ("2027-03-01", "2027-11-26")}),
    4: dict(name="Tier 4 · Relevance check first", wave="Relevance gate", priority="Conditional",
            mode="conditional",
            why="Bodies with no record yet linking them to the estate. M0 is a desk relevance check ending at the 31 March relevance gate: each lane is either promoted into Wave 2 dates or closed CANCELLED_WITH_REASON.",
            lanes=["sp27-25", "sp27-27", "sp27-41", "sp27-43", "sp27-46", "sp27-54", "sp27-55",
                   "sp27-56", "sp27-62", "sp27-65", "sp27-66", "sp27-67", "sp27-68", "sp27-69",
                   "sp27-72", "sp27-76", "sp27-77", "sp27-78", "sp27-80", "sp27-81", "sp27-82",
                   "sp27-84", "sp27-86"],
            M={"M0": ("2027-02-01", "2027-03-31"), "M1": ("2027-05-04", "2027-06-30"),
               "M2": ("2027-07-01", "2027-09-30"), "M3": ("2027-10-01", "2027-11-26")}),
}
TIER_OF = {lid.lower(): t for t, v in TIERS.items() for lid in v["lanes"]}

GATES = [
    dict(id="G0", name="Initiation approval (authorise the 2027 programme)", date="2027-01-04",
         stage_closing="P0", decision="Approve PID, business case, tolerances, tiers and Stage 1 plan; authorise Wave 1 work packages."),
    dict(id="RG", name="Tier 4 relevance gate", date="2027-03-31", stage_closing=None,
         decision="Promote each Tier 4 lane to Wave 2 dates or close it with a recorded reason."),
    dict(id="G1", name="End of Stage 1 — mapping and design", date="2027-03-31", stage_closing="P1",
         decision="Proceed / amend / pause / stop; authorise Wave 2 work packages."),
    dict(id="G2", name="End of Stage 2 — disclosure and recovery", date="2027-06-30", stage_closing="P2",
         decision="Proceed / amend / pause / stop; approve review routes for exceptions raised."),
    dict(id="G3", name="End of Stage 3 — review routes", date="2027-09-30", stage_closing="P3",
         decision="Proceed / amend / pause / stop; confirm closure scope."),
    dict(id="G4", name="Programme closure", date="2027-12-17", stage_closing="P4",
         decision="Accept year-end report, title-chain products and lessons; decide 2028 options."),
]
STAGE_DATES = {"P0": ("2026-11-25", "2026-12-31"), "P1": ("2027-01-04", "2027-03-31"),
               "P2": ("2027-04-01", "2027-06-30"), "P3": ("2027-07-01", "2027-09-30"),
               "P4": ("2027-10-01", "2027-12-17")}
STAGE_EXIT = {
    "P1": "Tier 1: records and custody maps, question matrices and QA-approved request packs accepted; first Wave 1 submissions made from 1 March (one lane per working day). Tier 2: lane baselines (M0) accepted. Tier 3: live 2026 cases reconciled. Tier 4: every lane promoted or closed at the relevance gate.",
    "P2": "Tier 1: every planned request submitted and clock-tracked; every reply and attachment analysed and catalogued within one working day. Tier 2: request packs accepted and submissions under way from 4 May. Parcel A and Parcel B title-chain products updated from new evidence.",
    "P3": "Every Tier 1 refusal, delay or search gap has a recorded remedy decision by the Executive; Tier 3 routes opened only on those decisions. Tier 2 responses analysed.",
    "P4": "Every lane closed with an evidenced disposition; every question in the master register answered or given a final disposition; title-chain products for Parcel A and Parcel B accepted; year-end report, lessons and 2028 options approved at G4.",
}

WP_PRODUCT = {"WP01": "PD27-04", "WP02": "PD27-04", "WP03": "PD27-05", "WP04": "PD27-06",
              "WP05": "PD27-07", "WP06": "PD27-08", "WP07": "PD27-09", "WP08": "PD27-10"}

PRODUCTS = [
    # management products
    dict(id="PD27-01", type="management", name="Programme Initiation Documentation (PID 2027)",
         purpose="Single approved baseline: business case, organisation, tolerances, tiers, schedule, controls.",
         composition="This page and programme.json schema 1.1.0, approved at G0.",
         quality_criteria="Every section traceable to a source dataset; tolerances quantified; every lane has a tier and dated milestones.",
         quality_method="Independent QA review; Executive approval at G0.", approver="Executive"),
    dict(id="PD27-02", type="management", name="Highlight reports and stage-end reports",
         purpose="Show progress against the baseline and forecast tolerance breaches before they happen.",
         composition="Monthly highlight report; end-stage report at G1–G3; end-programme report at G4.",
         quality_criteria="% complete computed by the progress rules, not estimated; every exception has an Exception Report.",
         quality_method="Generated from programme.json; QA agent checks against Dartboard.", approver="Executive"),
    # specialist products
    dict(id="PD27-03", type="specialist", name="Master question register",
         purpose="Every open question about the estate, numbered, with the record that would answer it.",
         composition="Q&A case questions, 2026 gaps and missing-question sweep (GWP-02, GWP-04).",
         quality_criteria="Each question states the parcel (A or B), the record sought, the likely holder(s) and a testable answer format.",
         quality_method="QA agent review; Executive approval at G0.", approver="Executive"),
    dict(id="PD27-04", type="specialist", name="Lane baseline and preservation record",
         purpose="Reconciled 2026 history for one lane before anything new is sent.",
         composition="Threads, references, clocks, attachments, drafts, preservation status (WP01–WP02).",
         quality_criteria="Every 2026 thread mapped to a reference; no overlapping denominators combined; live clocks handed over.",
         quality_method="Independent QA against Gmail and Dartboard.", approver="Project Manager"),
    dict(id="PD27-05", type="specialist", name="Records and custody map",
         purpose="Where each relevant record series sits, who created it and where else a copy may be.",
         composition="Record-series matrix: creator, description, dates, holder, transfer route, retention status, alternative holder (WP03).",
         quality_criteria="Every series sourced to a catalogue, retention schedule or reply; homonym check (Llandough-juxta-Cowbridge out of scope) recorded.",
         quality_method="QA agent spot-checks every catalogue reference.", approver="Project Manager"),
    dict(id="PD27-06", type="specialist", name="QA-approved request pack",
         purpose="A request the Executive can send unchanged.",
         composition="Draft, regime (FOIA/EIR/SAR/archive enquiry/voluntary), numbered questions, parcel identification, homonym warning, due-date calculation, HubSpot draft task (WP04).",
         quality_criteria="No duplicate of a live request; one subject per request; regime correct; standing public-wording rules met.",
         quality_method="Independent QA; Executive sends.", approver="Executive"),
    dict(id="PD27-07", type="specialist", name="Request and clock register entry",
         purpose="Track each sent request to its statutory or stated date.",
         composition="Reference, sent date, due date, reminders at 5/2/0 working days, first-overdue chase (WP05).",
         quality_criteria="Due date calculated and checked; chase raised on first overdue working day.",
         quality_method="Daily control audit (issue #21).", approver="Project Manager"),
    dict(id="PD27-08", type="specialist", name="Response analysis and evidence catalogue entries",
         purpose="Turn each reply into catalogued evidence and answered or unanswered questions.",
         composition="Per-question disposition; attachments ingested with stable evidence IDs; contradictions recorded (WP06).",
         quality_criteria="Ingested within one working day; every numbered question dispositioned; every attachment read.",
         quality_method="Independent QA against the reply and the catalogue.", approver="Project Manager"),
    dict(id="PD27-09", type="specialist", name="Remedy decision record",
         purpose="For each refusal, delay or search gap, the Executive's decision on the next route.",
         composition="Facts, route options (internal review, regulator, alternative holder, none), deadline, decision (WP07).",
         quality_criteria="Route and time limit verified against the body's own published process.",
         quality_method="QA review; Executive decides.", approver="Executive"),
    dict(id="PD27-10", type="specialist", name="Lane closure record",
         purpose="Close a lane with an evidenced disposition and a lesson.",
         composition="Questions answered / not held / refused / open-with-reason; preservation status; lesson (WP08).",
         quality_criteria="No lane closed on administrative closure alone.",
         quality_method="Independent QA.", approver="Project Manager"),
    dict(id="PD27-11", type="specialist", name="Title-chain reconstruction — Parcel A (house parcel)",
         purpose="Every link in the freehold and occupation chain for Parcel A, each tied to a primary source or a holder's recorded 'not held'.",
         composition="Chain table from the 1877 agreement through 1905/1924, 1928, 1938, 1955/1962, 1974, 1982–83 registration and 1987, with evidence IDs.",
         quality_criteria="Parcel A only — never merged with Parcel B; every link sourced or marked evidence pending with the record sought.",
         quality_method="Independent QA; updated at each gate.", approver="Executive"),
    dict(id="PD27-12", type="specialist", name="Title-chain reconstruction — Parcel B (eastern fields, woodland and green)",
         purpose="As PD27-11, for Parcel B.",
         composition="Chain table including 1916 tenancy, 1938 conveyance, May 1939 agreement, 1955 order, 1961 and 1970 registrations, 1969 conveyance.",
         quality_criteria="Parcel B only; acreage figures reconciled against each instrument.",
         quality_method="Independent QA; updated at each gate.", approver="Executive"),
    dict(id="PD27-13", type="specialist", name="Year-end report and 2028 options",
         purpose="What 2027 found, what is still pending and the options for 2028.",
         composition="Benefits measured against baseline; question register dispositions; title-chain status; lessons.",
         quality_criteria="Every statement sourced; benefits measured, not asserted.",
         quality_method="Independent QA; Executive acceptance at G4.", approver="Executive"),
]

BUSINESS_CASE = dict(
    reasons=[
        "The 2026 campaign reached 39 institutions with 138 statutory requests and 200 substantive replies (tracker, 24 Nov 2026), but 9 statutory clocks were missed, 81 conversations had no reply at the 6 Nov count and the datasets were never reconciled to one baseline.",
        "Key links in the title chain for both parcels are still evidence pending: the 1877 agreement, the 1905 and 1924 instruments, the 1938 conveyance, the original May 1939 agreement, the 1955 and 1962 orders, and the 1982–83 first-registration files.",
        "Of 20 case questions in the Q&A register, 5 are open, 4 contested and 5 rest on the family account alone (Q&A register, Oct 2026).",
    ],
    options=[
        dict(id="O0", name="Do nothing", summary="Close at year end with only the Bute reply outstanding.",
             verdict="Rejected — leaves both title chains incomplete."),
        dict(id="O1", name="Repeat 2026 across all 88 lanes in parallel",
             summary="The 25 Nov draft: 1,408 tasks, no sequencing.",
             verdict="Rejected — exceeds the Executive's sending capacity and raises repeat-request (FOIA s.14) risk."),
        dict(id="O2", name="Staged, prioritised, product-based programme (recommended)",
             summary="Record holders first (Wave 1), successors second (Wave 2), review routes only on exception, low-relevance bodies checked before any request.",
             verdict="Recommended — same scope, deliverable load, measurable benefits."),
    ],
    benefits=[
        dict(id="B1", name="Question register dispositioned", measure="% of master-register questions with an evidenced answer or final disposition",
             baseline="Q&A register: 20 case questions, 6 documented or not-held (30%)", target="100% at G4", owner="Executive", measured="Monthly highlight; each gate"),
        dict(id="B2", name="Title-chain completeness — Parcel A", measure="% of chain links with a primary source or a holder's recorded 'not held'",
             baseline="Set at G0 from PD27-11 first issue", target="100% dispositioned at G4", owner="Executive", measured="Each gate"),
        dict(id="B3", name="Title-chain completeness — Parcel B", measure="As B2, for Parcel B",
             baseline="Set at G0 from PD27-12 first issue", target="100% dispositioned at G4", owner="Executive", measured="Each gate"),
        dict(id="B4", name="Evidence ingestion speed", measure="% of disclosures catalogued within one working day",
             baseline="Not measured in 2026", target="≥ 95%", owner="Project Manager", measured="Weekly"),
        dict(id="B5", name="Requester-side clock discipline", measure="Chases raised on the first overdue working day",
             baseline="2026: follow-up not systematic (lessons log)", target="100%; 0 missed", owner="Project Manager", measured="Daily control audit"),
    ],
    dis_benefits=["Executive time (he sends every request and makes every decision) — measured through weekly time-use reviews and controlled by staged waves.",
                  "Strain on relationships with bodies if requests overlap — controlled by one request per body per day and the duplicate check in PD27-06."],
    timescale="25 Nov 2026 (mobilise) to 17 Dec 2027 (G4).",
    costs="£0 cash (standing zero-spend rule). Cost is Executive time and agent compute on existing free tiers.",
    investment_appraisal="Free routes only: FOIA/EIR/SAR where applicable, voluntary archive enquiries and published catalogues. Any fee, paid copy or paywall is PAUSE—NO SPEND; use a free alternative or close that avenue.",
    major_risks="See RAID: Executive capacity, repeat-request refusals, homonym errors, retention loss, public-wording breaches.",
    benefits_review="Measured in each monthly highlight report and at every gate; post-programme benefits review in Q1 2028.",
)

STANDING_RULES = [
    "Research, not litigation: the programme raises queries about records; it does not bring proceedings.",
    "Zero spend. Any fee, paywall, paid copy, subscription, postage, licence or travel cost is PAUSE—NO SPEND; no paid exception.",
    "Agents draft; the Executive sends every email and makes every external contact.",
    "Agents propose by pull request; merging is the Executive's.",
    "Every statement cites catalogued evidence; missing evidence gets an 'evidence pending' record, not a conclusion.",
    "Public text follows the standing word list and never names the current owner.",
    "Two parcels, always: Parcel A (house) and Parcel B (eastern fields, woodland, green) are tracked separately.",
    "Every request warns about the duplicate Llandough / Great House names; Llandough-juxta-Cowbridge is out of scope.",
    "One request per body per day; drafts reconciled against the full thread before use.",
]

TOLERANCES = [
    dict(area="Time", programme="G4 on 17 Dec 2027 ± 0; stage ends ± 10 working days", lane="Milestone finish + 5 working days", statutory="0 days — requester actions on statutory dates never slip"),
    dict(area="Cost", programme="£0 cash — no paid exception", lane="£0; PAUSE—NO SPEND on fees/paywalls", statutory="No paid route; record the barrier and search free alternatives"),
    dict(area="Scope", programme="Cedwyn estate (Llandough-juxta-Penarth / Leckwith) only; lanes added or re-tiered only by change control", lane="Request scope may not be narrowed without a written scope analysis", statutory="—"),
    dict(area="Quality", programme="0 unsourced public statements; 0 banned public words; 100% of sends QA-approved", lane="Product accepted only against its quality criteria", statutory="—"),
    dict(area="Executive load", programme="≤ 2 outbound messages per working day; weekly time-use review; measure time per evidence outcome (no fixed weekly hours cap assumed)", lane="≤ 1 new first request per body per working day", statutory="—"),
    dict(area="Benefits", programme="B1 forecast < 80% at G3 → exception", lane="—", statutory="—"),
    dict(area="Risk", programme="Any risk scoring ≥ 15 (5×5) escalated to the Executive the same day", lane="Any lane BLOCKED > 10 working days → exception", statutory="—"),
    dict(area="Sustainability", programme="Free-tier infrastructure only; no new paid services", lane="—", statutory="—"),
]

RAID = [
    dict(id="R27-01", type="risk", title="Executive capacity is the bottleneck", p=4, i=5, response="Reduce: waves, one Wave 1 submission per working day, weekly decisions pack (issue #12), load tolerance.", owner="Project Manager"),
    dict(id="R27-02", type="risk", title="Bodies refuse overlapping requests as repeated or vexatious (FOIA s.14)", p=3, i=5, response="Avoid: duplicate check against live requests in PD27-06; one subject per request; reconcile 2026 history first (M0).", owner="Project Manager"),
    dict(id="R27-03", type="risk", title="Cost-limit refusals (FOIA s.12) on broad requests", p=4, i=3, response="Reduce: record-series-specific requests built from PD27-05; narrow by date range up front.", owner="Research agent"),
    dict(id="R27-04", type="risk", title="Homonym confusion (Llandough-juxta-Cowbridge, Llandow, other Great Houses)", p=3, i=4, response="Avoid: mandatory homonym paragraph; QA checks parish and grid reference on every record.", owner="QA agent"),
    dict(id="R27-05", type="risk", title="Records destroyed or lost under retention schedules before they are found", p=3, i=5, response="Reduce: preservation requests in M0 for every Tier 1 lane; retention status in PD27-05.", owner="Research agent"),
    dict(id="R27-06", type="risk", title="Public pages breach the standing wording rules", p=3, i=4, response="Avoid: automated word-list check before every merge; QA sign-off.", owner="QA agent"),
    dict(id="R27-07", type="risk", title="Parcel A and Parcel B records conflated in analysis", p=3, i=5, response="Avoid: separate products PD27-11 and PD27-12; every question tagged with a parcel.", owner="QA agent"),
    dict(id="R27-08", type="risk", title="Overlapping datasets added together (denominator errors)", p=3, i=3, response="Avoid: control rule; dated, scoped counts only.", owner="Project Manager"),
    dict(id="R27-09", type="risk", title="Agents edit the same page or file concurrently", p=3, i=3, response="Reduce: changes by pull request; one agent per page.", owner="Project Manager"),
    dict(id="R27-10", type="risk", title="Personal data of living people published from correspondence", p=2, i=4, response="Avoid: QA privacy check before publication (issue #20).", owner="QA agent"),
    dict(id="A27-01", type="assumption", title="Bute archive (Mount Stuart) resumes external enquiries in January 2027", p=None, i=None, response="Check first working week of January; if not, re-plan SP27-44 at G1.", owner="Executive"),
    dict(id="A27-02", type="assumption", title="Existing free tiers (Cloudflare, GitHub, HubSpot) remain available through 2027", p=None, i=None, response="Review at each gate.", owner="Project Manager"),
    dict(id="I27-01", type="issue", title="Parcel A plan still carries a legacy £0–£800 allowance; it must be amended to reflect the confirmed no-spend rule", p=None, i=None, response="No expenditure is authorised. Amend the Parcel A plan to £0 cash and mark every fee-bearing or paywalled route PAUSE—NO SPEND; use a free alternative or close it.", owner="Executive"),
    dict(id="I27-02", type="issue", title="HR-07 still open; 2026 datasets unreconciled", p=None, i=None, response="Close in P0 (GWP-01, GWP-13) before G0.", owner="Project Manager"),
]

DEPENDENCIES = [
    dict(id="DEP27-01", product="PD27-11 / PD27-12 (both title chains)", depends_on="SP27-44 Mount Stuart (Bute archive) reply — expected January 2027", type="External"),
    dict(id="DEP27-02", product="PD27-11 Parcel A chain", depends_on="SP27-05 HM Land Registry first-registration items for WA240304 and WA231076", type="External"),
    dict(id="DEP27-03", product="PD27-12 Parcel B chain", depends_on="SP27-16 Glamorgan Archives: 1939 agreement original and D696 WGR papers", type="External"),
    dict(id="DEP27-04", product="All Wave 1 request packs (PD27-06)", depends_on="PD27-03 master question register approved at G0", type="Internal"),
    dict(id="DEP27-05", product="All Wave 2 request packs", depends_on="Wave 1 M1 accepted (G1)", type="Internal"),
    dict(id="DEP27-06", product="Any Tier 3 lane beyond M0", depends_on="A remedy decision record (PD27-09) from a Tier 1/2 lane", type="Internal"),
    dict(id="DEP27-07", product="Tier 4 M1–M3", depends_on="Relevance gate RG (31 Mar 2027) promotes the lane", type="Internal"),
]

PROGRESS_RULES = dict(
    status_weight={"NOT_STARTED": 0, "IN_PROGRESS": 25, "BLOCKED": 25, "WAITING_FOR_AUTHORITY": 25,
                   "QA_FAILED": 50, "READY_FOR_QA": 75, "COMPLETE": 100, "CANCELLED_WITH_REASON": None},
    rollup="Task % from status weight. Work package % = mean of its tasks; milestone % = mean of its work packages; lane % = mean of its milestones; programme % = mean of lanes weighted by tier (Tier 1 × 3, Tier 2 × 2, Tier 3 × 1, Tier 4 × 1). CANCELLED_WITH_REASON tasks leave the denominator; a lane with every task cancelled counts as closed and drops out.",
    rag="Green: on or ahead of planned % for today's date. Amber: behind by ≤ 15 points or forecast inside tolerance. Red: behind by > 15 points or forecast outside tolerance (Exception Report required).",
)

CHANGE_CONTROL = [
    "Any change to scope, tiers, dates beyond tolerance or products is raised as a GitHub issue labelled 'change-request' (an Issue Report).",
    "The Project Manager records impact on time, benefits, risk and Executive load; QA reviews.",
    "The Executive decides: approve, reject or defer. Approved changes are applied by re-running tools/build_2027_plan.py and recorded in change_log.",
]

WORDING = [  # standing public word list fixes, applied to JSON strings and the page
    (r"\bexplicitly marked unverified\b", "explicitly marked evidence pending"),
    (r"\bremain unverified\b", "remain to be established"),
    (r"\bunverified\b", "not yet established"),
    (r"\bpublic allegation\b", "public statement"),
    (r"\bunsupported allegation\b", "unsourced statement"),
    (r"\bsays\b", "states"),
    (r"\ballegations?\b", "statement"),
]


def fix_words(s):
    for a, b in WORDING:
        s = re.sub(a, b, s)
    return s


def walk(o):
    if isinstance(o, dict):
        return {k: (v if k in ("roadmap_lane_id", "id", "url") else walk(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    if isinstance(o, str):
        return fix_words(o)
    return o


def pct(status):
    return PROGRESS_RULES["status_weight"].get(status, 0)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


# ---------------------------------------------------------------- build JSON
def build(d):
    d = walk(d)
    d["schema"] = "cedwyn-prince2-programme/1.1.0"
    d["status"] = "DRAFT_BASELINE_FOR_G0"
    d["generated_by"] = "tools/build_2027_plan.py"
    d["built"] = BUILT
    d["standing_rules"] = STANDING_RULES
    d["business_case"] = BUSINESS_CASE
    d["tolerances"] = TOLERANCES
    d["stage_gates"] = GATES
    d["tiers"] = {str(t): {k: v for k, v in x.items()} for t, x in TIERS.items()}
    d["product_breakdown"] = PRODUCTS
    d["raid_2027"] = RAID
    d["dependencies"] = DEPENDENCIES
    d["progress_rules"] = PROGRESS_RULES
    d["change_control"] = CHANGE_CONTROL
    gov = d["governance"]
    gov["project_board"] = ("Executive: Hywel (decision-maker; sends all external correspondence). "
                            "Senior User: the family as users of the evidence (Executive and Sion). "
                            "Senior Supplier: the agent hive (Project Manager agent, research agents) and, for records, the holding institutions. "
                            "Project Assurance: independent QA agent, never the drafter. Change authority: Executive.")
    gov["tolerances"] = "Quantified in the tolerances table; forecast breaches raise an Exception Report before the limit is crossed."
    for p in d["phases"]:
        s, e = STAGE_DATES[p["id"]]
        p["start"], p["end"] = s, e
        g = next((g for g in GATES if g["stage_closing"] == p["id"]), None)
        p["gate"] = g["id"] if g else None
        p["gate_date"] = g["date"] if g else None
        if p["id"] in STAGE_EXIT:
            p["exit"] = STAGE_EXIT[p["id"]]
        p["period"] = f"{s} to {e}"

    seq = {1: 0, 2: 0}
    lanes_out = []
    for inst in d["institutions"]:
        lid = inst["id"].lower()
        t = TIER_OF[lid]
        T = TIERS[t]
        inst["tier"], inst["wave"], inst["priority"], inst["mode"] = t, T["wave"], T["priority"], T["mode"]
        sub = None
        if t in seq:
            sub = add_wd(D(T["M"]["M2"][0]), seq[t])
            seq[t] += 1
            inst["planned_first_submission"] = sub.isoformat()
        ms_dates = {}
        for m in inst["milestones"]:
            mid = m["id"].split("-")[-1]
            a, b = map(D, T["M"][mid])
            m["planned_start"], m["planned_finish"] = a.isoformat(), b.isoformat()
            wps = [w["id"].split("-")[-1] for w in m["work_packages"]]
            if mid == "M2" and sub:
                clock_end = add_wd(sub, 25)
                wins = [(sub, clock_end), (add_wd(sub, 20), b)]
            else:
                wins = split(a, b, len(wps))
            for w, (ws, we) in zip(m["work_packages"], wins):
                w["planned_start"], w["planned_finish"] = ws.isoformat(), we.isoformat()
                w["product_id"] = WP_PRODUCT[w["id"].split("-")[-1]]
                ms_dates[w["id"].split("-")[-1]] = (ws, we)
        prev = None
        wp_last = {}
        for task in inst["tasks"]:
            ws, we = ms_dates[task["work_package"]]
            task["planned_start"], task["planned_finish"] = ws.isoformat(), we.isoformat()
            task["priority"] = T["priority"]
            task["product_id"] = WP_PRODUCT[task["work_package"]]
            preds = []
            if prev and prev["work_package"] != task["work_package"]:
                preds.append(wp_last[prev["work_package"]])
            elif prev:
                preds = list(prev.get("predecessors", []))
            if task["milestone"] == "M0" and task["work_package"] == "WP01" and not prev:
                preds = ["G0"]
            if t == 3 and task["milestone"] != "M0" and "PD27-09 trigger" not in preds:
                preds = preds + ["PD27-09 trigger"]
            if t == 4 and task["milestone"] != "M0" and "RG" not in preds:
                preds = preds + ["RG"]
            task["predecessors"] = preds
            task["percent_complete"] = pct(task["status"])
            wp_last[task["work_package"]] = task["id"]
            prev = task
        # roll-up
        for m in inst["milestones"]:
            for w in m["work_packages"]:
                wk = w["id"].split("-")[-1]
                w["percent_complete"] = mean([x["percent_complete"] for x in inst["tasks"] if x["work_package"] == wk])
            m["percent_complete"] = mean([w["percent_complete"] for w in m["work_packages"]])
        inst["percent_complete"] = mean([m["percent_complete"] for m in inst["milestones"]])
        lanes_out.append(inst)
    wt = {1: 3, 2: 2, 3: 1, 4: 1}
    # Fully cancelled lanes have no progress value and must leave both the
    # numerator and denominator; counting their tier weight as zero progress
    # contradicts the roll-up rule in PROGRESS_RULES.
    active_lanes = [l for l in lanes_out if l["percent_complete"] is not None]
    num = sum(l["percent_complete"] * wt[l["tier"]] for l in active_lanes)
    den = sum(wt[l["tier"]] for l in active_lanes)
    d["percent_complete"] = round(num / den, 1) if den else 0.0
    d["counts"] = {"lanes": len(lanes_out), "tasks": sum(len(l["tasks"]) for l in lanes_out),
                   "by_tier": {str(t): len(v["lanes"]) for t, v in TIERS.items()}}
    log = d.get("change_log", [])
    if not any(c.get("ref") == "issue #29" for c in log):
        log.append(dict(date=BUILT, ref="issue #29", by="Project Manager agent",
                        change="Schema 1.1.0: business case, quantified tolerances, dated gates, tiers and waves, task dates/priorities/products/predecessors, product breakdown, RAID, dependencies, % complete roll-up, change control; public word-list fixes.",
                        status="Proposed — awaiting Executive approval (PR)"))
    d["change_log"] = log
    return d


# ---------------------------------------------------------------- HTML
e = html.escape


def fmt(s):
    x = D(s)
    return f"{x.day} {x.strftime('%b')} {x.year}"


def table(head, rows):
    h = "".join(f"<th>{e(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f'<td data-l="{e(head[i])}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="t"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def sec(sid, title, pv, body, open_=False):
    o = " open" if open_ else ""
    return (f'<details class="sec" id="{sid}"{o}><summary><h2>{e(title)}</h2><span class="pv">{e(pv)}</span></summary>'
            f'<div class="body">{body}</div></details>\n')


def bar(p):
    p = p or 0
    return (f'<span style="display:inline-block;width:80px;height:8px;border-radius:4px;background:rgba(127,127,127,.25);vertical-align:middle">'
            f'<span style="display:block;width:{p}%;height:8px;border-radius:4px;background:currentColor"></span></span> {p:g}%')


def new_sections(d):
    L = d["institutions"]
    out = []
    # 0 plan on a page
    rows = []
    for t, T in TIERS.items():
        ls = [l for l in L if l["tier"] == t]
        rows.append([f"<b>{e(T['name'])}</b><br><small>{e(T['why'])}</small>", e(T["wave"]), str(len(ls)),
                     " · ".join(f"{k} {fmt(a)}–{fmt(b)}" for k, (a, b) in T["M"].items()), bar(mean([l['percent_complete'] for l in ls]))])
    g = table(["Gate", "Date", "Decision"], [[f"<b>{x['id']}</b> · {e(x['name'])}", fmt(x["date"]), e(x["decision"])] for x in GATES])
    body = (f"<p><b>Programme % complete:</b> {bar(d['percent_complete'])} (tier-weighted; rules in §3c). "
            f"<b>Cash budget:</b> £0. <b>Next gate:</b> G0 on {fmt('2027-01-04')}.</p>"
            + table(["Tier", "Wave", "Lanes", "Milestone windows (M0 · M1 · M2 · M3)", "% complete"], rows)
            + "<h3>Gates</h3>" + g
            + "<p class=\"note\">Wave 1 submissions are staggered one lane per working day from 1 March; Wave 2 from 4 May. Tier 3 opens only on a remedy decision; Tier 4 is promoted or closed at the relevance gate. "
              "Dates are generated by <code>tools/build_2027_plan.py</code> from the tier table, using England and Wales bank holidays.</p>")
    out.append(sec("plan-on-a-page", "0 · Plan on a page", "Tiers, waves, gates and % complete", body, True))
    # standing rules
    out.append(sec("standing-rules", "0a · Standing rules for 2027", f"{len(STANDING_RULES)} rules",
                   "<ul>" + "".join(f"<li>{e(r)}</li>" for r in STANDING_RULES) + "</ul>"))
    # business case
    bc = BUSINESS_CASE
    body = ("<h3>Reasons</h3><ul>" + "".join(f"<li>{e(r)}</li>" for r in bc["reasons"]) + "</ul>"
            + "<h3>Business options</h3>" + table(["Option", "Summary", "Verdict"], [[f"<b>{o['id']}</b> · {e(o['name'])}", e(o["summary"]), e(o["verdict"])] for o in bc["options"]])
            + "<h3>Expected benefits</h3>" + table(["ID", "Benefit", "Measure", "Baseline", "Target", "Owner", "Measured"],
                                                     [[b["id"], e(b["name"]), e(b["measure"]), e(b["baseline"]), e(b["target"]), e(b["owner"]), e(b["measured"])] for b in bc["benefits"]])
            + "<h3>Expected dis-benefits</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in bc["dis_benefits"]) + "</ul>"
            + f"<p><b>Timescale:</b> {e(bc['timescale'])}<br><b>Costs:</b> {e(bc['costs'])}<br><b>Investment appraisal:</b> {e(bc['investment_appraisal'])}<br>"
              f"<b>Major risks:</b> {e(bc['major_risks'])}<br><b>Benefits review:</b> {e(bc['benefits_review'])}</p>")
    out.append(sec("business-case", "3a · Business case", "Continued business justification", body))
    out.append(sec("tolerances", "3b · Tolerances and exceptions", "Quantified; set for approval at G0",
                   table(["Area", "Programme", "Lane / work package", "Statutory"], [[f"<b>{e(t['area'])}</b>", e(t["programme"]), e(t["lane"]), e(t["statutory"])] for t in TOLERANCES])
                   + "<p>A forecast breach raises an Exception Report to the Executive before the limit is crossed (issue #9).</p>"))
    pr = PROGRESS_RULES
    out.append(sec("progress-rules", "3c · % complete and status rules", "Task → work package → lane → programme",
                   table(["Status", "Weight"], [[k, "leaves denominator" if v is None else f"{v}%"] for k, v in pr["status_weight"].items()])
                   + f"<p>{e(pr['rollup'])}</p><p>{e(pr['rag'])}</p>"))
    out.append(sec("change-control", "3d · Change control", "Issue Reports via GitHub",
                   "<ol>" + "".join(f"<li>{e(x)}</li>" for x in CHANGE_CONTROL) + "</ol>"))
    # products
    rows = [[f"<code>{p['id']}</code>", e(p["type"]), f"<b>{e(p['name'])}</b><br><small>{e(p['purpose'])}</small>", e(p["composition"]), e(p["quality_criteria"]), e(p["quality_method"]), e(p["approver"])] for p in PRODUCTS]
    out.append(sec("product-breakdown", "5a · Product breakdown and product descriptions", f"{len(PRODUCTS)} products; every task linked to one",
                   table(["ID", "Type", "Product", "Composition", "Quality criteria", "Quality method", "Approver"], rows)
                   + "<p>Lane work packages map to products: WP01–02 → PD27-04, WP03 → PD27-05, WP04 → PD27-06, WP05 → PD27-07, WP06 → PD27-08, WP07 → PD27-09, WP08 → PD27-10.</p>"))
    rows = [[f"<code>{r['id']}</code>", e(r["type"]), e(r["title"]), "—" if r["p"] is None else f"{r['p']}×{r['i']} = {r['p']*r['i']}", e(r["response"]), e(r["owner"])] for r in RAID]
    out.append(sec("raid-2027", "5b · RAID log for 2027", f"{sum(r['type']=='risk' for r in RAID)} risks · {sum(r['type']=='assumption' for r in RAID)} assumptions · {sum(r['type']=='issue' for r in RAID)} issues",
                   table(["ID", "Type", "Item", "P×I", "Response", "Owner"], rows)))
    out.append(sec("dependencies-2027", "5c · Key dependencies", f"{len(DEPENDENCIES)} dependencies",
                   table(["ID", "Product", "Depends on", "Type"], [[x["id"], e(x["product"]), e(x["depends_on"]), x["type"]] for x in DEPENDENCIES])))
    return "".join(out)


def stages_html(d):
    rows = []
    for p in d["phases"]:
        g = f"<b>{p['gate']}</b> · {fmt(p['gate_date'])}" if p.get("gate") else "—"
        rows.append([f"<b>{p['id']} · {e(p['name'])}</b>", f"{fmt(p['start'])} – {fmt(p['end'])}", g, e(p["exit"])])
    return ('<details class="sec" id="stages" open><summary><h2>4 · Stages and stage gates</h2><span class="pv">Mobilisation plus four management stages, each closed by a dated gate</span></summary><div class="body">'
            + table(["Stage", "Dates", "Gate", "Exit criteria"], rows)
            + "<p>Each gate decision is proceed, amend, pause or stop, minuted in the decision log. No stage is passed merely because tasks were attempted; products must be accepted against their quality criteria.</p></div></details>\n")


def patch_html(s, d):
    s = fix_words(s)
    if '/2027-foi-programme/calendar/' not in s:
        s = s.replace('<a href="/programme-plan/">Master plan</a>',
                      '<a href="/programme-plan/">Master plan</a> · <a href="/2027-foi-programme/calendar/">2027 enquiry calendar</a>')
    s = s.replace("with 39 institution subprojects", "with 88 institution and recipient subprojects in four tiers")
    # facts line
    s = re.sub(r'<li>Tasks <b>[^<]*</b></li>(?:<li>Programme % <b>.*?</b></li><li>Next gate <b>.*?</b></li>)?',
               f'<li>Tasks <b>{d["counts"]["tasks"]:,} dated tasks</b></li><li>Programme % <b>{d["percent_complete"]:g}%</b></li><li>Next gate <b>G0 · {fmt("2027-01-04")}</b></li>', s, count=1)
    # remove previously inserted sections (idempotency), then insert
    s = re.sub(r'<details class="sec" id="(plan-on-a-page|standing-rules|business-case|tolerances|progress-rules|change-control|product-breakdown|raid-2027|dependencies-2027)".*?</div></details>\n', "", s, flags=re.S)
    # replace stages section
    s = re.sub(r'<details class="sec"(?: id="stages")? open><summary><h2>4 · Stages and stage gates</h2>.*?</div></details>\n?', lambda m: stages_html(d), s, count=1, flags=re.S)
    block = new_sections(d)
    first = block.split('<details class="sec" id="standing-rules"')[0]
    rest = block[len(first):]
    i = s.find('<details class="sec" open><summary><h2>1 · Programme mandate')
    s = s[:i] + first + s[i:]
    i = s.find('<details class="sec" id="stages"')
    s = s[:i] + rest + s[i:]
    # lanes: summary chips and task chips; drop the repeated focus text inside tasks
    for inst in d["institutions"]:
        sid = inst["id"].lower()
        T = TIERS[inst["tier"]]
        chip = f' · {T["name"].split(" · ")[0]} · {T["wave"]} · {inst["percent_complete"]:g}% complete'
        s = re.sub(rf'(<details class="sec" id="{re.escape(sid)}"><summary><h2>[^<]*</h2><span class="pv">)([^<]*?)(?: · Tier \d · [^<]*)?(</span>)',
                   lambda m: m.group(1) + m.group(2) + e(chip) + m.group(3), s, count=1)
        for tk in inst["tasks"]:
            pat = (rf'(<code>{re.escape(tk["id"])}</code> — )(.*?)( <span class="pv">\[)([A-Z_]+) · '
                   rf'(?:(?:High|Medium|Trigger|Conditional) · [^·\]]+ · PD27-\d\d · )?')
            def rep(m, tk=tk):
                desc = re.sub(r" Institutional focus: .*$", "", m.group(2))
                return (m.group(1) + desc + m.group(3) + m.group(4)
                        + f' · {tk["priority"]} · {fmt(tk["planned_start"])}–{fmt(tk["planned_finish"])} · {tk["product_id"]} · ')
            s = re.sub(pat, rep, s, count=1)
    return s


def main():
    d = json.loads(JP.read_text(encoding="utf-8"))
    d = build(d)
    JP.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    s = HP.read_text(encoding="utf-8")
    HP.write_text(patch_html(s, d), encoding="utf-8")
    print("lanes", d["counts"], "programme %", d["percent_complete"])


if __name__ == "__main__":
    sys.exit(main())
