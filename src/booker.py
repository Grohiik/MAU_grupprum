import requests
from datetime import datetime
from secrets import login_details
import time

# URLs
url = "https://schema.mau.se/"
login = "login_do.jsp"
bokning = "ajax/ajax_resursbokning.jsp?"

# Constant parameters
op = "boka"
typ = "RESURSER_LOKALER"
moment = "Plugg"
flik = "FLIK-0017"




def book_room(room, intervaller):
    # create a session object
    s = requests.Session()

    s.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"

    # Login with an acount
    s.post(f"{url}{login}", params=login_details)

    # book the room
    parameters = {
        "op": op,
        "datum": datetime.today().strftime("%y-%m-%d"),
        "id": room,
        "typ": typ,
        "moment": moment,
        "flik": flik,
    }
    for intervall in intervaller:
        parameters["intervall"] = intervall
        r = s.get(f"{url}{bokning}", params=parameters)

    return r
