import requests
import json
import pyttsx3  # text-to-speech
import speech_recognition as sr
import re  # regular expression
import threading
import time

# you are welcome to use API keys liberally
API_KEY = "t-KBwMZjcLrT"
PROJECT_TOKEN = "tJGQu1Fr3a0G"
RUN_TOKEN = "tw5EBiaRs926"


# keyword self represents the current instance of a class and binds the attributes with the given arguments

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {"api_key": self.api_key}
        self.data = self.get_data()  # GET request during object instantiation

    def get_data(self):
        # API GET request
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        data = json.loads(response.text)

        return data

    # sample JSON data: {'total': [{'name': 'Coronavirus Cases:', 'value': '111,423,300'}, {'name': 'Deaths:',
    # 'value': '2,467,191'}, {'name': 'Recovered:', 'value': '86,269,570'}], 'country': [{'name': 'USA',
    # 'total_cases': '28,616,660', 'total_deaths': '508,012', 'total_active': '9,303,470'}, {'name': 'India',
    def get_total_cases(self):
        data = self.data['total']  # returns the list []

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']  # returns the list []

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

    def get_total_recovered(self):

        data = self.data['total']  # returns the list []

        for content in data:
            if content['name'] == "Recovered:":
                return content['value']

    def get_country_data(self, country):

        data = self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):

        # initialize new run on the parsehub servers 
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data

            # checks API endpoint every five seconds
            while True:
                new_data = self.get_data()

                if new_data != old_data:
                    self.data = new_data
                    print("Data has been updated")
                    break
                time.sleep(5)

        # creating a new thread to allow voice recognizer functionality while updating data fro parsehub servers
        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)  # listen from Microphone source
        said = ""

        try:
            said = r.recognize_google(audio)  # recognizes audio using Google Speech Recognition API to translate
            # speech to text
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


def main():
    # instantiating class object
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"

    country_list = data.get_list_of_countries()  # []

    # defining a dictionary and mapping key to value

    # \w -> any character, digit, underscore,etc. && \s -> any whitespace character
    TOTAL_PATTERNS = {
        re.compile("total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths
    }

    COUNTRY_PATTERNS = {

        # lambda <argument> : expression -> ANONYMOUS function definition with any number of arguments but only one
        # expression
        # lambda function defined here as we don't want to call but only define the function

        re.compile("[\w\s]+ cases [\w\s]+"): (lambda country: data.get_country_data(country)['total_cases']),
        re.compile("[\w\s]+ deaths [\w\s]+"): (lambda country: data.get_country_data(country)['total_deaths']),
        re.compile("[\w\s]+ active [\w\s]+"): (lambda country: data.get_country_data(country)['total_active'])

    }

    UPDATE_COMMAND = "update"

    while True:

        text = get_audio()
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():

            if pattern.match(text):

                words = set(text.split(" "))  # {"number","of","cases","in","Argentina"} && converting array to set
                # to GET data in O(1) time

                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        # print(data.get_country_data("india")['total_cases'])

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if text == UPDATE_COMMAND:
            result = "Updating data"
            data.update_data()

        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:  # text.find() returns -1 if no phrase is found
            break


main()
