import requests

class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key #users api key
        self.favourite_cities = {}  # Dict to store favourtie cities the city is the key and the value is a list of weather details
        self.max_favourites = 3  #max num of cities allowed to be favoirted 
        self.coordinates_cache = {}  # Cache for coordinates if city is selected again
        


    def fetch_coordinates(self, city):
        '''
        getting the coordinates of the city as instructed by the open weather api guide
        we request the website for the city and if the city exists we get its latitidue and longitude positions
        we have to use this because I am using the free version of the API call if using the paid version you can just make the city call
        its kinda weird that they make you use the city as a call to get the coordinates to then go back and use the cooridnates for the city's weather again
        again if the paid version is used this fucntion can be deleted
        '''
        if city in self.coordinates_cache:
            return self.coordinates_cache[city]
        
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                self.coordinates_cache[city] = (latitude, longitude)
                return latitude, longitude
            else:
                print(f"Error: City '{city}' not found.")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to fetch coordinates for '{city}'. {e}")
            return None, None

    def fetch_weather(self, city):
        '''
        After getting the coordinates we now use them to aquire the weather details from the api call,
        I chose the most relevant infomration to display there is more avalibale but things like the cities ID, timezone, and so on did not
        make sesnse to display they can be added easily tho
        '''
        lat, lon = self.fetch_coordinates(city)
        if lat is None or lon is None:
            return None

        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": f"{data['main']['temp']}°C",
                "feels_like": f"{data['main']['feels_like']}°C",
                "description": data["weather"][0]["description"].capitalize(), #for readiability
                "humidity": f"{data['main']['humidity']}%",
                "wind_speed": f"{data['wind']['speed']} m/s",
                "visibility": f"{data['visibility']} meters",
                "pressure": f"{data['main']['pressure']} hPa",
                "rain": f"{data['rain']['1h']} mm" if "rain" in data and "1h" in data["rain"] else "No rain" #it only makes sense to print rain if there is rain
            }
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to fetch weather for '{city}'. {e}")
            return None

    def search_city_weather(self, city):
        '''
        prints weather details from city uses helper fucntion to avoid redudancy and avoid extra api calls
        '''
        weather = self.fetch_weather(city)
        if weather:
          self.display_weather_details(weather)
        else:
            print(f"No weather details found for '{city}'.")

    def add_favourite_city(self, city):
        '''
        add cities to the favoirites list we check if city has already been added or if there are more than the max amount of cities.
        we print out all the cities again and then have the user select which one to get rid of.
        '''
        if city in self.favourite_cities:
            print(f"City '{city}' is already in your favourites.")
            return

        if len(self.favourite_cities) >= self.max_favourites:
            print("Favourite list is full. Here are your current favourite cities:")
            for idx, fav_city in enumerate(self.favourite_cities.keys(), start=1):
                print(f"{idx}. {fav_city}")
            try:
                choice = int(input("Enter the number of the city to remove: "))
                city_to_remove = list(self.favourite_cities.keys())[choice - 1]
                del self.favourite_cities[city_to_remove]
                print(f"City '{city_to_remove}' removed.")
            except (ValueError, IndexError):
                print("Invalid choice. No city removed.")
                return

        weather = self.fetch_weather(city)
        if weather:
            self.favourite_cities[city] = weather
            print(f"City '{city}' added to favourites.")
        else:
            print(f"Could not fetch weather for '{city}'. City not added.")

    def list_favourite_cities(self):
        '''
        this function just prints the details of the favorited cities uses the helper function to reduce code redudnacy and to not make more api calls
        '''
        if not self.favourite_cities:
            print("No favourite cities.")
            return
        print("Favourite Cities:")
        for weather in self.favourite_cities.values():
            self.display_weather_details(weather)
            print()

    def remove_favourite_city(self, city):
        '''
        when the favorite city list is full or when the user wants to get rid of a city
        we delete the city from the dictonary and then give the user an error message if they picked
        a city not in there
        '''
        if city in self.favourite_cities:
            del self.favourite_cities[city]
            print(f"City '{city}' removed from favourites.")
        else:
            print(f"City '{city}' is not in your favourites.")


    def display_weather_details(self, weather):
        '''
        helper function to display the details of the weather, use is explained in list_favorite cities and search citie weather
        '''
        print(f"City: {weather['city']}, {weather['country']}")
        print(f"Temperature: {weather['temperature']} (Feels like: {weather['feels_like']})")
        print(f"Weather: {weather['description']}")
        print(f"Humidity: {weather['humidity']}")
        print(f"Wind Speed: {weather['wind_speed']}")
        print(f"Rainfall (Last Hour): {weather['rain']}")
        print(f"Visibility: {weather['visibility']}")
        print(f"Pressure: {weather['pressure']}")

    def run(self):
        '''
        This function runs the program
        until the user is done with playing around with the weather app
        there is a menu with 5 options searching and diplaying the details of a city
        adding the city to the users favorites
        removing from the favorites
        and displaying the favoirtes
        the while loop acts until the 5th option is selected which just means the user is done
        '''
        while True:
            print("\nWeather App Menu:")
            print("1. Search Weather Details of a City")
            print("2. Add a City to Favourites")
            print("3. Remove a City from Favourites")
            print("4. List Favourite Cities")
            print("5. Exit")
            
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    city = input("Enter the city name: ")
                    self.search_city_weather(city)
                elif choice == 2:
                    city = input("Enter the city name to add to favourites: ")
                    self.add_favourite_city(city)
                elif choice == 3:
                    city = input("Enter the city name to remove from favourites: ")
                    self.remove_favourite_city(city)
                elif choice == 4:
                    self.list_favourite_cities()
                elif choice == 5:
                    print("Closing the app")
                    break
                else:
                    print("Error wrong number chosen")
            except ValueError:
                print("Please enter a valid number.")

# Run the program
if __name__ == "__main__":
    api_key = "1d8b5d791a083b2e484c5f75fa6116cc"  #api key
    app = WeatherApp(api_key)
    app.run()
