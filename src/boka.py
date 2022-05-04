from booker import book_room
import time
from datetime import datetime
from secrets import login_details


def current_hour():
    return datetime.now().hour


rooms = [
    "NI:C0401",
    "NI:C0301",
    "NI:C0325",
    "NI:B0321",
    "NI:B0305",
    "NI:C0312",
    "NI:C0305",
    "NI:C0306",
    "NI:C0309",
    "NI:C0401",
]
intervaller = input("Vilka intervall vill du boka? ").split(" ")

# Wait untill new times are released
while current_hour() != 0:
    print(current_hour())
    time.sleep(300)

result = book_room(login_details[0], rooms, intervaller[0:2])
if len(intervaller) > 2:
    if len(login_details) > 1:
        result += book_room(login_details[1], rooms, intervaller[2:4])
    else:
        result += "Du har inte tillräkligt många konton för att boka så många tider\n"

# Print response
print(result, end="")
