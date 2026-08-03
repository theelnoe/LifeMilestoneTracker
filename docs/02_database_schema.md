# Life Milestone Tracker

# Database Schema

Version: 1.0

Status: Design Approved

Author: Elnoe

Last Updated: 2026-07-23

---

# Purpose

This document defines the logical database model of the Life Milestone Tracker project.

The goal is to describe the entities, relationships, business rules, and normalization decisions independently of the storage engine.

This document is the primary reference for future development.

---

# Database Design Philosophy

The database is intentionally designed using a normalized relational model, even though the current storage engine is JSON.

The storage engine is considered an implementation detail.

The logical model must remain independent from the storage technology.

### Design Goals

- Avoid duplicated data
- Preserve data consistency
- Simplify reporting
- Support future scalability
- Support future migration to relational databases
- Keep business logic independent from the storage engine

---

# Current Storage Engine

Current

- JSON

Future options

- SQLite
- PostgreSQL

The application business logic must not depend on the storage engine.

---

# Application User Model

The current version is designed as a single-user application.

The User entity exists for structural consistency and future extensibility.

Version 1.0 contains one user record only.

The current primary user is represented by User_ID = 1.

---

# Entities

Current entities

- User
- Project
- Unit
- Domain
- Activity
- DomainActivity
- Session

---

# Entity Dependency

Current dependency order

User
    ↓
Project
    ↓
Session

Domain
    ↓
DomainActivity
    ↓
Session

Activity
    ↓
DomainActivity

Unit
    ↓
Project

---

# Entity Status

| Entity | Status |
|---------|---------|
| User | Draft |
| Project | Frozen |
| Unit | Frozen |
| Domain | Frozen |
| Activity | Frozen |
| DomainActivity | Frozen |
| Session | Frozen |
| GoalProfile | Removed |

---

# Design Principles

The following principles apply to every entity in this database.

1. No duplicated information is stored.

2. Derived values are never stored.

3. Every stored attribute must have a real business purpose.

4. Presentation-layer information does not belong to the database.

5. Soft Delete is preferred over physical deletion whenever historical information must be preserved.

6. Every design decision must be documented before implementation.

7. Design decisions should be documented before major implementation changes.

8. Derived values may be stored only when their maintenance cost is lower than their recalculation cost.

---

# Session

Status: Frozen

---

## Purpose

A Session represents a single completed work period performed by the user.

Examples:

- Reading an English lesson
- Listening practice
- Writing a research paper
- Programming
- Exercising

Every measurable progress in the system is recorded as a Session.

---

## Stored Fields

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| Session_ID | Integer | Yes | Primary Key |
| Project_ID | Integer | Yes | Foreign Key → Project |
| DomainActivity_ID | Integer | Yes | Foreign Key → DomainActivity |
| StartTime | DateTime | Yes | Session start date and time |
| Value | Integer | Yes | Duration in minutes |
| Material | Text | No | Learning resource or material |
| Notes | Markdown Text | No | User notes |

---

## Derived Fields (Not Stored)

Display

Reason:

Display is generated from Value when needed.

Examples:

25 → 25 m

60 → 1 h

90 → 1 h 30 m

135 → 2 h 15 m

---

## Relationships

Project

1 → N

Session

---

DomainActivity

1 → N

Session

---

## Business Rules

- Value must be greater than zero.
- Project is required.
- DomainActivity is required.
- Material is optional.
- Notes are optional.
- Sessions are never created with zero duration.

---

## Design Decisions

### Session_ID

Session_ID is an auto-increment integer.

Reasons:

- Simpler implementation
- Easier debugging
- Easier migration to relational databases

---

### StartTime

StartTime represents the beginning of the session.

EndTime is intentionally NOT stored.

Reason:

EndTime is calculated as

StartTime + Duration

---

### Value

Value is stored in minutes.

Reasons:

- Avoid floating-point precision problems.
- Simplify calculations.
- Easier reporting.
- Easier aggregation.

Examples:

25

45

90

135

---

### Material

Material is stored as plain text.

Reason:

The application should remain simple.

The user decides how to describe the study material.

Examples:

- Passages 1 Lesson 3
- Oxford Grammar Unit 12
- Research Paper XYZ

---

### Notes

Notes support Markdown formatting.

Reason:

Markdown provides rich formatting while remaining portable.

Supported examples:

- headings
- bullet lists
- emphasis
- links
- code blocks

Markdown syntax is stored as plain text.

Rendering is performed by the application layer.

The database stores only the raw Markdown content.

---

## Normalization Notes

User_ID is intentionally NOT stored.

Reason:

The user is inferred through the Project relationship.

Session

↓

Project

↓

User

---

Display is intentionally NOT stored.

Reason:

Display is derived from Duration.

Derived values must never be stored in the database.

---

# Domain

Status: Frozen

---

## Purpose

A Domain represents a major area of the user's life, work, or learning.

A Domain contains Projects and defines the primary context of those Projects.

Examples:

- English
- Research
- Programming
- Fitness
- Medium Publishing

---

## Stored Fields

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| Domain_ID | Integer | Yes | Primary Key |
| Name | Text | Yes | Domain name |
| Is_Active | Boolean | Yes | Soft Delete flag |

---

## Relationships

Domain

1 → N

DomainActivity

---

## Business Rules

- Domain names must be unique.
- Domain names are case-insensitive.
- Domains may be renamed if necessary.
- Domains are never physically deleted.
- Domains can be deactivated.
- Existing sessions must never be deleted because a domain is removed.

---

## Design Decisions

### Name

Domain names are intentionally simple.

Examples:

- English
- Research
- Programming

Descriptions are intentionally NOT stored.

Reason:

The purpose of a domain should be obvious from its name.

Additional explanations belong to project documentation rather than the database.

---

### Is_Active

Soft Delete is used.

Domains are never physically deleted.

Reason:

Historical study sessions must always remain valid.

---

## Normalization Notes

Activities are NOT stored inside Domain.

Activities are connected through DomainActivity.

Reason:

This avoids duplicated activity definitions.

---

Presentation information is intentionally NOT stored.

Examples:

- Display order
- Icons
- Colors

Reason:

Presentation belongs to the UI layer rather than the database model.