# ops-audit and ops-foundation

`ops-audit` is a user-invoked expert operations diagnosis. It is not a workspace protocol and is not implicitly invoked. Its visible sequence is: interview one question at a time; get consent; inspect evidence; reconstruct causal work paths; choose the right intervention; prove claims; render the roadmap.

The only owner-facing audit result is offline `roadmap.html`. Its first screen shows first move, first automation (or a written reason for none), known monthly hours, annual labor burden, and unknown-cost count. Cards disclose action, cost, existing coverage, diagnosis, proof, then evidence. Feedback is accept/change/reject; change requires a note and uses revision-safe clipboard text. Storage and clipboard fallbacks remain visible.

Every roadmap has exactly one first move. Existing automation is evidence: audit scripts/jobs, definitions, recent runs, outputs, and failure visibility before proposing work. Owner numbers are the only cost inputs; unknown remains unknown. A partial stop renders an incomplete roadmap.

The deterministic spine owns flow. A model may make bounded judgment only, with a required shape; malformed output receives one retry, then a visible flag and no action. Consequential actions require named approval and read destination state back. Patterns are post-diagnosis hypotheses, not evidence.

After owner approval, ops-audit may model-invoke `ops-foundation` when it is installed. Until then it reports unavailable handoff and stops. The local generated catalog includes every installable package. Explicit-invocation policy is separate from catalog eligibility; publication remains a manual review decision.
