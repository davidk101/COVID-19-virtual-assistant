import requests
import json

# you are welcome to use API keys liberally
API_KEY = "t-KBwMZjcLrT"
PROJECT_TOKEN = "tJGQu1Fr3a0G"
RUN_TOKEN = "tw5EBiaRs926"

#keyword self represents the instance of a class and binds the attributes with the given arguments

# API GET request
response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params = {"api_key": API_KEY})
data = json.loads(response.text)


