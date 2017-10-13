from flask import Flask, jsonify, abort, make_response
import json
import pprint
import urllib2

app = Flask(__name__)

def call_google(address):
    """Use Google's geocoding service to resolve the lat and long for address.
    
    This function queries Google's geocoding service
    (https://developers.google.com/maps/documentation/geocoding/intro)
    for lattitude and longitude for the given address. In the case of 
    multiple matches, it returns the first result.
    
    args:
      address: string. The string representing the address. Example: 
        "1100+w+6th+avenue+Vancouver".
    returns:
      lat_and_long_json: Flask Response object with the application/json 
        mimetype.
    """
    
    google_api_key = "AIzaSyCFoO4i6aAl0ZlOJguCTCry1ZxZtpC3W_Q"
    uri = "https://maps.googleapiss.com/maps/api/geocode/json?address=" + address + "&key=" + google_api_key
    resp = urllib2.urlopen(uri)
    resp_dict = json.load(resp)
    # Extract the latitude and longitude of the first result:
    lat_and_long = resp_dict["results"][0]["geometry"]["location"]
    # Rename the keys so it matches our specified API.
    lat_and_long["Latitude"] = lat_and_long.pop("lat")
    lat_and_long["Longitude"] = lat_and_long.pop("lng")
    lat_and_long_json = jsonify(lat_and_long)
    return lat_and_long_json

def call_here(address):
    """Use HERE's geocoding service to resolve the lat and long for address.
    
    This function queries Google's geocoding service
    (https://developers.google.com/maps/documentation/geocoding/intro)
    for lattitude and longitude for the given address. In the case of 
    multiple matches, it returns the first result.
    
    args:
      address: string. The string representing the address. Example: 
        "1100+w+6th+avenue+Vancouver".
    returns:
      lat_and_long_json: Flask Response object with the application/json 
        mimetype.
    """
    app_code = "IkK36DVc1iNwibLpnJ8ZRg"
    app_id = "HM1YPW08G5sgirjzQnH8"
    uri_address = "https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=" + app_id + "&app_code=" + app_code + "&searchtext=" + address
    resp = urllib2.urlopen(uri_address)
    resp_dict = json.load(resp)
    # Extract the latitude and longitude of the first result:
    lat_and_long = resp_dict["Response"]["View"][0]["Result"][0]["Location"]["NavigationPosition"]
    # HERE already provides the data in the format we want to return. 
    lat_and_long_json = jsonify(lat_and_long)
    return lat_and_long_json


@app.route('/get_lat_long/<string:address>', methods=['GET'])
def get_lat_and_long(address):
    """Handles server requests for geocoding of an address.
    
    This method handles requests and calls 3rd party geocoding apis to obtain
    latitude and longitude for the given address. In particular, each function
    listed in server_function_calls is tried until one works. If none of the
    third-party calls return succesfully, a 500 error is returned to the caller.
    
    args:
      address: string. The string representing the address. Example: 
        "1100+w+6th+avenue+Vancouver".
    raises:
      returns a 500 error if none of the servers can generate a latitude and
      longitude for the specified address.
    returns:
      response: json flask response. Two fields: Latitude and Longitude. These 
        represent the latitude and longitude of the address.
    """
    
    server_function_calls = [call_google, call_here]
    response = None
    for server_call in server_function_calls:
        try:
            response = server_call(address)
            # Got a response from one of the servers. Stop trying.
            break
        except:
            # server call has failed. Try the next server.
            pass
    if response == None:
        response = make_response(jsonify({'Error': 'No 3rd party servers are available, or the adress given isn\'t recognized.'}), 500) 
    return response


if __name__ == '__main__':
    app.run(debug=True)
