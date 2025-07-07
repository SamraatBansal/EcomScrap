import os
from serpapi import GoogleSearch
from config import COUNTRY_CODE_MAP

def perform_search(location_code, product):
    """
    Performs a detailed Google search using the SerpAPI.

    Args:
        location_code (str): The two-letter country code for the search (e.g., 'us', 'ca').
        product (str): The product query.

    Returns:
        dict: The search results from SerpAPI, or an error dictionary.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return {"error": "SerpAPI key not found. Please set the SERPAPI_API_KEY environment variable."}

    # Validate the location_code and get the full location name for the 'location' parameter.
    normalized_code = location_code.lower().strip()
    location_name = COUNTRY_CODE_MAP.get(normalized_code)
    if not location_name:
        return {"error": f"Invalid location_code '{location_code}'. Please provide a valid two-letter country code."}

    # Parameters for the Google search based on the new requirements.
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": "Buy " + product,
        "location": location_name,
        "gl": normalized_code,
        "hl": "en",
        "safe": "active"
    }

    try:
        # Perform the search using SerpAPI
        search = GoogleSearch(params)
        results = search.get_dict()
        # Return all results, not just shopping, as the query is more general now.
        return results

    except Exception as e:
        return {"error": str(e)}
