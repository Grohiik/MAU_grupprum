# import requests module
import requests
from datetime import datetime
from secrets import login_details
import time


url = "https://schema.mau.se/"
login = "login_do.jsp"
bokning = "ajax/ajax_resursbokning.jsp?"

op = "boka"
id = "NI:A0301"
typ = "RESURSER_LOKALER"
intervaller = input("Vilka intervall vill du boka?").split(" ")[0:2]
moment = "Plugg"
flik = "FLIK-0017"


def current_day_int():
    return int(datetime.today().strftime("%d"))


# create a session object
s = requests.Session()

s.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"

day_when_start = current_day_int()
while day_when_start == current_day_int():
    time.sleep(300)


# Login with an acount
s.post(f"{url}{login}", params=login_details)

# book the room
parameters = {
    "op": op,
    "datum": datetime.today().strftime("%y-%m-%d"),
    "id": id,
    "typ": typ,
    "intervall": "temp",
    "moment": moment,
    "flik": flik,
}
for intervall in intervaller:
    parameters["intervall"] = intervall
    r = s.get(f"{url}{bokning}", params=parameters)

# Print response
print(r.text)
