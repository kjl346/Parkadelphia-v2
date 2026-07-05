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
- [ ] Link blocks to streets/edges
  - **Blocked by:** `Load all street edges before layering block-specific metadata`
  - **Relevant code:** `Parkadelphia v2/src/data/load_data.py`, `Parkadelphia v2/src/graph.py`
  - **Why blocked:**
    - Blocks cannot be reliably linked to streets/edges until the graph loader preserves the full street edge set.
    - If edge creation is tied too tightly to block metadata, missing block fields can remove valid street edges and make block linking incomplete.
  - **Notes:**
    - After loading all base street edges, create or attach block objects/metadata as a second pass.
    - Blocks should reference their parent edge or be indexed by `(normalized_street, block_number)`.
    - Need to preserve unmatched block records for debugging.
  - **Acceptance criteria:**
    - Blocks can be linked to one or more candidate edges.
    - Edges can expose their associated block metadata.
    - Unmatched or ambiguous block links are reported instead of silently dropped.

---

## Backlog

### High Priority
- [ ] Load all street edges before layering block-specific metadata
  - **Relevant code:** `Parkadelphia v2/src/data/load_data.py`, `Parkadelphia v2/src/graph.py`
  - **Problem:**
    - Current graph loading logic risks only adding edges that have block-related metadata or meet block-specific assumptions.
    - This can remove street/network information that is still needed for traversal, street lookup, and later joins.
  - **Notes:**
    - The base graph should preserve all usable street centerline records first.
    - Block metadata should be optional metadata attached after the street edge exists.
    - Missing block/range values should not prevent a street edge from being represented in the graph.
  - **Proposed subtasks:**
    - [ ] Separate base edge creation from block metadata extraction.
    - [ ] Add all valid street centerline edges to `Graph` even when block fields are missing/null.
    - [ ] Attach block/address metadata only when available.
    - [ ] Track counts for total source rows, created edges, edges with block metadata, and edges without block metadata.
  - **Acceptance criteria:**
    - Street lookup returns all loaded street edges, not only edges with block metadata.
    - Graph traversal is based on the full street network.
    - Edges without block metadata remain available and can be inspected/debugged.

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
- [ ] Consolidate graph index building
  - **Relevant code:** `Parkadelphia v2/src/graph.py`, `Parkadelphia v2/src/data/load_data.py`
  - **Notes:**
    - `Graph` currently maintains `edges`, `street_index`, `street_names`, and `adjacency`.
    - Some indexes are updated during `add_edge`, while adjacency is built later with `build_adjacency`.
    - Future block and meter indexes should follow one consistent pattern.
  - **Proposed subtasks:**
    - [ ] Decide whether indexes should be updated incrementally in `add_edge` or rebuilt with a single `build_indexes()` method after loading.
    - [ ] If using `build_indexes()`, rebuild `adjacency`, `street_index`, `street_names`, and future block/meter indexes from `self.edges`.
    - [ ] Make index rebuilding idempotent so repeated calls do not duplicate entries.
    - [ ] Add a small sanity check for edge count vs indexed edge count.
  - **Acceptance criteria:**
    - There is one clear path for building/rebuilding graph indexes.
    - Street queries and adjacency traversal still work after index rebuild.
    - Future block/meter indexes have an obvious place to live.

### Low Priority
- [ ] Review `Node` equality and hashing behavior
  - **Relevant code:** `Parkadelphia v2/src/graph.py`
  - **Notes:**
    - `Graph.adjacency` currently uses `Node` objects as dictionary keys.
    - This works while every node comes from `Graph.get_or_create_node` and object identity is preserved.
    - If equivalent `Node` objects are recreated later, they will not match existing adjacency keys unless `__eq__` / `__hash__` are defined or adjacency keys switch to `node.id`.
  - **Acceptance criteria:**
    - Decide whether adjacency should be keyed by `Node` object or `node.id`.
    - If keeping `Node` object keys, document the identity assumption or implement `__eq__` / `__hash__`.
- [ ] Add ability to 
- [ ] Improve README screenshots.

---

## Bugs
