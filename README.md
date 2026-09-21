# SURAYA AI

Private Personal AI Operating System

Version: 0.2.0

---

## 1. SYSTEM

SURAYA AI is a private, modular, extensible personal AI system.

Main hierarchy:

Creator
↓
Brain
↓
Guardian
↓
Executor
↓
Tools

Guardian has control over Executor.

---

## 2. CORE COMPONENTS

### Creator

The Creator is the owner and highest authority of the system.

The Creator can:

- send commands
- approve sensitive operations
- stop execution
- restart execution
- inspect reports
- inspect audit records
- configure system policies
- connect external services

---

### Brain

Brain is responsible for:

- understanding commands
- identifying goals
- creating plans
- using memory
- selecting tools
- preparing actions

Brain does not directly execute dangerous operations.

---

### Guardian

Guardian is the independent inspection and control layer.

Guardian checks:

- commands
- plans
- actions
- permissions
- risk
- execution
- results

Guardian can:

- allow
- block
- request Creator approval
- stop execution
- verify results

Guardian must not weaken its own security policies.

---

### Executor

Executor performs approved actions.

Executor cannot bypass Guardian.

Executor can use registered tools.

---

### Tools

Tools are modular capabilities.

Examples:

- browser
- filesystem
- code execution
- Git
- GitHub
- cloud storage
- research
- image generation
- audio
- video
- social media
- financial APIs

---

## 3. MEMORY

Current memory:

SQLite

Planned memory:

- short-term memory
- long-term memory
- semantic memory
- vector memory
- knowledge graph
- experience memory
- project memory
- cloud memory

---

## 4. MODEL ROUTER

SURAYA does not depend on one AI model.

Models are connected through:

core/models/router.py

This allows future integration of:

- local models
- private models
- cloud models
- multiple AI providers
- specialized models

The Core should remain independent from any specific provider.

---

## 5. CLOUD STORAGE

SURAYA supports a provider-independent cloud storage architecture.

Planned providers:

- Google Drive
- Microsoft OneDrive
- Dropbox
- Amazon S3
- S3-compatible storage
- Cloudflare R2
- private server
- NAS
- self-hosted storage

Cloud storage documentation:

docs/CLOUD_STORAGE.md

---

## 6. AUDIT

SURAYA records important system events.

Audit events include:

- Creator commands
- Brain plans
- Guardian decisions
- Executor actions
- execution errors
- verification
- final reports

Current storage:

data/audit.jsonl

---

## 7. API

### Health

GET

```text
/health
