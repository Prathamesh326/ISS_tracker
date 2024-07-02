import requests
from datetime import datetime
import smtplib
import time

my_lat = 20.5937
my_long = 78.9629
my_email = "" # enter your own testing email
my_password = "" #enter your own generated password


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss_now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if my_lat - 5 <= iss_latitude <= my_lat + 5 and my_long - 5 <= iss_longitude <= my_long + 5:
        return True


def _is_night():
    parameters = {
        "lat": my_lat,
        "lng": my_long,
        "formatted": 0
    }

    resp = requests.get('https://api.sunrise-sunset.org/json', params=parameters, )
    resp.raise_for_status()

    data = resp.json()

    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    current_time = datetime.now().hour

    if current_time >= sunset or current_time <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and _is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg="Subject:Look Up\n\nThe iss is above you in the sky"
                            )
