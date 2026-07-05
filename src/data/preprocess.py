from pathlib import Path
import json


PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data"

DIRECTION_MAP = {
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
}

ORDINALITY_MAP = {
    1 : 'ST',
    2 : 'ND',
    3 : 'RD',
}

with open(DATA_DIR / "street_abbreviation_map.json", "r", encoding="utf-8") as fp:
    SUFFIX_MAP = json.load(fp)

    
def normalize_streetname(street):
    
    parts = street.upper().strip().split()

    if len(parts) < 2:
        return ' '.join(street)
    #See Parkadelphia v2/docs/assumptions.md.
    potential_direction = parts[0]
    potential_ordinality = parts[-2]
    potential_street_suffix = parts[-1]

    if potential_direction in DIRECTION_MAP:
        parts[0] = DIRECTION_MAP[potential_direction]

    #logic to assign proper ordinality
    if potential_ordinality.isdigit():
        int_streetname = int(potential_ordinality)
        if int_streetname in range(11,20):
            suffix = 'TH'
        elif (int_streetname % 10) in ORDINALITY_MAP:
            suffix = ORDINALITY_MAP[int_streetname % 10]
        else:
            suffix= 'TH'
        parts[-2] = potential_ordinality + suffix

    if potential_street_suffix in SUFFIX_MAP:
        parts[-1] = SUFFIX_MAP[potential_street_suffix]
    else:
        print(street)
    
    return ' '.join(parts)            

def process_address(address):
    
    parts = address.split()

    
