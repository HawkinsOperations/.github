# HawkinsOps

Detection engineering and SOC automation with the evidence attached.

HawkinsOps is the GitHub home for Raylee Hawkins' detection, triage, and security automation work. The repositories here trace back to a single self-hosted operational pipeline: a live Wazuh deployment, a file-backed triage engine, CI-gated detection content, and script-verified proof artifacts. Claims are scoped to what was built, operated, and verified.

## Core repositories

- **[HawkinsOperations](https://github.com/HawkinsOps/HawkinsOperations)** - Live operational repository. Detection content (Sigma, Wazuh XML, Splunk SPL), IR playbooks, the AutoSOC pipeline, CI verification, and the `PROOF_PACK/` with script-generated counts and supporting evidence.
- **[SignalFoundry](https://github.com/HawkinsOps/SignalFoundry)** - Reviewer-facing narrative repo. Architecture docs, methodology, detection principles, case studies, and representative samples for understanding the system without digging through the full operational repository.
- **[wazuh-mcp-server](https://github.com/HawkinsOps/wazuh-mcp-server)** - Focused technical artifact. A read-only Model Context Protocol server in TypeScript for exposing Wazuh agent status, alerts, rules, and manager health to MCP clients. No write operations are exposed.

## Proof over posture

Counts are script-generated, not self-reported. Detection content passes validators and CI before it lands. Case studies are derived from real operational work and tied back to evidence. In `HawkinsOperations`, `PROOF_PACK/VERIFIED_COUNTS.md` is the source of truth, and drift between markdown, JSON, and site data fails CI.

AI tools are used to accelerate drafting, review, and analysis. They are not used to bypass validation, make escalation decisions, or create claims that cannot be traced back to a script or artifact.

## Scope honesty

This is a single-operator, self-hosted lab environment run with production discipline. It is not an enterprise SOC and is not presented as one. The Wazuh deployment is single-node with 10 agents, and the pipeline is intentionally simple enough to remain inspectable and reviewable. Direct experience here covers detection authoring, Wazuh deployment and tuning, pipeline engineering, and verification discipline.

## Start here

- **Recruiter / hiring manager** -> [START_HERE.md](https://github.com/HawkinsOps/HawkinsOperations/blob/main/START_HERE.md)
- **Technical reviewer** -> [SignalFoundry](https://github.com/HawkinsOps/SignalFoundry) then [`PROOF_PACK/VERIFIED_COUNTS.md`](https://github.com/HawkinsOps/HawkinsOperations/blob/main/PROOF_PACK/VERIFIED_COUNTS.md)
- **Detection engineer** -> [`content/detection-rules/INDEX.md`](https://github.com/HawkinsOps/HawkinsOperations/blob/main/content/detection-rules/INDEX.md)
- **MCP / tooling reviewer** -> [wazuh-mcp-server](https://github.com/HawkinsOps/wazuh-mcp-server)
- **Portfolio site** -> [hawkinsops.com](https://hawkinsops.com)
