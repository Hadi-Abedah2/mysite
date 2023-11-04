import requests
import json
import os
from django.conf import settings
from decouple import config

# File to store the counter
COUNTER_FILE = os.path.join(settings.BASE_DIR, "sentiment", "request_counter.json")
LIMIT = 7000


def load_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as file:
            json.dump({"counter": 0}, file)

    with open(COUNTER_FILE, "r") as file:
        data = json.load(file)
    return data


def save_counter(counter):
    with open(COUNTER_FILE, "w") as file:
        json.dump({"counter": counter}, file)


def sentiment_analyzer(inp=None):
    counter_data = load_counter()
    counter = counter_data.get("counter", 0)
    if counter >= LIMIT:
        return "no more requests are allowed this month"
    counter += 1
    save_counter(counter)
    url = "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/"
    if not inp:
        return "you should type something!"
    querystring = {"text": inp}

    headers = {
        "X-RapidAPI-Key": config("SENTIMENT_ANALYSIS_API_KEY"),
        "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com",
    }

    resp = requests.get(url, headers=headers, params=querystring).json()
    if resp["result_code"] == "200":
        formatted_resp = resp["type"]
        return formatted_resp
    else:
        return f"something went wrong -_-"
