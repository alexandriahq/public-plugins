# Report intake: save, ask, update

## Destination

Product/customer feedback in this workflow goes to **Product Feedback**, data source `3d4c87e6-4427-8028-a439-000b23f9417f`, database `3d4c87e6-4427-80bf-b230-c8101df648b6`. Its title is **Feedback**. Do not substitute engineering Issues (`9a2fbcbd-f0af-4b86-a53e-ed166146fa32`). Existing engineering issue records remain there; do not duplicate or migrate them automatically. Outside this enrolled Alexandria workflow, use the explicitly configured destination.

The table covers both schemas: fill every field present in the actual live schema, not properties that exist only in another database. Product Feedback uses Classification, Customer type and OS; do not create Issues-only hierarchy or ownership fields to satisfy this table.

A request to file/report a problem authorizes saving it to the configured tracker. Do not wait for follow-up answers, complete diagnostics, GitHub availability, or a final confirmation before the first Notion write. This contract overrides GitHub-first filing and summary-only Notion intake for polish reports.

1. Inspect the live database schema and existing report identifiers. Immediately create or update the Notion row with all currently available user-provided facts, known context and dates. Use a stable Report ID generated once (reuse the diagnostic reportId when already available). Do not delay persistence to run diagnostics. Set Status=Open, Archived=false. Fill every writable property, or explicitly account for its pending/not-applicable value in Field Notes. Read back the saved row and show its link.
2. Collect bounded diagnostics and create/link the GitHub detail issue when available. Persist additional facts immediately. Put the outstanding questions in Follow-up Questions and set Completeness=Needs information before asking those questions in chat. Ask only for facts that cannot be inferred reliably, using the actual field names; group related questions into one concise message. The saved record must already contain the user's report if they leave or cancel the conversation.
3. On each answer, update the same Notion row and linked GitHub issue; preserve Report ID and Created, refresh Updated, remove only answered questions, and read back the changes. Do not require all answers before saving a partial reply. No reply leaves the row Open / Needs information. Never delete, archive, close, or cancel a report merely because the user stopped replying. Explicit user cancellation/deletion instructions still apply.

## Field-by-field contract

Read this table before every intake. Enumerate the live schema so newly added properties are also accounted for. Notion formula, rollup, created-time, last-edited-time and other computed properties are read-only: verify them, do not write them.

