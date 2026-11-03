# Issue tracker configuration

- **Canonical tracker:** GitHub Issues in ClippyFirst/Lao-Ukrainian-Phonetic-System.
- **Current integration:** use the connected GitHub repository integration when available. Do not assume a local gh CLI is installed or authenticated.
- **Pull requests as intake:** disabled. PRs are delivery/review objects; issues remain the canonical request, blocker and research-decision records.
- **Status vocabulary:** DONE_VERIFIED, PARTIAL, TODO, BLOCKED, DEFERRED, as defined by AGENTS.md and the master handoff.
- **Triage labels:** do not create a second label vocabulary. Inspect the repository's existing labels before any label mutation; if no suitable label exists, leave labels unchanged and record status in the issue body.
- **Issue discipline:** search for an existing issue before creating one; link the originating issue from implementation PRs; distinguish verified evidence, project decisions, hypotheses and external blockers.
- **Authorship:** do not present agent-generated issue or PR prose as owner-authored. Preserve any human-authored template sections.
- **Research issues:** include source URL, exact source locator/version, profile, data provenance, license state and acceptance criteria. A source-attested comparator is not independent gold.
