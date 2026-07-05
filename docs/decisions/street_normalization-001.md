# ADR-001: Normalize Street Naming

## Status
In Progress

## Date
2026-07-05

## Context
The application needs to store street names in an efficient manner for later joining and retrieval of user query.

## Decision
Street names will be stored and queried using a canonical normalized form.

Normalization will:
- Convert street names to uppercase.
- Trim leading/trailing whitespace.
- Collapse repeated internal whitespace.
- Remove punctuation that does not affect street identity.
- Normalize only the final street suffix token using a predefined mapping, e.g.:
  - `STREET` -> `ST`
  - `AVENUE` -> `AVE`
  - `ROAD` -> `RD`
  - `COURT` -> `CT`

Examples:
- `Market Street` -> `MARKET ST`
- `market st.` -> `MARKET ST`
- `S 13th Street` -> `S 13TH ST`
- `Avenue of the Republic` -> `AVENUE OF THE REPUBLIC`

## Why
- Provides a stable key for joins between user input, street graph edges, meters, and other datasets.
- Reduces duplicate street representations such as `MARKET STREET`, `Market St`, and `MARKET ST`.
- Keeps canonical street names readable while matching the abbreviated form commonly used in source data.


## Alternatives Considered
- Store entire suffixes
  - Unncessarry extra storages

## Consequences
- Need to ensure all User Queries are normalized using the same procedure
- Need a Robust list of potential suffix mappings