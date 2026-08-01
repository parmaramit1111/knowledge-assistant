# Engineering Decisions

## Decision 001

### CQRS

Reason

Separate reads from writes to simplify business logic.

Alternatives

- CRUD Service

Decision

Use CQRS.

---

## Decision 002

### Repository Pattern

Reason

Keep persistence isolated.

---

## Decision 003

### Ambient Transactions

Reason

Avoid passing AsyncSession everywhere.

---

## Decision 004

### ContextVar

Reason

Provides request-scoped transaction context.

---

## Decision 005

### Provider Architecture

Reason

Support multiple AI providers.

---

## Decision 006

### Response Wrapper

Reason

Consistent API contract.

---

## Decision 007

### UUID

Reason

Distributed systems.

---

## Decision 008

### Async SQLAlchemy

Reason

Better scalability.

---

## Decision 009

### Service Factory

Reason

Centralized dependency creation.

---

## Decision 010

### Repository Factory

Reason

Centralized repository creation using the current transaction context.
