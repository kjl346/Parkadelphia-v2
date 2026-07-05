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
- If the input is a full address, split and store the leading house number separately before normalizing the street name.
- Convert street names to uppercase.
- Trim leading/trailing whitespace.
- Collapse repeated internal whitespace.
- Remove punctuation that does not affect street identity.
- Normalize leading direction tokens using a predefined mapping, e.g.:
  - `NORTH` -> `N`
  - `SOUTH` -> `S`
  - `EAST` -> `E`
  - `WEST` -> `W`
- Normalize numbered street-name tokens to ordinals only after the house number has been removed, e.g.:
  - `42 STREET` -> `42ND ST`
  - `13 STREET` -> `13TH ST`
  - `1 STREET` -> `1ST ST`
- Normalize only the final street suffix token using a predefined mapping, e.g.:
  - `STREET` -> `ST`
  - `AVENUE` -> `AVE`
  - `ROAD` -> `RD`
  - `COURT` -> `CT`
- Do not apply ordinal suffixes to the house number.

Examples:
- `Market Street` -> `MARKET ST`
- `market st.` -> `MARKET ST`
- `S 13th Street` -> `S 13TH ST`
- `143 North 42 Street` -> house number `143`, street `N 42ND ST`
- `Avenue of the Republic` -> `AVENUE OF THE REPUBLIC`

## Why
- Provides a stable key for joins between user input, street graph edges, meters, and other datasets.
- Reduces duplicate street representations such as `MARKET STREET`, `Market St`, and `MARKET ST`.
- Keeps canonical street names readable while matching the abbreviated form commonly used in source data.


## Alternatives Considered
- Store entire suffixes
  - Unnecessary extra storage and more duplicate street representations.

## Consequences
- Need to ensure all user queries are normalized using the same procedure.
- Need a robust list of potential suffix mappings.
- Need to split house numbers before normalizing street-name ordinals.
