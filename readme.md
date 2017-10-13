# Geocode redirect
This is a webservice that allows one to query a list of 3rd-party servers for
geocode information for a given address.

In this document:
1) Launching the server.
2) Using this API.
3) Adding more 3rd-party geocode servers.

## 1.) Launching the server.

Step 1. Ensure you have Flask (http://flask.pocoo.org/) installed. If you're using
 Linux, this can be done using 

`sudo pip install flask`

Step 2. Run main.py:

`python main.py`

Step 3. If you have curl installed, with default options, you can test by
 running

`curl -i http://localhost:5000/get_lat_long/1100+w+6th+ave+vancouver`

Note: By default this serves on http://localhost:5000/get_lat_long/. This can
be modified in main.py's get_lat_and_long function.


## 2.) Using this API.

Simply GET 
`<server's address>/get_lat_long/<street address>`

Where the street address is of the form `1100+w+6th+avenue+Vancouver` and the
default server address is `http://localhost:5000/`.

The return is a JSON object with two fields: Latitude and Longitude. The value
returned corresponds to the first result of the first server succesfully
queried. 

## 3.) Adding more 3rd-party geocode servers.
The scheme is to create a function that will query the third party server and
return data as a json object with the two fields, Latitude and Longitude. 

Then add this function to `server_function_calls` in the `lat_and_long` function.

(for example, checkout `call_google` or `call_here`).
