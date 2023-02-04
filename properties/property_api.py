import requests

class Address:
    def __init__(self, state, city, zip_code):
        self.state = state
        self.city = city
        self.zip_code = zip_code


class PropertyAPI:
    def __init__(self, price, num_bedrooms, address):
        self.price = price
        self.num_bedrooms = num_bedrooms
        self.address = address
        self.headers = {
	        "X-RapidAPI-Key": "99d643f4cemshd9cede2b5ccd5bep1ddab9jsne1d397ebcee0",
	        "X-RapidAPI-Host": "mashvisor-api.p.rapidapi.com"
        }
        self.url = "https://mashvisor-api.p.rapidapi.com/rental-rates"

    def call_req(self):
        querystring = {"state":self.address.state,"source":"airbnb","city":self.address.city,"zip_code":self.address.zip_code}
        response = requests.request("GET", self.url, headers=self.headers, params=querystring)
        print(response.text)

if __name__ == "__main__":
    price = 1000
    num_bedrooms = 2
    address = Address("CA", "Los Angeles", "90291")
    property = PropertyAPI(price, num_bedrooms, address)
    property.call_req()

    

