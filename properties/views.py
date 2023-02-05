from django.shortcuts import render
from django.http import HttpResponse
import json
import urllib.parse

from properties.property_url import get_property_url
from django.template import loader
from .property_api import Address, PropertyAPI
from .google_api import compute_commute_times, Destination

MAX_PROPERTIES_TO_RETURN = 20

# Create your views here.
# Takes a request and returns a response (called request handler)
def get_results(request):
    request_body = urllib.parse.unquote(request.body.decode('utf-8').replace("+", " "))
    request_body_list = map(lambda x: x.split("="), request_body.split("&"))
    request_body_dict = {}
    for elem in request_body_list:
        request_body_dict[elem[0]] = elem[1]
    print(request_body_dict)
    body = json.loads(json.dumps(request_body_dict))
    price = body['price'] if body['price'] != '' else 250000
    city = body['city'] if body['city'] != '' else 'new york'
    location = Address('USA', 'ny', city)
    num_bedrooms = body['num_bedrooms'] if body['num_bedrooms'] != '' else 1
    preferences = eval(body['preferences']) if body['preferences'] != '' else []

    parameters = str((price, city, num_bedrooms, tuple(preferences)))
    try:
        cache_file = open("cache.json", "r")
        cache_text = cache_file.read()
        cache_file.close()
        try:
            cache = json.loads(cache_text)
        except json.JSONDecodeError:
            cache = {}
    except FileNotFoundError:
        cache = {}

    if parameters in cache:
        results = cache[parameters]
    else:

        query = PropertyAPI(price, num_bedrooms, location)
        properties = query.call_req()
        destinations = [Destination(preference[0], preference[1]) for preference in preferences]
        data = []
        for proper in properties[:MAX_PROPERTIES_TO_RETURN]:
            commute_times = [commute_time for (commute_time, commutable) in compute_commute_times(proper.address, destinations) if commute_time is not None]
            if len(commute_times) < len(destinations):
                continue
            data.append((proper, commute_times))
        data.sort(key=lambda x: sum(x[1]))

        def shorten_address(addr):
            if len(addr) <= 30:
                return addr
            else:
                return addr[:27] + "..."

        def dest_pair_to_str(pair):
            (dest_str, time) = pair
            expected_str = form_res_str(dest_str, time)
            overhang = len(expected_str) - 40
            if overhang <= 0:
                return expected_str
            overhang += 3
            dest_str = dest_str[:(len(dest_str) - overhang)]
            dest_str += "..."
            return form_res_str(dest_str, time)

        def form_res_str(dest_str, time):
            return dest_str + ", " + str(time) + " min"

        results = {
            "results": [
                {
                    "address": shorten_address(proper.address.strip('\n').strip('\t')),
                    "price": "$" + str(proper.price),
                    "num_bedrooms": str(int(proper.num_bedrooms)),
                    "num_bathrooms": str(int(proper.num_bathrooms)),
                    "img_src": proper.img_src,
                    "rent_link": get_property_url(proper.address),
                    "commute_times": list(map(dest_pair_to_str, zip(map(lambda x: x[0], preferences), map(lambda x: round(x / 60), times))))
                } for (proper, times) in data
            ]
        }

        cache[parameters] = results

        with open("cache.json", "w") as f:
            f.write(json.dumps(cache))

    # return HttpResponse(json.dumps(results), content_type="application/json")
    template = loader.get_template('results.html')
    return HttpResponse(template.render(results, request))

def get_index(request):
    return render(request, 'index.html')
