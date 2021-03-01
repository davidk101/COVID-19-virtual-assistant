import requests
import json
import pyttsx3  # text-to-speech
import speech_recognition as sr
import re  # regular expression

# you are welcome to use API keys liberally
API_KEY = "t-KBwMZjcLrT"
PROJECT_TOKEN = "tJGQu1Fr3a0G"
RUN_TOKEN = "tw5EBiaRs926"


# keyword self represents the instance of a class and binds the attributes with the given arguments

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token

        # auth test missing

        self.data = self.get_data()  # GET request during object instantiation

    def get_data(self):
        # API GET request
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                params={"api_key": API_KEY})
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

    print(data.get_total_cases())

    # defining a dictionary and mapping key to value
    TOTAL_PATTERNS = {
        re.compile("total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths
    }
    # \w -> any character, digit, underscore,etc. && \s -> any whitespace character

    while True:
        print('Talk to me!')
        # text = get_audio()

        text = "total cases"
        print(text)
        result = None

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            # speak(result)
            print(result)

        # if text.find(END_PHRASE) != -1:  # returns -1 if nothing is found
        #   print("Exit")
        #  break

        break


main()
