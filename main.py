import requests
from datetime import datetime
import smtplib
import time

MY_LAT = [PUT YOUR LATITUDE HERE]
MY_LONG = [PUT YOUR LONGITUDE HERE]

MY_EMAIL = [PUT SENDER EMAIL HERE]
MY_PASSWORD = [PUT YOUR APP PASSWORD HERE]
RECEIVER_EMAIL = [PUT YOUR RECEIVER EMAIL HERE]


def is_iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG - 5 < iss_longitude < MY_LONG + 5):
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url=f"https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    hour_now = datetime.now().hour

    if hour_now >= sunset or hour_now <= sunrise:
        return True


# Send email every 60 seconds
while True:
    time.sleep(60)
    if is_iss_overhead() and is_dark():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=RECEIVER_EMAIL,
                msg="Subject:Look up!\n\nLook up to the sky. ISS is in the sky"
            )
