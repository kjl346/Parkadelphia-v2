# Data Model

## Normalization Decisions

### How Streets Are Normalized
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
