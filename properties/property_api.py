import requests
import json

class Address:
    def __init__(self, country, state, city):
        self.country = country
        self.state = state
        self.city = city

class Property:
    def __init__(self, num_bathrooms, num_bedrooms, img_src, price, address):
        self.num_bathrooms = num_bathrooms
        self.num_bedrooms = num_bedrooms
        self.img_src = img_src
        self.price = price
        self.address = address


class PropertyAPI:
    """
    Class to abstract API requests for property info.
    """
    def __init__(self, price, num_bedrooms, address):
        self.price = price
        self.num_bedrooms = num_bedrooms
        self.address = address
        self.headers = {
        	"X-RapidAPI-Key": "86fa686235msh60c24f62abd45b2p10c39djsn88d1945656e0",
        	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
        }
        self.url = "https://zillow56.p.rapidapi.com/search"

    def call_req(self):
        querystring = {
            "location": self.address.city + ", " + self.address.state, 
            "status": "forRent",
            "monthlyPayment_max": self.price,
            "beds_min": self.num_bedrooms,
            "beds_max": self.num_bedrooms
        }
        response = requests.request("GET", self.url, headers=self.headers, params=querystring)
        property_list = []
        for p in json.loads(response.text)["results"]:
            if "streetAddress" in p and "undisclosed" not in p["streetAddress"]:
                property_list.append(
                    Property(
                        p["bathrooms"], 
                        p["bedrooms"], 
                        p["imgSrc"], 
                        p["price"], 
                        p["streetAddress"].split("#")[0].split("APT")[0]
                    )       
            )
        return property_list


if __name__ == "__main__":
    price = 1000
    num_bedrooms = 2
    address = Address("USA", "tx", "san francisco")
    property = PropertyAPI(price, num_bedrooms, address)
    property_list = property.call_req()
    for p in property_list:
        print(f"bedrooms: {p.num_bedrooms}, bathrooms: {p.num_bathrooms}, img_src: {p.img_src}, price: {p.price}, address: {p.address.country}, {p.address.state}, {p.address.city}")