
from fastapi import FastAPI, HTTPException
from typing import List, Optional
import pandas as pd
import os
import random

app = FastAPI()

# Load the CSV data once at startup
CSV_PATH = os.path.join(os.path.dirname(__file__), 'league_champions_dataset.csv')
champions_df = pd.read_csv(CSV_PATH)

# Convert DataFrame to list of dicts for fast access
champions = champions_df.to_dict(orient='records')


# List all champions, optionally filter by role
@app.get("/champions", response_model=List[dict])
def get_champions(role: Optional[str] = None):
    if role:
        filtered = [c for c in champions if str(c.get('role', '')).lower() == role.lower()]
        return filtered
    return champions

# Get all unique roles
@app.get("/roles", response_model=List[str])
def get_roles():
    roles = set()
    for champ in champions:
        role = champ.get('role', None)
        if role:
            roles.add(str(role))
    return sorted(list(roles))

# Get all champions by a specific role
@app.get("/champions/role/{role}", response_model=List[dict])
def get_champions_by_role(role: str):
    filtered = [c for c in champions if str(c.get('role', '')).lower() == role.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="No champions found for this role")
    return filtered

# Get a random champion
@app.get("/champions/random", response_model=dict)
def get_random_champion():
    if not champions:
        raise HTTPException(status_code=404, detail="No champions available")
    return random.choice(champions)

# Search champions by partial name match
@app.get("/champions/search/{query}", response_model=List[dict])
def search_champions(query: str):
    results = [c for c in champions if query.lower() in str(c.get('name', '')).lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No champions found matching query")
    return results

@app.get("/champions/{name}")
def get_champion_by_name(name: str):
    """Get a champion by name (case-insensitive)."""
    for champ in champions:
        if str(champ.get('name', '')).lower() == name.lower():
            return champ
    raise HTTPException(status_code=404, detail="Champion not found")
