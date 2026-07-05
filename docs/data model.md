# Data Model

## Normalization Decisions

### How Streets Are Normalized
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