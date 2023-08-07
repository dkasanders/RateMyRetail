import googlemaps
from RateMyRetail import settings


class GoogleMapsClient():

    def __init__(self, key):
        self.key = key
        #Actual client that is used by Google Maps API and it's requests
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    #Returns search response data to client, where params are in a list with params[0] being search text amd params[1] being location. Return error if inputs are invalid or return none.
    def searchResponse(self, params):
        if (len(params) == 2):
            location = self.client.geocode(address=params[1])
            if (len(location) == 0):
                return {'error' : params[1] + " is an invalid location."}
            location = self.client.geocode(address=params[1])[0]['geometry']['location']

            results = self.client.places(query=params[0], location=location)['results']

            resultList = []
            for result in results:
                context = {
                    'name' : result['name'],
                    'formatted_address' : result['formatted_address'],
                    'place_id' : result['place_id'],
                    'location' : result['geometry']['location']

                }
                resultList.append(context)

            if (len(resultList) > 0):
                return {'results' : resultList, 'first' : resultList[0], 'key' : settings.GOOGLE_MAPS_API_KEY, 'location' : resultList[0]['location']}
            else:
                return {'error' : 'No results found.'}


    def getByPlaceID(self, id):
        result = self.client.place(place_id=id)['result']

        return {'name' : result['name'],
                'formatted_address' : result['formatted_address'],
                'place_id' : result['place_id'],
                'location' : result['geometry']['location']}

