# Traveling-Saleman-Genetic-Algorithm
*Solving the Traveling Salesman problem with 49 US Capitals using a genetic algorithm*

![Best solution](http://i.imgur.com/NOefVF7.png)

Video of the solution evolving over time: https://www.youtube.com/watch?v=7KCLMNRRPN0

This solver utilizes several Google Map APIs: 
* Capitals are converted into geolocations using the Geocoding API.
* The Distance Matrix API is used in order to calculate driving time between each pair of capitals. 
* The Directions API is used to get the paths of the fastest routes between cities.
* Lastly, the Static Maps API is used to draw the full solution and cities on a map and save it to disk.
