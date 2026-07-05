# Assumptions

## Address Parsing And Street Normalization

- The first token in a full address is assumed to be the house number and is stored separately from the street name.
- If the second token is a direction, it is normalized using the direction mapping, e.g.:
  - `NORTH` -> `N`
  - `SOUTH` -> `S`
  - `EAST` -> `E`
  - `WEST` -> `W`
- If the second-to-last token in the street portion is a number, ordinality is applied to that token, e.g.:
  - `42 STREET` -> `42ND ST`
  - `13 STREET` -> `13TH ST`
  - `1 STREET` -> `1ST ST`
- The last token in the street portion is treated as the street suffix and normalized using the street suffix mapping, e.g.:
  - `STREET` -> `ST`
  - `AVENUE` -> `AVE`
  - `ROAD` -> `RD`
  - `COURT` -> `CT`

Example:

- `143 North 42 Street` -> house number `143`, street `N 42ND ST`
