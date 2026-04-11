# HawkinsOps

Detection engineering, SOC automation, and proof-driven security operations.

Built by [Raylee Hawkins](https://github.com/raylee-hawkins) — from zero experience to a live 10-agent Wazuh deployment in 7 months.

---

**[Live portfolio](https://hawkinsops.com)** | **[Flagship repo](https://github.com/HawkinsOps/HawkinsOperations)** | **[LinkedIn](https://linkedin.com/in/raylee-hawkins)**

---

### What this is

A live detection and triage pipeline on self-hosted infrastructure. The AutoSOC engine ingests Wazuh alerts from a 10-agent deployment, performs policy-driven triage, redacts sensitive fields, and assembles escalation packs as reproducible proof artifacts.

### By the numbers

- **103** Sigma rules | **28** Wazuh rule blocks | **79** Splunk searches | **10** IR playbooks
- **123** MITRE ATT&CK technique/sub-technique IDs across 69 families
- **8,574** escalation packs from 324,074 total cases (~88% auto-close rate)
- **7** CI workflows verifying content integrity, drift detection, and deployment

Every count is script-generated and reproducible. If a number is in the repo, a script verified it.

### Key work

- **Wazuh telemetry remediation** — diagnosed three independent failures, restored process creation visibility from zero to 2,120+ indexed events
- **Detection tuning sprint** — 23 targeted exclusions across 328K alerts, zero MITRE technique coverage removed
- **Race condition fix** — TOCTOU bug at 505K queue depth, 4-site patch, zero data loss
- **Pipeline recovery** — six-day outage, ~1.1M alert backlog reconciliation
- **15-server MCP stack** — Windows native, including custom Wazuh MCP server in TypeScript
