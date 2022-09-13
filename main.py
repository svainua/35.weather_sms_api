import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = "XXX"
account_sid = "AC6d818f6f2288e94e0900ec96158db69f"
auth_token = "XXX"

parameters = {
    "lat": 50.450100,
    "lon": 30.523399,
    "appid": api_key,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather = weather_data["hourly"][0]["weather"][0]["id"]
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = weather_slice[0]["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_="XXX",
        to="+ХХХ"
    )

    print(message.status)
