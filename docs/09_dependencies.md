# Life Milestone Tracker

# Dependencies

Version: 1.0

Status: Frozen

Author: Elnoe

Last Updated: 2026-07-23

---

# Purpose

This document records the dependencies between modules and functions.

Its purpose is to support safe refactoring by making the impact of changes visible.

---

# Dependency Types

The project distinguishes three dependency categories.

## 1. Function Dependency

A function calls another function.

## 2. Module Dependency

A module imports another module.

## 3. External Dependency

A function depends on an external library or framework.

Examples:

- Flask
- datetime
- json
- os

---

# Current Function Dependencies

## create_session()

Calls

- repository.load()
- repository.save()


Purpose

Creates a new session record.

---

## get_project_view()

Calls

- get_project()
- calculate_total()
- calculate_today()
- calculate_week()
- generate_milestones()
- calculate_progress()
- get_next_milestone()

Side Effects

None

---

## get_project()

Calls

- load()

---

## get_project_history()

Purpose

Returns project session history.

Calls

- format_minutes()

Side Effects

None

---

## calculate_total()

Purpose

Calculate total progress of a project.

Calls

None

Side Effects

None


## calculate_today()

Purpose

Calculate today's project progress.

Calls

None

Side Effects

None


## calculate_week()

Purpose

Calculate weekly project progress.

Calls

None

Side Effects

None

---

## generate_milestones()

Uses

- None

---

## calculate_elapsed_minutes()

No dependencies

---

## format_minutes()

No dependencies

---

# Current Module Dependencies

app.py

↓

project_service.py

↓

utils.py

---

app.py

↓

repository.py

---

# External Dependencies

| Module | External Dependency |
|--------|----------------------|
| app.py | Flask |
| repository.py | json, os |
| project_service.py | datetime |
| utils.py | None |

---

# Design Rule

Dependencies must always point downward.

UI

↓

Application

↓

Domain

↓

Persistence

Utility functions may be called from every layer.

Lower layers must never depend on higher layers.