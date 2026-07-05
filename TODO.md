## In Progress

 - [ ] Add block metadata to street graph edges
  - **Relevant code:** `Parkadelphia v2/src/graph.py`, `Parkadelphia v2/src/data/load_data.py`, `Parkadelphia v2/src/user_facing/user_interaction.py`
  - **Notes:**
    - Store the street block / hundred-block on each `Edge`.
    - Load block values from street centerline fields such as `l_hundred` / `r_hundred`.
    - Preserve side-specific block metadata where possible.
    - Use block metadata to match parking meters and user-entered addresses to candidate street edges.
  - **Acceptance criteria:**
    - Each edge exposes block metadata.
    - Querying by normalized street + address number can narrow results to the correct block.
    - Meter records can be associated with street/block candidates.   


---

## Blockers
- [ ] Waiting to implement the street name standardization logic and documenting how street names are stored

---

## Backlog

### High Priority
- [ ] Implement way to standardize different street queries
  - **Relevant code:** `Parkadelphia v2/src/data/preprocess.py`,`Parkadelphia v2/src/user_facing/user_interaction.py`
  - **Notes:** 
    - Need to have an efficient way to decode user entry into a standardized format
    - Should be resilient to ave , road being shortcutted
    - May need to make a robust list first and then refine 
    - May need a regex extract address of user query
  - **Next Step:**
    - Have an LLM call to extract address of problematic user queries
  - **Comments:**
    - Need to first standardize 

- [ ] Implement way to join meter metadata onto different blocks
  - **Relevant code:** `Parkadelphia v2/src/data/load_data.py`, `Parkadelphia v2/src/data/preprocess.py`, `Parkadelphia v2/src/graph.py`
  - **Goal:**
    - Associate each parking meter/kiosk record with the most likely street graph edge/block.
  - **Notes:**
    - Meter data has `street`, `block_limits`, and `side`.
    - Street graph edges have normalized `stname`, `f_block`, and `t_block`.
    - Need to normalize meter street names using the same street normalization rules used for graph edges.
    - Need to decide whether `block_limits` should match `f_block`, `t_block`, or a derived edge address range.
    - Side-specific matching may matter because meters are listed by side (`E`, `W`, etc.) and street centerline ranges are left/right.
  - **Proposed subtasks:**
    - [ ] Add meter preprocessing function that normalizes `meters.street`.
    - [ ] Standardize meter block values to numeric block/range fields.
    - [ ] Add a graph edge export method or helper that returns edges as a DataFrame with `edge`, `stname`, `f_block`, `t_block`, and node/intersection metadata.
    - [ ] Join meters to edge candidates by normalized street name.
    - [ ] Filter candidates by block/address range compatibility.
    - [ ] Add side-aware filtering if the left/right metadata is reliable enough.
    - [ ] Decide how to handle multiple candidate edges for one meter.
    - [ ] Decide how to handle meters that do not match any edge.
    - [ ] Store matched meter records on the corresponding edge or in a separate `meter_index`.
  - **Acceptance criteria:**
    - Meters can be joined to candidate graph edges using normalized street + block.
    - The join produces counts for matched, unmatched, and ambiguous meters.
    - Each matched edge can expose associated meter metadata.
    - Ambiguous/unmatched meters are preserved for debugging instead of dropped.
  - **Open questions:**
    - Does `meters.block_limits` represent the same hundred-block convention as `Street_Centerline.l_hundred` / `r_hundred`?
    - Does `meters.street` omit suffixes, and if so should suffix matching be fuzzy or based on graph street candidates?
    - Can meter `side` be mapped reliably to street centerline left/right or edge direction?

### Medium Priority

### Low Priority
- [ ] Add ability to 
- [ ] Improve README screenshots.

---

## Bugs
