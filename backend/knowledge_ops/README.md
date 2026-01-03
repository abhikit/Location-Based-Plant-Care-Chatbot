# Knowledge Ops Layer

This module manages the lifecycle of knowledge improvement.

## Guarantees
- No automatic knowledge updates
- No hallucinated enrichment
- Human approval required

## Lifecycle
DETECTED → PROPOSED → UNDER_REVIEW → APPROVED / REJECTED → ARCHIVED

## Ownership
- Agents can DETECT and PROPOSE
- Humans APPROVE
- KB writes are manual and versioned