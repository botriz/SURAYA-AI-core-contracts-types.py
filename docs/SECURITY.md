# SURAYA AI Security Model

## Principles

1. Least privilege.
2. Explicit permissions.
3. Guardian-controlled execution.
4. Auditability.
5. Secret isolation.
6. Safe file handling.
7. Human approval for sensitive actions.
8. Emergency stop.
9. No credential harvesting.
10. No permission bypass.

## Sensitive Capabilities

The following capabilities require additional controls:

- financial transactions
- publishing to external accounts
- deleting important data
- credential access
- external account changes
- arbitrary code execution
- irreversible cloud operations

## Secret Handling

Production credentials must not be committed to Git.

They should be stored in a protected secret system appropriate to the deployment environment.

## Emergency Stop

The Creator must be able to stop execution independently of ordinary task flow.

## Guardian

The Guardian must remain outside the Executor's authority.

An Executor must never be able to:

- disable Guardian policy
- modify its own permissions
- approve its own sensitive actions
- erase its own audit history
