# Design Decisions

## DD-001

Title: Version 1.0 is a single-user application

Status: Approved

Decision

Version 1.0 supports a single user only.

The database contains exactly one user record.

Future versions may support multiple users without changing the logical model.

## DD-002

Title: User_ID

Status: Approved

Decision

The only user in Version 1.0 has User_ID = 1.

All projects belong to this user.

## DD-003

Title: User entity

Status: Approved

Decision

The User entity contains the following fields:

- User_ID
- Name

No additional user attributes are included in Version 1.0.

## DD-004

Title: Project and Activity relationship

Status: Approved

Decision

A Project may contain sessions belonging to multiple activities.

Each Session references one DomainActivity.

Activities are not assigned directly to a Project.

## DD-005

Title: Domain management

Status: Approved

Decision

Domains are predefined in Version 1.0.

Users cannot create or delete domains.

Domain names may be renamed if necessary.

## DD-006

Title: Activity management

Status: Approved

Decision

Activities are predefined in Version 1.0.

Users cannot create or delete activities.

Activity names may be renamed if necessary.

Sessions reference Activity through DomainActivity, therefore renaming an activity automatically affects the display of historical sessions.

## DD-007

Title: DomainActivity defines valid Domain-Activity combinations

Status: Approved

Decision

DomainActivity defines all valid combinations of Domain and Activity.

A Session must reference an existing DomainActivity.

Users cannot create or delete DomainActivity records in Version 1.0.

If a Domain-Activity combination does not exist, it cannot be selected when recording a session.

## DD-008

Title: Project measurement unit

Status: Approved

Decision

Each Project is associated with exactly one Unit.

The Unit defines how the project's goal is measured (e.g. Hours, Books, Articles, Problems).

Users cannot create or delete Units in Version 1.0.

## DD-009

Title: Project determines the available activities

Status: Approved

Decision

Each Project belongs to exactly one Domain.

When recording a Session, only the Activities associated with the Project's Domain (through DomainActivity) may be selected.

Activities from other Domains are not available for that Project.

## DD-010

Title: Unit defines the measurement strategy

Status: Approved

Decision

Each Unit defines how a project's progress is measured.

Version 1.0 supports two measurement types:

- Time
- Count

Time-based projects record progress using session duration.

Count-based projects record progress using completed quantities.

The user interface may present different controls depending on the project's measurement type.

## DD-011

Title: Quantities are numeric

Status: Approved

Decision

All measurable values (such as project goals and recorded quantities) are represented as numeric values.

The logical data model does not distinguish between integer and fractional quantities.

This allows future support for measurements such as weight, distance, money, and other continuous units.


## DD-012

Title: Milestones and achievements are derived

Status: Approved

Decision

Milestones are generated from the project's goal and are not stored.

Achievements are derived from the current progress.

If the current progress falls below a previously reached milestone, the achievement is considered lost.

Neither milestones nor achievements are persisted in the database.

## DD-013

Title: Session records project progress

Status: Approved

Decision

Each Session belongs to one Project and references one DomainActivity.

For each Session, exactly one progress value is recorded:

- Duration for time-based projects.
- Quantity for count-based projects.

Duration and Quantity are mutually exclusive.

The Activity is selected by the user when the Session is recorded.

## DD-014

Title: Session workflow depends on the project measurement type

Status: Approved

Decision

Time-based projects support timer-based and manual time registration.

Count-based projects do not record intermediate progress.

A Session is created only when a measurable unit of work has been completed (e.g. one book, one article, multiple solved problems).

## DD-015

Title: Time measurements are stored in minutes

Status: Approved

Decision

Session.Value stores the progress value of a session.

For time-based projects, Value is stored as an integer number of minutes.

For all other measurement types, Value is stored using the project's unit and may be a floating-point number.

Rationale

Storing time in minutes avoids floating-point precision errors and simplifies time calculations while keeping the data model flexible for other measurement units.

## DD-016

Title
Temporary DomainActivity assignment

Status
Approved

Decision

The DomainActivity entity is fully defined in Version 1.0.

However, activity selection is not yet implemented in the user interface.

Until activity selection is available, newly created sessions temporarily store DomainActivity_ID = 0.

This temporary value will be replaced by a valid DomainActivity identifier when activity selection is implemented.