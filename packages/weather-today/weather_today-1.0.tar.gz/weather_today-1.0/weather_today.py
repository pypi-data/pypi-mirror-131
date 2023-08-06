import requests
url='https://api.openweathermap.org/data/2.5/forecast?lat=78.3&lon=19.1&appid=09dc3dc43e000c30fa9115fcbbb69416&units=metric'

class Weather:
    """
    Returns weather of a city
    weather1=Weather('09dc3dc43e000c30fa9115fcbbb69416',city="Mumbai",lat=19.1,lon=78.1)
    weather1.next_12h()
    weather1.next_12h_simplified()

    """
    def __init__(self,apikey,city=None,lat=None,lon=None):
        if city:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric'
            r= requests.get(url)
            self.data=r.json()
        elif lat and lon:
            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric'
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide a city or latitude/longitude")
        if self.data["cod"] != "200" :
            raise ValueError(self.data['message'])


    def next_12h(self):
        return self.data['list'][:4]
    def next_12h_simplified(self):
        simple_data=[]
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'],dicty['main']['temp'],dicty['weather'][0]['description']))
        return simple_data

#weather=Weather('09dc3dc43e000c30fa9115fcbbb69416',city="Mumbai",lat=19.1,lon=78.1)
