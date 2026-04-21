# HawkinsOperations

**Detection engineering and SOC automation, built as a managed system rather
than a pile of scripts.**

This organization is the forward-looking home for the HawkinsOps system as it
migrates from a single public repository into a multi-repository architecture.
The live operational system and the current public proof surface remain at
[hawkinsops.com](https://hawkinsops.com) and
[raylee-hawkins/HawkinsOperations](https://github.com/raylee-hawkins/HawkinsOperations).
This organization is where the next generation is being built.

[![Current system](https://img.shields.io/badge/Current_system-hawkinsops.com-00D4FF)](https://hawkinsops.com)
[![Legacy repo](https://img.shields.io/badge/Legacy_repo-raylee--hawkins%2FHawkinsOperations-181717?logo=github)](https://github.com/raylee-hawkins/HawkinsOperations)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-raylee--hawkins-0A66C2)](https://linkedin.com/in/raylee-hawkins)

---

## Evaluating this work

Go to [hawkinsops.com](https://hawkinsops.com) for the live metrics, the
case studies, and the proof pack. The operational evidence lives there and
in the legacy repository. This organization is architecture-in-progress and
is not yet the right surface for evaluating current capability.

---

## The thesis

The dominant industry frames for AI in security operations are either
hand-waving about reliability or treating large language models as opaque
copilots attached to a human analyst. Both frames fail at scale. Hand-waving
produces brittle pipelines that silently drift. Copilot framing underuses
the model while still inheriting its unreliability.

HawkinsOperations starts from a different premise. Large language models
are unreliable labor. Unreliable labor, treated as labor, is a problem the
manufacturing world solved decades ago through management systems: intake
controls, standard work, verification gates, escalation paths, evidence
capture, regression harnesses, and post-incident review. The IATF 16949
and ISO 9001 frameworks that govern Tier 1 automotive production floors
are, at their core, systems for extracting reliable output from unreliable
inputs. Applied to an AI triage workforce running against a live SOC
pipeline, the same discipline produces a system that auto-closes what
should be closed, escalates what should not, and leaves an audit trail
for every decision. The domain changed. The discipline did not.

This thesis is what separates the work in this organization from the
default pattern of grafting a language model onto a SIEM and hoping for
the best.

---

## Why the split

The original build grew into a single public repository that mixed
detection content, validation harnesses, platform code, proof artifacts,
and the portfolio website. That worked while the system was small. It
stopped working once the proof surface had to serve recruiters, the
detection source had to be read by engineers, the validation had to be
run by automation, and the platform code had to evolve without breaking
published claims. The fix is the same fix any mature engineering
organization applies: separate surfaces by audience and by change
velocity.

This organization separates the system into five repositories, each
with a single responsibility, a single primary audience, and a rate of
change that matches its contents.

| Repository | Responsibility | Primary audience | Change velocity |
|---|---|---|---|
| `hawkinsoperations-detections` | Sigma, Wazuh XML, Splunk SPL rule sources | Engineers | High |
| `hawkinsoperations-validation` | Regression harnesses, rule-firing tests, FP/TP tracking | Automation | High |
| `hawkinsoperations-platform` | Pipeline control, AutoSOC orchestration, MCP servers | Engineers | Medium |
| `hawkinsoperations-proof` | Verified counts, case studies, evidence bundles | Reviewers | Low |
| `hawkinsoperations-website` | Source for the successor public site | Visitors | Medium |

The taxonomy is not arbitrary. Detections change weekly. Proof changes
quarterly. Mixing them inside one repository meant that every proof
update triggered noisy diffs against detection content, and every
detection tune polluted the commit history a reviewer would read to
audit proof. The split makes each surface legible on its own terms.

---

## Current system metrics

While the new architecture comes online, evaluation should happen against
the live system documented at [hawkinsops.com](https://hawkinsops.com).
Canonical figures as of the most recent truth-lock:

| Metric | Value |
|---|---|
| Verified cases triaged | **324,074** |
| Auto-close rate | **88%** |
| Detection coverage | **210** rules across Sigma, Wazuh XML, Splunk SPL |
| Escalation packs produced | **8,574** |
| Agent fleet | **10** Wazuh agents, 8/8 host coverage |
| Infrastructure | **15**-server Proxmox homelab, V100 local inference |

Canonical values live at hawkinsops.com. Any figure in this organization
that disagrees with the site is stale; the site wins.

---

## Background

Raylee Hawkins. Self-taught detection engineer. Built the current system
in eight months from a manufacturing supervision background running
IATF 16949, ISO 9001, and TISAX quality frameworks on Tier 1 automotive
production floors at Fehrer Automotive and Unipres Alabama, supervising
thirty-plus operators on twelve-hour shifts.

The manufacturing background is the core of the thesis, not an aside.
The management systems that govern an unreliable AI workforce are the
same systems that govern an unreliable human workforce. The framework
transferred. The output is this system.

---

## Contact

- Current system: [hawkinsops.com](https://hawkinsops.com)
- Email: raylee@hawkinsops.com
- LinkedIn: [linkedin.com/in/raylee-hawkins](https://linkedin.com/in/raylee-hawkins)
- Location: Gadsden, AL, relocating to Huntsville, AL