| Field | Fill with / missing-value rule |
| --- | --- |
| Feedback / Name | Concise symptom and affected surface; derive from the user's report. |
| Classification | Bug or Improvement according to the reported behavior; if unclear leave select null, record pending and ask. |
| Company | Reporter’s stated company; unknown is pending and ask. Internal Alexandria reports may use Alexandria when established. |
| Customer contact | Known reporter email only. Missing: typed null, pending explanation and ask for a follow-up contact; do not fabricate an email. |
| Customer type | Internal or External from known relationship; unknown is pending and ask. |
| OS | macOS, Windows or Linux from evidence; unknown is pending and ask. Put version/architecture in Environment. |
| Report ID | Stable diagnostic reportId or a newly generated UUID before first write. Keep it across retries; attach later diagnostic bundle IDs as evidence without replacing it. |
| Summary | Short factual report summary, including all supplied context not mapped below. |
| Observed | What happened, preserving meaningful error text. Unknown: `Pending — what happened?` and ask. |
| Expected | Intended outcome from user or established contract. Label an inference; if uncertain, save `Pending — expected outcome` and ask. |
| Reproduction | Known steps and frequency; preserve a one-off occurrence as such. Missing details are pending and become follow-up questions. Do not invent reproducibility. |
| Environment | Product, App/Bridge versions, release channel, OS/architecture and relevant setup, each known value plus explicit pending values. Ask only for unavailable relevant context. |
| Impact | Affected task/users, frequency and workaround. Unknown details are pending; ask. |
| Evidence | Links or concise facts already provided; label source/mock/native evidence. `Pending — not yet collected` if absent. Keep raw diagnostics/screenshots on GitHub; never upload private capture or secrets. |
| GitHub Issue | Exact existing/created issue URL. Until available, typed null plus `GitHub Issue: Pending — creation/link unavailable` in Field Notes. First Notion save must not depend on GitHub. |
| Status | Open on intake; Fixed only after released-version verification; Closed only with a recorded disposition. Missing answers never change this lifecycle. |
| Completeness | Needs information while any relevant fact/question or required linking operation is pending. Complete only when every property is known or legitimately not applicable and there are no unresolved questions. This is independent of issue Status. |
| Follow-up Questions | Exact unanswered questions keyed to fields. `None — intake complete` when none. Persist before asking in chat. |
| Field Notes | Every pending or not-applicable property with its reason, including typed-null dates/links/relations. `None — all fields have known values` only if true. Also record declared defaults and any extra schema properties. |
| Created | First report-save timestamp in ISO 8601 with timezone; immutable. Backfill existing rows from Notion created_time, not today's time. |
| Updated | Current ISO 8601 timestamp with timezone on every report mutation. |
| Incident At | Actual incident timestamp with timezone, or date-only if that is all the evidence supports. Never substitute reporting time. If unavailable: typed null, Field Notes pending, ask when it happened and timezone if needed. |
| Due | User/team-agreed deadline. No deadline: typed null and `Due: N/A — no deadline set`. Never invent one; ask only when a deadline is implied but unspecified. |
| Verified At | Date/time the original scenario passed on the running released version. While Open: typed null and `Verified At: N/A — not verified on a release`. Source tests are not a verification date. |
| Closed At | Actual closure timestamp plus disposition in Field Notes. While open: typed null and `Closed At: N/A — issue remains open`. |
| Creator | Human reporter's known name; distinguish reporting agent if useful. Unknown reporter: pending and ask. |
| Assignee | Configured owner, defaulting in Alexandria to bot.owner.user from ntn whoami, never the integration bot. Record default in Field Notes. Unknown/unresolvable owner: empty people list plus pending explanation and ask. |
| Priority | Derive from stated impact using existing options; record rationale. If impact unknown use No priority only if that option exists; otherwise leave select null. Record pending rationale and ask about impact. |
| Labels | Existing supported category, e.g. Bug for a defect; preserve existing labels. Unclear category: pending explanation and ask. |
| Project / Team | Configured destination (Alexandria: Product Development / Alexandria), recording defaults. If destination unknown, ask; do not infer a destination from diagnostics. |
| Archived | false for active intake. Silence is not authorization to archive. |
| Git Branch / GitHub Branch / GitHub PR | Verified linked implementation branch/name/PR. Before implementation, rich-text N/A / typed-null URLs with `N/A — no implementation yet` in Field Notes. Never invent links. |
| Parent / Parent item / Sub-item / Sub-items / Parent ID | Existing known relationships, preserving established links. Standalone report: empty relation lists and Parent ID=N/A, with reasons in Field Notes. Do not manufacture hierarchy. |
| Legacy ID / Legacy Source | Existing import identity/source only. New report: Legacy ID=N/A, null Legacy Source, Field Notes `N/A — not imported`. |
| Any additional writable property | Populate from reliable context; otherwise add its exact name and pending/N/A reason to Field Notes, and ask if it needs user input. Never silently ignore new fields. |

All fields must be accounted for. Text supports `Pending — …` or `N/A — …`; typed dates, URLs, people and relations do not support text placeholders, so leave their typed value null/empty and put the explanation in Field Notes. This is not permission to claim a record is complete while required facts remain unknown.

## Failure and retry

Use ntn first for Notion, and gh for GitHub when available. If a save times out, search by Report ID before retrying creation. Once a page ID exists, update it rather than creating another row. A diagnostic collection failure or missing capability never blocks initial intake. GitHub failure leaves the existing Notion report with a pending link and its original facts intact. If Notion itself is unavailable, preserve a local draft, report the failed save honestly, and retry/reconcile by Report ID when access returns; never claim it was uploaded.
