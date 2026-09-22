# SURAYA AI Integration

## Backend

The Android application communicates with:

- GET /health
- GET /status
- POST /command

## Development Android Connection

Android Emulator:

http://10.0.2.2:8000

Physical Android device:

Use the development machine's local network address.

## Production

Production must use:

- HTTPS
- authenticated API requests
- device/session authentication
- encrypted credentials
- Guardian-controlled sensitive operations

## Architecture

Android Creator Console
        ↓
Authenticated API
        ↓
SURAYA Runtime
        ↓
Brain
        ↓
Guardian
        ↓
Executor
        ↓
Tools
