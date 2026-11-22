---
title: "Workspace review, responsibility and handover"
version: "1.0.0"
updated: "2026-11-22"
owner: "Double FW Ltd"
license: "MIT"
language: "en-GB"
status: "editorial_guidance_for_local_adoption"
---

# Workspace review, responsibility and handover

Use this with the [21-item checklist](Accessible_Workspaces_Design_Checklist.md). These are adaptable local planning instructions, not adopted assignments, a professional access/safety assessment or an installed approval workflow. Involve affected people appropriately without requiring unnecessary diagnosis disclosure or exposure to known hazards.

## Plan a connected review

Define the actual tasks and routes, premises use, jurisdiction, opening hours, project stage, necessary facilities and material dependencies. Consider pre-arrival information, entry/security, work, shared facilities, meetings, support and departure together. Include temporary, busy, out-of-hours and hybrid contexts where relevant. Use drawings, reports, actual measurements, safe walkthroughs and competent specialist evidence for what each can establish; a drawing review is not an inspection.

Identify known urgent barriers and appropriate interim access before routine completion of the record. Agree a proportionate participation plan. Do not stage an unsafe transfer, access attempt, equipment failure or evacuation simply to gather evidence. Emergency arrangements and specialist equipment/design decisions belong with the relevant competent roles.

## Delivery roles to confirm locally

| Question | Role or responsibility to establish | Practical handover |
| --- | --- | --- |
| Who owns scope, resources and unresolved priorities? | Actual project/employer decision-maker | Define decisions and dependencies; identify limits of delegated authority. |
| Who controls routes, furniture and day-to-day operation? | Facilities/estates or the relevant workspace owner | Preserve access while arranging changes and maintenance. |
| Who specifies technical design or building work? | Competent design/access/building professionals as applicable | Supply task evidence and the applicable source question; do not invent dimensions. |
| Who controls fire, emergency and safety arrangements? | Actual responsible safety/fire roles | Refer the specific risk through established arrangements; a refuge is not the whole plan. |
| Who controls booking, entry, communication and work systems? | Relevant IT/product/service owner | Verify real interfaces and configurations; avoid treating building access as proof of digital access. |
| Who coordinates individual support? | Line manager/HR or another agreed coordinator | Minimise sharing, retain interim access and distinguish coordination from delivery control. |
| Who handles supplier, funding, legal or privacy decisions? | Relevant authorised specialist/owner | Prepare a bounded question and options; do not infer contractual remedies or approvals. |
| Who verifies and reviews the outcome? | Appropriate reviewer/specialist with affected-user input | Record actual task evidence, conditions and residual limits, not simply task completion in a project tool. |

This table proposes responsibilities to establish; it does not appoint anyone or assert that those services exist. Where a manager is implicated or a concern is disputed, use an actual appropriate independent route. Do not send a referral or publish site/case details without authority.

## Record progress and evidence separately

| Workflow status | Check result | Required interpretation |
| --- | --- | --- |
| `not_assessed` | `not_tested` | The specified review did not run. Blank context is unassigned. |
| `in_progress` | `unknown` | Evidence or decisions do not yet establish the whole item’s result. A partial check is not a parent pass. |
| `works_as_intended` | `pass` | Scoped evidence and actual verification support the stated task/location/conditions. Not universal suitability or compliance. |
| `barrier_found` | `fail` | Evidence shows a barrier to the stated intended use; preserve whether it is observed, measured or reported. |
| `not_applicable` | `not_applicable` | A scoped rationale and actual accepted applicability decision exist. Uncertainty or pending approval is not not applicable. |

Record an evidenced barrier as barrier_found/fail without waiting for unrelated checks; preserve remaining untested parts separately. Record open issues, action proposals, actual assignments, human decisions and later verification separately. Preserve the owning vocabulary if importing a specialist test result; a tool error, task-blocked outcome or legal question cannot silently become a pass. Do not erase a credible report because direct observation is unavailable.

The [schema](workspace-finding.schema.json) defines the local record shape, permitted identifiers/states and conditional requirements. The [example](workspace-finding.example.json) is intentionally blank and labelled illustrative. Nulls mean unassigned, never actual approval or completed work. `record_state: recorded` requires a non-identifying project reference, AW item, jurisdiction, premises use and actual task/location. Schema validation does not establish the truth of any entered evidence or decision. Use a Draft 2020-12 validator with date format checking where implementing validation; no validation service is installed here.

## Meetings and temporary event setups

When a workspace hosts a meeting or staff event, define the attendee, presenter, remote-participant and staff tasks. Review arrival/security and out-of-hours arrangements, furniture/seating and routes, facilities, sensory conditions, communication/materials and the actual hybrid platform. Apply relevant AW items, particularly AW-01–AW-09, AW-13–AW-19 and AW-21, rather than assuming the room’s normal layout covers a temporary setup.

Ask relevant communication and access preferences without requiring public disclosure. Prepare usable invitations/materials and contact routes; check captions, hearing support, meaningful visual descriptions and remote participation where needed. A single feature such as captions does not provide every communication alternative. Keep service/facilities owners and the actual safety arrangements involved. Recheck access after changing room layout or equipment. This local guidance covers workspace and meeting dependencies, not every aspect of organising a conference.

Use the public [HR communication module](https://github.com/Double-FW/Inclusion-for-Managers-and-HR-Systems/blob/main/docs/04-communication.md) and [meeting checklist](https://github.com/Double-FW/Inclusion-for-Managers-and-HR-Systems/blob/main/checklists/meetings.md) for optional detailed prompts. Retain their proposed-practice status and individual-choice/privacy boundaries.

## Verify, hand over and reopen

A useful handover identifies the item/task, evidence and scope, barrier or uncertainty, interim access, options and dependencies, proposed delivery role, actual decision where known, verification plan and review/reopen trigger. Keep unagreed names/dates unassigned. A proposed repair, order, ticket closure or training session is not verified restoration of access.

Check the changed real task/route in relevant conditions with appropriate expertise and affected-user input. Revisit dependent digital/physical features and cumulative burdens, not just the changed component. Review after relocation, refurbishment, layout/role/system/supplier changes, maintenance failure or a barrier report. Keep actual review/evidence dates separate from source retrieval and editorial updates.

## Privacy and scope

Completed records belong only in the real approved project/case system. Do not put personal adjustment/health information, confidential site/security details, credentials or identifying narratives in public examples or datasets. Minimise evidence references and assess re-identification risk; pseudonyms alone do not establish anonymity. No retention, access-control, redaction, escalation or evidence-store mechanism is configured by these documents. See [NOTICE](NOTICE.md) and [public source routes](Related_Double_FW_Guidance.md).
