# ClaritasZ Publications

Everything ClaritasZ publishes, in one place: reports, essays, papers and AI prompts.

| Kind | Folder |
|---|---|
| Reports | [`reports/`](./reports/) |
| Essays | [`essays/`](./essays/) |
| Papers | [`papers/`](./papers/) |
| AI prompts | [`prompts/`](./prompts/) |

Published files are never overwritten. A new version is added next to the previous one.

## Reports

Concise architecture reports that translate consequential developments into role specific decision impact.

Each edition separates confirmed fact, architecture interpretation, sector impact and the decisions that may need to be reconsidered.

### Publication rhythm

#### Tuesday · Nederlandse weekeditie

Six Dutch one page reports based on one shared factual ground:

- De Enterprisearchitect
- De Businessarchitect
- De Dataarchitect
- De Integratiearchitect
- De Securityarchitect
- De Infrastructuurarchitect

The Dutch edition focuses on developments with material impact in the Netherlands.

#### Thursday · European weekly edition

Six English one page reports covering the same architecture perspectives from a European context:

- The Enterprise Architect
- The Business Architect
- The Data Architect
- The Integration Architect
- The Security Architect
- The Infrastructure Architect

This is a separate European selection, not a translation of the Dutch edition.

#### Last Friday · European Architecture Review

A monthly English theme issue looking back at the most consequential European architecture theme of the month.

The review interleaves six A4 architecture perspectives with five in depth developments and closes with an editorial on their interactions. The first issue covers September 2026.

### Architecture perspectives

| Perspective | Accent |
|---|---|
| Enterprise | Grey |
| Business | Red |
| Data | Orange |
| Integration | Green |
| Security | Purple |
| Infrastructure | Blue |

Colour supports recognition. The editorial system remains consistent across every report.

### Latest published editions

#### Nederlandse reports · editie 26-40

- [De Enterprisearchitect](./reports/de-enterprisearchitect/2026/De_Enterprisearchitect_26_40.pdf)
- [De Businessarchitect](./reports/de-businessarchitect/2026/De_Businessarchitect_26_40.pdf)
- [De Dataarchitect](./reports/de-dataarchitect/2026/De_Dataarchitect_26_40.pdf)
- [De Integratiearchitect](./reports/de-integratiearchitect/2026/De_Integratiearchitect_26_40.pdf)
- [De Securityarchitect](./reports/de-securityarchitect/2026/De_Securityarchitect_26_40.pdf)
- [De Infrastructuurarchitect](./reports/de-infrastructuurarchitect/2026/De_Infrastructuurarchitect_26_40.pdf)

#### European reports

- [The Infrastructure Architect · European Edition 26-09](./reports/sample/the-infrastructure-architect/eu/2026/The_Infrastructure_Architect_26_09.pdf)

#### European Architecture Review · 26-09

- [September 2026 · European Architecture Review](./reports/european-architecture-review/2026/European_Architecture_Review_26_09.pdf)

### How to publish

publications.claritasz.com is built from these folders on every push to `main` (see `build.py`). Put the PDFs in the right folder with the right name; the site follows by itself.

**Nederlandse weekeditie** · Tuesday · `reports/<folder>/YYYY/`

| Report | Folder | Example file |
|---|---|---|
| De Enterprisearchitect | `de-enterprisearchitect` | `De_Enterprisearchitect_26_41.pdf` |
| De Businessarchitect | `de-businessarchitect` | `De_Businessarchitect_26_41.pdf` |
| De Dataarchitect | `de-dataarchitect` | `De_Dataarchitect_26_41.pdf` |
| De Integratiearchitect | `de-integratiearchitect` | `De_Integratiearchitect_26_41.pdf` |
| De Securityarchitect | `de-securityarchitect` | `De_Securityarchitect_26_41.pdf` |
| De Infrastructuurarchitect | `de-infrastructuurarchitect` | `De_Infrastructuurarchitect_26_41.pdf` |

**European weekly edition** · Thursday · `reports/<folder>/eu/YYYY/`

| Report | Folder | Example file |
|---|---|---|
| The Enterprise Architect | `the-enterprise-architect` | `The_Enterprise_Architect_26_41.pdf` |
| The Business Architect | `the-business-architect` | `The_Business_Architect_26_41.pdf` |
| The Data Architect | `the-data-architect` | `The_Data_Architect_26_41.pdf` |
| The Integration Architect | `the-integration-architect` | `The_Integration_Architect_26_41.pdf` |
| The Security Architect | `the-security-architect` | `The_Security_Architect_26_41.pdf` |
| The Infrastructure Architect | `the-infrastructure-architect` | `The_Infrastructure_Architect_26_41.pdf` |

**European Architecture Review** · last Friday of the month · `reports/european-architecture-review/YYYY/European_Architecture_Review_26_10.pdf`

Rules the build relies on:

- Folder names exactly as above: lower case with hyphens.
- The year is its own four digit folder (`2026/`, `2027/`).
- File names end in `_YY_WW.pdf` for weekly editions and `_YY_MM.pdf` for the monthly review.
- Upload all six reports of an edition in one commit, so the edition appears complete at once.
- Published editions are never overwritten.
- Essays, papers and AI prompts each have their own description in `build.py`; adding one there is a separate step.

`reports/sample/` holds early and example editions that precede the current structure or naming convention. They are kept as they were published and are not shown on the site.

### Editorial model

One shared factual ground is interpreted from multiple architecture responsibilities. Facts remain consistent while the impact, dependencies and decision relevance differ by perspective.

Only material developments from authoritative primary sources are selected. The reports are organisation independent and written for readers who need a clear view without a product inventory or solution design.

## Essays

A reflection or argument, developing a single thought.

| Essay | Version | Date |
|---|---|---|
| [Ambiguity Is the Attack Surface](./essays/ClaritasZ_Ambiguity_Is_the_Attack_Surface_v1_0.pdf) | 1.0 | September 2026 |

## Papers

Methodical and substantiated, with a structure or model as the result.

- [The Governance Chain](./papers/the-governance-chain.pdf) · Source → policy → principle → framework → guideline → measure. How decisions flow through an organisation.
- [Explicit Grounds](./papers/explicit-grounds.pdf) · Architecture practice in complex, changing environments.
- [A Grammar of Work](./papers/the-grammar-of-work.pdf) · A seven object grammar for describing services through explicit relations, owners and agreements.

## AI prompts

Freeware prompts and scripts for AI assistants, readable as text and usable as a tool. Each prompt states what it does, what it does not do and which assistant it was written for.

**Provenance Framework** makes architecture decisions traceable. Amendments capture what a document says; architecture decision records establish which observations are intentional decisions; documents are derived from both. The ZIP holds the complete documentation (`claritasz-complete-documentation.pdf`) and the database schema (`schema.pdf`). Free to use; support in Dutch or English at €200 per hour, excluding VAT.

| Prompt | Assistant | Version | Date |
|---|---|---|---|
| [Provenance Framework](./prompts/provenance-framework-v1.0.zip) | Copilot | 1.0 | July 2026 |

**ClaritasZ**  
Consistent in Design. Powered by Logic.
