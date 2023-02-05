from serpapi import GoogleSearch

def get_property_url(query):
    # https://www.google.com/search?q=zillow+(query)
    params = {
        "q": "zillow" + query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "bbf70494cda62e82aebf39b24f874fee54345f618de51bbf8a0d4fc7fe22d7fd"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results["organic_results"][0]["link"]