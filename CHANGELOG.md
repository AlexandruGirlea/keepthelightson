# Changelog

Notable changes to this repository. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). The specification keeps its own
changelog inside [spec/SPECIFICATION.md](spec/SPECIFICATION.md#changelog); this file covers the
skills package, its bundled references and the project documentation.

## [Unreleased]

## [0.1.0] - 2026-09-10

### Added

- First release of the specification: 38 clauses in 7 sections, BCP 14 keywords, and an
  informative section on the legal position.
- Two agent skills, `klod` and `klod-check`, installable with APM.
- Independent versions for the skills package (`apm.yml`) and the specification (its header).
- Governance, the contribution guide, the RFC process and the code of conduct.
- Spec Kit extension for human takeover planning and implementation review.
- OpenSpec custom schema with a project-preserving installer and verification handover.
- Self-contained integration archives generated from the canonical KLOD skills.
- Public integration tests and shared GitHub/website setup instructions.

### Changed

- Simplified the README, guides and skill instructions.
- Added project, Git origin, model and timestamp fields to skill-generated reports.
- Added an independent AI off switch and human takeover as the sixth design principle.
- Strengthened implementation guidance and evidence gates.
- Bundled all required references and helpers with each skill.
- Added a standalone package check and synchronisation command using Python's standard library.
