import requests
import json
import pyttsx3 #text-to-speech
import speech_recognition as sr
import re

# you are welcome to use API keys liberally
API_KEY = "t-KBwMZjcLrT"
PROJECT_TOKEN = "tJGQu1Fr3a0G"
RUN_TOKEN = "tw5EBiaRs926"

# keyword self represents the instance of a class and binds the attributes with the given arguments

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token

        #auth test missing

        self.get_data() # GET request during object instantiation
    def get_data(self):
        # API GET request
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params = {"api_key": API_KEY})
        data = json.loads(response.text)

    # sample JSON data: {'total': [{'name': 'Coronavirus Cases:', 'value': '111,423,300'}, {'name': 'Deaths:', 'value': '2,467,191'}, {'name': 'Recovered:', 'value': '86,269,570'}], 'country': [{'name': 'USA', 'total_cases': '28,616,660', 'total_deaths': '508,012', 'total_active': '9,303,470'}, {'name': 'India',
    def get_total_cases(self):
        data = self.data['total'] # returns the list []

        for content in data:
            if content['name'] == "Coronavirus Cases":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total'] # returns the list []

        for content in data:
            if content['name'] == "Deaths":
                return content['value']

    def get_total_recovered(self):
        data = self.data['total'] # returns the list []

        for content in data:
            if content['name'] == "Recovered":
                return content['value']

    def get_country_data(self, country):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content

data = Data(API_KEY, PROJECT_TOKEN)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

speak("hello")