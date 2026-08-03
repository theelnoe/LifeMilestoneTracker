# Life Milestone Tracker

# Internal API Design Proposal

Version: 1.0

Status: Draft

Author: Elnoe

Last Updated: 2026-07-23

---

# Purpose

This document defines the internal API of the application.

The goal is to specify how different layers of the application communicate with each other.

This document describes function contracts rather than HTTP endpoints.

---

# API Design Principles

The internal API follows these principles:

- Clear input parameters
- Predictable outputs
- No hidden side effects
- Layer independence
- Storage independence

Every public function should have a documented contract.

---

# Layer Communication

The current implementation is a monolithic Flask application.

Future refactoring may introduce separate layers such as:

- Route layer
- Service layer
- Repository layer

These layers are design goals and are not required for Version 1.0.

---

# Function Contracts

---

## generate_milestones()

Layer

Domain Service

Purpose

Generate milestone values for a project goal.

Input

| Parameter | Type | Description |
|-----------|------|-------------|
| goal | Number | Final project goal |

Output

| Type | Description |
|------|-------------|
| List<Number> | Generated milestone values |

Side Effects

- None

---
## get_projects()
Layer

Domain Service

Purpose

Return all available projects.

Input

None

Output

List<Project>

Side Effects

None

## get_project()
Layer

Domain Service

Purpose

Return a project by index.

Input

project_index | Integer

Output

Project object

Side Effects

None

## get_project_view()
Layer

Domain Service

Purpose

Prepare complete project dashboard data.

Input

project_index | Integer

Output

Object containing:

- project information
- total progress
- today progress
- week progress
- milestones
- next milestone

Side Effects

None

## create_project()
Layer

Domain Service

Purpose

Create a new project.

Input

name | String

goal | Number

domain_id | Integer

unit_id | Integer

Output

Created project

Side Effects

Updates storage

## update_project()
Layer

Domain Service

Purpose

Update project information.

Input

project_id | Integer

name | String

goal | Number

domain_id | Integer

unit_id | Integer

Output

Updated project

Side Effects

Updates storage

## delete_project()
Layer

Domain Service

Purpose

Delete a project.

Input

project_id | Integer

Output

None

Side Effects

Updates storage

## create_session()
Layer

Domain Service

Purpose

Create a completed session.

Input

project_id | Integer

value | Integer

For time projects:
value represents minutes.

Output

Created session

Side Effects

Updates storage

## update_session()
Layer

Domain Service

Purpose

Update session progress value.

Input

session_id | Integer

value | Integer

Output

None

Side Effects

Updates storage

## delete_session()
Layer

Domain Service

Purpose

Delete a session.

Input

session_id | Integer

Output

None

Side Effects

Updates storage

## finish_timer()
Layer

Domain Service

Purpose

Convert a running timer into a completed session.

Input

start_time | DateTime

project_id | Integer

Output

Created session

Side Effects

Updates storage

# Repository API

The repository layer currently provides:

- exists()
- load()
- save()

These functions are storage-engine dependent.

Business logic must never access the storage engine directly.

---

# Future Expansion

When REST endpoints are introduced, this document will be extended to include:

- HTTP Method
- URL
- Request Schema
- Response Schema
- Error Codes

The current document only specifies the internal API.