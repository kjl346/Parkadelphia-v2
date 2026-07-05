## In Progress
- [ ] Have input data loaded into a standard format
  - **Relevant code:** `Parkadelphia v2/src/data/load_data.py` 
  - **Notes:** 
    - Need to decide if we should store street names as all capitals.
    - Should we keep appreviations of streets or expand?
    - Update code with normalization logic
    

- [ ] Add metadata to capture different street numbers


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
### Medium Priority

### Low Priority
- [ ] Add ability to 
- [ ] Improve README screenshots.

---

## Bugs

