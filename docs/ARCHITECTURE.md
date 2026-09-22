# SURAYA AI Architecture

## Authority

Creator
  ↓
Brain
  ↓
Guardian
  ↓
Executor
  ↓
Tools

## Core Components

### Creator Console

The Android application used by the Creator.

### Brain

Responsible for:

- understanding
- intent detection
- planning
- model interaction
- task decomposition

### Guardian

Independent control layer.

Responsible for:

- policy
- risk
- permissions
- approvals
- verification
- emergency stop

### Executor

Performs only authorized actions.

### Tools

Capabilities are isolated into modules.

Examples:

- code
- browser
- Git
- research
- media
- social
- cloud
- finance

### Memory

Stores durable information and session context.

### Cloud

Provides provider-independent storage.

### Audit

Records important system decisions and operations.

## Design Principle

Adding a new capability must not create a path around Guardian controls.
