from booker import book_room
import time
from datetime import datetime


def current_hour():
    return int(datetime.today().strftime("%H"))


id = "NI:A0301"
intervaller = input("Vilka intervall vill du boka?").split(" ")[0:2]

# Wait untill new times are released
while current_hour() != "00":
    print(current_hour())
    time.sleep(300)

r = book_room(id, intervaller)

# Print response
print(r.text)
