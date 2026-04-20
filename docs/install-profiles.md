# Installation Profiles

Brain OS is easier to adopt when installed in layers.

This file defines the recommended profiles for both humans and AI agents.

---

## Principle

> Start with the smallest setup that gives the user a real success.

Do not default users into the full system unless they explicitly ask for it.

---

## Profile 1: Minimal

Best for:
- first-time users
- users who mainly want a personal knowledge system
- users evaluating whether Brain OS fits them
- AI agents doing first-pass setup

### Includes
- `vault-template/`
- `scripts/config.env`
- a small core skill set
- basic verification

### Recommended skill set
- `skills/brain-os-installer/`
- `skills/article-notes-integration/`

Optional:
- `skills/personal-ops-driver/` only if the user asked for planning / todos

### Does not include by default
- Observer
- CI/CD protection
- conversation-mining
- QMD setup
- full nightly pipeline
- full recommended skills set

### Success definition
- vault created
- config written
- core skills installed
- one script or one small workflow works

---

## Profile 2: Standard

Best for:
- users ready to actually run Brain OS day to day
- users who want both knowledge and personal ops
- users willing to set up OpenClaw cron soon

### Includes
- everything in Minimal
- core knowledge workflows
- personal ops workflows
- selected cron examples

### Recommended skill set
- `skills/article-notes-integration/`
- `skills/personal-ops-driver/`
- `skills/conversation-knowledge-flywheel/`
- `skills/knowledge-flywheel-amplifier/`

### Typical docs to read next
- `docs/component-guide.md`
- `docs/getting-started.md`
- `docs/personal-ops.md`
- `docs/agents.md`

### Success definition
- minimal setup works
- at least one recurring workflow is enabled
- the user understands the daily loop

---

## Profile 3: Advanced

Best for:
- users who explicitly want the full operating system
- multi-agent setups
- users who want ongoing automation, governance, and iteration

### Includes
- everything in Standard
- nightly pipeline
- Observer
- optional CI/CD and governance workflow
- additional integrations and deeper operating docs

### Typical docs to read next
- `docs/agents.md`
- `docs/architecture.md`
- `docs/nightly-pipeline-guide.md`
- `docs/agent-playbooks/observer-playbook.md`
- `docs/agent-playbooks/release-playbook.md`

### Success definition
- standard setup works
- advanced modules are enabled intentionally
- user understands operational boundaries and maintenance costs

---

## Recommended default

If the user has not clearly asked for the full system:

> Choose **Minimal** first.

Brain OS grows better by layering than by overwhelming the user on day one.
