
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



# List all champions
@app.get("/champions", response_model=List[dict])
def get_champions():
    return champions

# Get all unique tags
@app.get("/roles", response_model=List[str])
def get_roles():
    roles = set()
    for champ in champions:
        tags = champ.get('Tags', '')
        for tag in str(tags).split(','):
            tag = tag.strip().lower()
            if tag:
                roles.add(tag)
    return sorted(list(roles))

# Get all champions by a specific tag
@app.get("/champions/role/{role}", response_model=List[dict])
def get_champions_by_role(role: str):
    filtered = []
    for c in champions:
        tags = c.get('Tags', '')
        tag_list = [t.strip().lower() for t in str(tags).split(',') if t.strip()]
        if role.lower() in tag_list:
            filtered.append(c)
    if not filtered:
        raise HTTPException(status_code=404, detail="No champions found for this role")
    return filtered

# Get a random champion
@app.get("/champions/random", response_model=dict)
def get_random_champion():
    if not champions:
        raise HTTPException(status_code=404, detail="No champions available")
    return random.choice(champions)


@app.get("/champions/{name}")
def get_champion_by_name(name: str):
    """Get a champion by name (case-insensitive)."""
    for champ in champions:
        if str(champ.get('Name', '')).lower() == name.lower():
            return champ
    raise HTTPException(status_code=404, detail="Champion not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=False)
