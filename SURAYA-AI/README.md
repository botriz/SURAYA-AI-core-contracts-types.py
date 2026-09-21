# SURAYA AI

Private Personal AI Operating System.

## Architecture

Creator
↓
Core Brain
↓
Guardian
↓
Executor
↓
Tools

## Core Components

- Creator Interface
- Brain
- Planner
- Guardian
- Executor
- Model Router
- Memory
- Tool Registry
- Audit
- Cloud Storage
- Future Plugin System

## Guardian

Guardian controls:

- instruction verification
- plan verification
- permission control
- risk control
- execution monitoring
- result verification
- blocking
- approval
- future rollback

## Model Independence

SURAYA does not depend on one AI provider.

Models are connected through ModelRouter.

## Memory

Initial memory uses SQLite.

Future memory layers:

- Long Term Memory
- Vector Memory
- Knowledge Graph
- Experience Memory
- Cloud Memory

## Cloud

Cloud storage uses provider adapters.

Planned providers:

- Google Drive
- OneDrive
- Dropbox
- S3
- S3 Compatible
- Private Storage

## Backend

Install:

```bash
pip install -r backend/requirements.txt
