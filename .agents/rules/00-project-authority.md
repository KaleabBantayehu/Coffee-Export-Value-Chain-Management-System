# Rule 00 — Project Authority and Document Precedence

## Purpose

This rule defines which documents govern CEVCMS V1.0, in what order, and what
a human or AI agent must do when two documents appear to disagree. No task,
architecture decision, or feature is valid unless it can be traced to one of
the documents listed below.

## Authoritative source documents, in order of precedence

When documents conflict, the document higher in this list wins, **unless**
that document is explicitly marked as narrowed or superseded by a
lower-numbered use in Section 2 below (this happens once: see the frontend
framework resolution).

1. **Project Baseline & Scope Freeze** (`ECTA-CEVCMS-BASELINE-V1.0`)
   Controls the frozen V1.0 implementation boundary: core scope, stretch
   scope, out-of-scope list, the critical acceptance workflow, team
   ownership, and the change-control policy. This is the single most
   authoritative document for "what is CEVCMS V1.0."

2. **Implementation Specification & Development Backlog**
   Controls the technical stack freeze, the EPIC/task backlog, task
   ownership, and the four-week implementation order. Where the Baseline sets
   the boundary, this document sets the concrete backlog inside it.

3. **Design Document V1.0** (`ECTA-CEVCMS-DD-V1.0`)
   Controls the technical implementation design: architecture, data model
   (ERD), API design, sequence diagrams, and security design for the modules
   in scope.

4. **Minimum Project Plan** (`ECTA-CEVCMS-PP-V1.0`)
   Controls the one-month schedule, milestones, and dependencies. **Status:
   not available in the project repository at the time these rules were
   written.** Until it is supplied, the four-week schedule in the
   Implementation Specification and the Implementation Playbook is used in
   its place — see `README.md` for the full note. Any agent that locates or
   is given the actual Minimum Project Plan must flag any schedule
   discrepancy rather than silently adopting either version.

5. **Software Requirements Specification (SRS)** (`ECTA-CEVCMS-SRS-V2.1`)
   Controls detailed functional and non-functional requirement wording
   (FR-xxx, SEC-xxx, NFR-xxx identifiers) **within** the scope already
   approved by documents 1–3. The SRS describes ECTA's full national
   enterprise system; it is a source of requirement detail for in-scope
   modules, never a source of additional scope.

6. **Assignment Description** (`ECTA-CEVCMS-AD-V1.0`)
   Controls the university assignment's objectives, deliverables, and
   acceptance procedure. Relevant for what the team must demonstrate and
   report, not for backend/frontend implementation detail.

7. **Implementation Playbook** (`ECTA-CEVCMS-PLAYBOOK-V1.0`)
   Controls the agreed day-to-day development workflow: git process,
   per-feature checklist, and the immediate next-steps sequence. This
   `.agents/` directory implements the Playbook's Section 11 ("Working Rule
   for AI-Assisted Development") in structured form.

8. **ECTA Phase 1 Discovery Report** — context only.
   Provides stakeholder and business background. It must **never** be used to
   justify adding a feature, module, or requirement to V1.0. If the Discovery
   Report describes something the SRS or Baseline does not include in V1.0
   scope, it stays out.

## One already-resolved conflict

The Design Document left the frontend framework open ("Angular or React —
team's final choice confirmed at implementation start"). The Implementation
Specification and the Baseline have since fixed this to **React + JavaScript**.
This is treated as resolved, not open: **React only. Do not introduce
Angular or discuss it as a live option.**

## What an agent must do when it finds a conflict

1. **Stop.** Do not silently pick one side or blend both.
2. Identify the two (or more) conflicting documents and quote the specific
   conflicting statements.
3. Apply the precedence order above to determine which document should win.
4. If precedence resolves it cleanly, proceed under the higher-authority
   document **and record the conflict** in the task's `Expected Agent Report`
   section (see task file format) so a human reviewer sees it.
5. If precedence does **not** resolve it cleanly (e.g., the conflict is
   between two sections of the same document, or the higher-authority
   document is silent on the specific point), **do not proceed**. Raise the
   conflict to the Project Manager (Kaleab) for a decision. Do not invent a
   resolution.

## Traceability requirement

Every implementation decision of consequence must be traceable to at least
one of:

- an SRS requirement ID (e.g., `FR-FARM-001`),
- a Design Document section (e.g., "Design Document §4.2"),
- an Implementation Specification backlog item (e.g., "EPIC 1, Backend
  Tasks"),
- a Baseline scope line (e.g., "Baseline §3.1 Core Scope"),
- or a Minimum Project Plan milestone/dependency, once that document is
  available.

If an agent cannot find a traceable source for something it believes it needs
to build, that is a signal to **stop and ask**, not to invent a plausible
requirement. See `01-scope-boundaries.md`.
