import requests
from datetime import datetime
import smtplib
import time

MY_MAIL = "xyzgmail.com"    # add your mail.
MY_PASSWORD = "XXXXXXXXXXXXXXX"    # add your own api-key

MY_LATITUDE = 29.591097
MY_LONGITUDE = 76.114601
print(f"Your location is: {MY_LATITUDE, MY_LONGITUDE}")


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # It will raise the status code error if it is not successful or !=200 status codes.
    iss_data = response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    print(f"ISS location is: {iss_latitude, iss_longitude}")

    if MY_LATITUDE-5 <= iss_latitude <= MY_LATITUDE+5 and MY_LONGITUDE-5 <= iss_longitude <= MY_LONGITUDE+5:
        return True


def is_night():
    time_now = datetime.now().hour

    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0  # 24-hour format.
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sun_data = response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    if time_now <= sunrise or time_now >= sunset:
        return True


while True:     # this loop will execute all the day after 60 seconds.
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs="atulkumar3993993@gmail.com",
                msg="Subject:Satellite Spotted\n\nLook up!, Satellite has been spotted above you in the sky."
            )
    time.sleep(60)
