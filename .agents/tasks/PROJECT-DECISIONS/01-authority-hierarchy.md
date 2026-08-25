# PD-001 - Authority Hierarchy Decision

## Objective

Resolve and record one authoritative document-precedence order for CEVCMS V1.0 conflict handling.

## Why the decision is needed

The project currently has three different precedence statements. Developers cannot safely decide whether the Baseline, Assignment Description, SRS, Design Document, Implementation Specification, or Playbook controls a conflict without a single approved order.

## Authoritative sources

- [rules/00-project-authority.md](../../rules/00-project-authority.md), “Authoritative source documents, in order of precedence”.
- [execution/00-execution-overview.md](../../execution/00-execution-overview.md), “Authority Hierarchy”.
- [Implementation Playbook](../../docs/CEVCMS_V1.0_Implementation_Playbook.md), Section 1, “Document Precedence”.

## Current documented positions

The rules order is Baseline -> Implementation Specification -> Design -> Minimum Project Plan -> SRS -> Assignment -> Playbook. The execution order is Assignment -> SRS -> Minimum Project Plan -> Baseline -> Design -> Implementation Specification -> Playbook -> task packages -> rules/execution. The Playbook diagram places Discovery -> SRS -> Assignment -> Minimum Project Plan -> Design -> Implementation Specification/Backlog -> Baseline -> actual development.

## Conflict/gap

These are materially different orders, not formatting variants. The execution procedure also says it sits below Levels 1-4, while the rules file says the rules govern durable project decisions. The current project-decision file lists Baseline first but does not reconcile the execution/playbook orders.

## Impact

FIN, GIN, QR, ownership, schedule, scope, and QA-order conflicts could receive different outcomes. A developer could follow one order while a reviewer follows another.

## Options

1. Adopt the rules order, with the Baseline controlling V1.0 boundary, Implementation Specification controlling backlog/stack/order, Design controlling technical design, Minimum Project Plan controlling schedule, SRS supplying detailed requirements within the approved boundary, Assignment controlling academic deliverables, and Playbook controlling workflow.
2. Adopt the execution hierarchy, placing Assignment/SRS above project baseline.
3. Adopt the Playbook diagram.
4. Defer all conflict-sensitive implementation until the Project Manager publishes a reconciled order.

## Recommended resolution

Recommendation only, not a decision: adopt option 1 because the rules explicitly state it controls “what is CEVCMS V1.0,” while distinguishing backlog, design, schedule, and requirements responsibilities. Preserve higher-level Assignment/SRS obligations where they do not conflict with the frozen V1.0 boundary. The Project Manager must approve or reject this recommendation.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final decision: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab. Human review by a project member other than the author; record approval in current project decisions before implementation.

## Dependencies

None for preparation. This decision is a prerequisite for PD-002 through PD-008 and for conflict-sensitive coding.

## Acceptance criteria

- The three competing orders are recorded with their source locations.
- One approved precedence order is recorded by the Project Manager.
- Conflict-handling responsibility for scope, backlog, design, schedule, requirements, and workflow is explicit.
- No developer is instructed to treat an unapproved recommendation as final.

## Developer/PM handoff instructions

**DO NOT IMPLEMENT UNTIL APPROVED** for any conflict-sensitive decision. Until approval, stop and use the escalation format in `../../execution/06-failure-and-escalation.md`.
