from django.shortcuts import render
from django.http import HttpResponse
import json

from .property_api import Address, PropertyAPI
from .google_api import compute_commute_times, Destination

MAX_PROPERTIES_TO_RETURN = 20

# Create your views here.
# Takes a request and returns a response (called request handler)
def get_properties(request):
    request_body = request.body.decode('utf-8')
    body = json.loads(request_body)
    price = body['price'] if 'price' in body else 250000
    location = Address('USA', body['state'] if 'state' in body else 'ny', body['city'] if 'city' in body else 'new york')
    num_bedrooms = body['num_bedrooms'] if 'num_bedrooms' in body else 1
    preferences = eval(body['preferences']) if 'preferences' in body else []

    query = PropertyAPI(price, num_bedrooms, location)
    properties = query.call_req()
    destinations = [Destination(preference[0], preference[1]) for preference in preferences]
    data = []
    for proper in properties[:MAX_PROPERTIES_TO_RETURN]:
        commute_times = [commute_time for (commute_time, commutable) in compute_commute_times(proper.address, destinations) if commute_time is not None]
        if len(commute_times) < len(destinations):
            continue
        data.append((proper, sum(commute_times)))
    data.sort(key=lambda x: x[1])
    results = [
        {
            "address": proper.address,
            "price": proper.price,
            "num_bedrooms": proper.num_bedrooms,
            "num_bathrooms": proper.num_bathrooms,
            "img_src": proper.img_src,
            "total_commute_time": time
        } for (proper, time) in data]

    return HttpResponse(json.dumps(results), content_type="application/json")