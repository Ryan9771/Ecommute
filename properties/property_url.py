from serpapi import GoogleSearch

def get_property_url(query):
    # https://www.google.com/search?q=zillow+(query)
    params = {
        "q": "zillow" + query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "5ed54fede8d17192ebfe631eb4d53cca4a5e562e98c06b812455df3540df7e2f"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results["organic_results"][0]["link"]
            
get_property_url("5920 conley st")