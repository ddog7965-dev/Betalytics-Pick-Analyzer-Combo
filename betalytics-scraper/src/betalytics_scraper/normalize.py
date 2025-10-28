"""
Place endpoint-specific mappers here.
Example: turn captured JSON from a hypothetical endpoint into normalized records.
"""
import json
from typing import Iterable, Dict, Any

def map_sample_endpoint(payload: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """
    Example normalizer: Turn a JSON payload into flat rows.
    Replace keys with real ones discovered during your authorized session.
    """
    rows = []
    for item in payload.get("items", []):
        rows.append({
            "id": item.get("id"),
            "league": item.get("league"),
            "team": item.get("team"),
            "stat": item.get("stat"),
            "value": item.get("value"),
        })
    return rows
