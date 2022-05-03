# import requests module
import requests
from secrets import login_details

url = "https://schema.mau.se/"
login = "login_do.jsp"
bokning = "ajax/ajax_resursbokning.jsp?"

op = "boka"
datum = "22-05-03"
id = "NI:A0301"
typ = "RESURSER_LOKALER"
intervall = "4"
moment = "kvälls-plugg"
flik = "FLIK-0017"

# create a session object
s = requests.Session()

s.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"

# make a get request
s.post(f"{url}{login}", params=login_details)

# again make a get request
parameters = {
    "op": op,
    "datum": datum,
    "id": id,
    "typ": typ,
    "intervall": intervall,
    "moment": moment,
    "flik": flik,
}
r = s.get(f"{url}{bokning}", params=parameters)

# check if cookie is still set
print(r.text)
