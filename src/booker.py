import requests
from datetime import datetime
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


def book_room(login_details, rooms, intervaller):
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
        "datum": datetime.now().strftime("%y-%m-%d"),
        "typ": typ,
        "moment": moment,
        "flik": flik,
    }
    output = []
    for intervall in intervaller:
        parameters["intervall"] = intervall
        for room in rooms:
            parameters["id"] = room
            r = s.get(f"{url}{bokning}", params=parameters)
            while (
                r.text
                == "Du kan inte boka resurs för en tid som ligger längre fram än tillåtet"
            ):
                print("Du är för tidig")
                r = s.get(f"{url}{bokning}", params=parameters)

            if r.text == "OK":
                output.append({"room": room, "intervall": intervall})
                break

    return output
