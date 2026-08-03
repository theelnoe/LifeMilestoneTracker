# Life Milestone Tracker

# Architecture

Version: 1.0

Status: Frozen

Author: Elnoe

Last Updated: 2026-07-23

---

# Purpose

This document describes the architectural principles of the Life Milestone Tracker project.

It explains **why** the system is designed in its current form.

Implementation details, database schema, API specifications and future plans are documented in separate files.

---

# Architectural Philosophy

The architecture follows one simple principle:

> The architecture should always be proportional to the size and complexity of the project.

The goal is to build a system that is:

- simple
- maintainable
- extensible
- easy to understand

Complexity should never be introduced before it becomes necessary.

Over-engineering is intentionally avoided.

---

# Separation of Concerns

Each layer of the application has a single responsibility.

Business logic must remain independent from:

- storage engine
- user interface
- deployment platform

Changing one layer should have minimal impact on the others.

---

# Storage Independence

The logical data model is independent from the storage engine.

The current implementation uses JSON only as a storage format.

Future storage engines may include:

- SQLite
- PostgreSQL

The choice of storage engine is considered an implementation detail rather than an architectural decision.

Changing the storage engine must not require rewriting the business logic.

---

# Design Principles

The following principles apply throughout the project.

1. Keep the design simple.

2. Avoid duplicated information.

3. Store only business data.

4. Derive presentation data when needed.

5. Separate business logic from presentation.

6. Prefer readability over clever solutions.

7. Optimize only when necessary.

8. Major design decisions must be documented before implementation changes.

---

# Non-Goals

The project intentionally avoids:

- unnecessary abstractions
- premature optimization
- storage-specific business logic
- UI-specific database design
- unnecessary framework complexity

These decisions are intentional and may be revisited only when real requirements justify them.

---

# Architecture Decision Records (ADR)

This section records architectural decisions that have been explicitly accepted during the design process.

Each decision receives a permanent identifier.

Architecture decisions are never deleted.

If a decision changes in the future, a new ADR is created instead of modifying the original one.

---

## ADR-001

### Title

POST requests must receive data through JSON request bodies.

### Status

Accepted

### Date

2026-07-24

### Decision

All POST requests must receive business data exclusively through the JSON request body.

Query string parameters are prohibited for POST requests.

GET requests may use URL path parameters or query parameters.

### Rationale

Using JSON request bodies provides:

- consistent API design
- easier validation
- easier documentation
- cleaner backend implementation
- easier migration to REST APIs

### Consequences

Future API endpoints must follow this convention.

Existing endpoints that violate this rule must be refactored before Version 1.0 is finalized.

---

# Source Code Architecture

Version 1.0 focuses on stability and correctness.

The current implementation may contain multiple responsibilities in app.py.

Current implementation keeps route handlers inside app.py.

Business logic is progressively being moved to project_service.py.

Code separation is a future refactoring goal and is not required for Version 1.0.

Architecture improvements must not compromise a working system.

---

## route.py

Current implementation

Route handlers are located in app.py.

Future refactor

routes.py will contain all HTTP route handlers.

---

## app.py

Role

UI Layer

Responsibilities

- Receive HTTP requests
- Validate input
- Call Domain Services
- Return HTTP responses

Must NOT contain

- Business Logic
- Repository Logic
- Utility Logic

---

## project_service.py

Role

Domain Service Layer

Responsibilities

- Project business rules
- Session registration
- History management
- Statistics calculation
- Milestone generation

This module may call:

- repository.py
- utils.py

---

## repository.py

Role

Persistence Layer

Responsibilities

- Read data
- Write data
- Verify storage existence

This module must remain independent from project business rules.

---

## utils.py

Role

Utility Layer

Responsibilities

- Pure utility functions
- Formatting
- Time calculations

Utility functions must not depend on:

- Flask
- Repository
- Project
- Storage Engine

Some utility functions are currently implemented inside project_service.py.

They may be moved to utils.py during future refactoring.

---

## Removed Modules

The following module is intentionally removed from Version 1.0

- timer.py

Reason

Its responsibilities are not yet sufficiently independent to justify a separate module.

It may be introduced in a future version if real requirements emerge.

---

# Future Target Architecture

The allowed dependency flow is

app.py

↓

app.py

↓

project_service.py

↓

repository.py

Utility functions may be used by every layer.

Lower layers must never depend on higher layers.

---

# Architectural Rule

Every function belongs to exactly one module.

Duplicating business logic across multiple modules is prohibited.

Any future module split must first be documented before implementation.

---

# References

Related documents

- 02_database_schema.md
- 03_data_model.md
- 04_api.md
- 06_changelog.md
- 07_roadmap.md