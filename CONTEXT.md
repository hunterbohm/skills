# Workflow audit and build

Terms shared by the `workflow-audit` and `workflow-build` skills. One business, one workspace, one workflow at a time.

## People

**Owner**:
The person who sponsors the audit and approves the workflow choice.
_Avoid_: client, founder, sponsor, user

**Operator**:
The person who runs the workflow by hand today and will correct the built one.
_Avoid_: user, team member

**Approver**:
The named person who clears a consequential action at the gate.
_Avoid_: reviewer, stakeholder

**Customer**:
A person or organization the business serves.
_Avoid_: client, lead, account

## The audit

**Workflow**:
A recurring piece of work with a stable trigger, inputs, and output, seen across independent instances.
_Avoid_: process, automation, play, system

**Audit**:
The read-only survey that maps a business's workflows and chooses one to build.
_Avoid_: assessment, discovery, roadmap

**First run**:
The audit of a business that has no workspace yet.
_Avoid_: initial audit, onboarding

**Resume run**:
An audit run on a business that already has a workspace. It diffs against the ledger.
_Avoid_: re-audit, check-in, follow-up audit

**Source map**:
The list of systems that hold each kind of truth, with who may read and who may write each.
_Avoid_: integrations, tool list, stack

**Evidence label**:
The provenance of a workflow claim: observed, owner-reported, or inferred.
_Avoid_: confidence, source type

**Inventory**:
The ledger's list of every workflow found, each with its evidence label, status, and baseline.
_Avoid_: workflow map, catalog, list

**Baseline**:
The owner's own numbers for one workflow: runs per month, hours per run, hourly value.
_Avoid_: estimate, ROI, savings

**First workflow**:
The one workflow chosen to build first.
_Avoid_: pilot, MVP, quick win

**Runner-up**:
A workflow that waits until the first workflow has reached proven.
_Avoid_: backlog, phase two

## The workspace

**Audit root**:
The folder the owner chose to hold every workspace. Written `<audit-root>` in paths.
_Avoid_: base path, output directory

**Workspace**:
The one durable folder per business that every run shares.
_Avoid_: project, repo, output folder

**Ledger**:
The workspace's memory across runs: source map, inventory, statuses, corrections, run entries.
_Avoid_: state, database, index

**Correction**:
A dated standing rule or recorded owner decision that every later run applies.
_Avoid_: feedback, note, preference

**Owner summary**:
The one-page plain-language view regenerated after every run.
_Avoid_: report, status update, dashboard

**Run log**:
One line per workflow run: trigger, approver, action, verification.
_Avoid_: audit trail, history, telemetry

## The build

**Build spec**:
The runtime-neutral contract for one workflow, one pipeline stage at a time.
_Avoid_: PRD, design doc, plan

**Runtime**:
The system the owner already uses to run scheduled or triggered work, where the workflow is implemented.
_Avoid_: platform, host, runner

**Implementation**:
The workflow as built on the runtime, described in the workspace by where it lives, how to run it, how to switch dry-run and live, and how to stop it.
_Avoid_: scaffold, code, automation

**Pipeline**:
The fixed stage order every workflow follows: trigger, collect, agent joint, gate, act, verify, log.
_Avoid_: flow, chain, agent loop

**Stage**:
One element of the pipeline.
_Avoid_: step, phase, node

**Agent joint**:
The one bounded judgment the model makes inside a run, with a fixed output shape.
_Avoid_: prompt step, LLM call, reasoning

**Joint prompt**:
The fixed text the runtime sends to the model at the agent joint.
_Avoid_: system prompt, template, instructions

**Gate**:
The point where the approver reviews a proposed consequential action before it happens.
_Avoid_: human in the loop, checkpoint, review step

**Approval object**:
What the gate shows the approver: proposed action, target, evidence, draft, ambiguity, verification plan.
_Avoid_: approval card, request, ticket

**Fixture**:
One safe fixed input with its expected output, run with the act stage in dry-run.
_Avoid_: test case, mock, sample

**Dry-run**:
An act stage that prints the exact would-be write instead of performing it.
_Avoid_: test mode, sandbox, simulation

**Acceptance run**:
The one real run, cleared at the gate by the approver, that proves a built workflow.
_Avoid_: acceptance test, pilot run, UAT

**Ladder**:
The ordered statuses a workflow climbs: candidate, designed, built, proven, live.
_Avoid_: lifecycle, maturity model, state machine

**Rung**:
One status on the ladder.
_Avoid_: stage, phase, level

**Realized value**:
Hours and money returned so far, computed from verified real runs against the baseline.
_Avoid_: ROI, savings, impact, returned value

**Adoption gap**:
The difference between the baseline run rate and the actual verified run rate of a live workflow.
_Avoid_: usage, utilization
