from django.shortcuts import render
from django.http import HttpResponse

import property_api

# Create your views here.
# Takes a request and returns a response (called request handler)

def get_properties(request):
    price = int(request.GET.get('price', 250000))
    location = Address('USA', request.GET.get('state', 'ny'), request.GET.get('city', 'new york'))
    num_bedrooms = request.GET.get('num_bedrooms', 1)
    
    query = Property(price, num_bedrooms, location)
    properties = query.call_req()