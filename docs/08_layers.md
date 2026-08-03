# Life Milestone Tracker

# Layers

Version: 1.0

Status: Draft

Author: Elnoe

Last Updated: 2026-07-23

---

# Purpose

This document defines the architectural layer of every major function in the project.

It serves as the primary reference during refactoring.

---

# Layers

## UI Layer

Responsible for:

- HTTP Requests
- HTTP Responses
- Rendering Templates
- API Endpoints

Current Files:
- Flask application entry point

Future Refactor:
- routes.py

---

## Application Layer

Responsible for:

- Coordinating business operations
- Calling services
- Communicating with Repository

(Currently inside app.py)

---

## Domain Layer

Responsible for:

- Business Rules
- Progress Calculation
- Milestone Logic
- History Management

Files

- project_service.py

---

## Utility Layer

Responsible for:

- Pure Functions
- Formatting
- Date/Time Utilities
- Independent Calculations

Files

- utils.py

---

## Persistence Layer

Responsible for:

- Reading Data
- Writing Data
- Storage Engine

Files

- repository.py

---

# Current Function Classification

| Function | Target Layer |
|----------|--------------|
| format_minutes | Utility |
| generate_milestones | Domain |
| get_project | Domain |
| get_project_view | Domain |
| calculate_total | Domain |
| calculate_today | Domain |
| calculate_week | Domain |
| calculate_progress | Domain |
| get_next_milestone | Domain |
| create_project | Domain |
| update_project | Domain |
| delete_project | Domain |
| create_session | Domain |
| update_session | Domain |
| delete_session | Domain |
| finish_timer | Domain |
| repository.load | Persistence |
| repository.save | Persistence |
| Flask Routes | UI |

---

# Design Rule

A higher layer may call lower layers.

A lower layer must never call a higher layer.

Example

UI

↓

Application

↓

Domain

↓

Persistence

Utility functions may be used by any layer.