from booker import book_room
from ics import Calendar, Event
import time
from datetime import datetime
import pytz
from secrets import login_details


def index_to_time(index):
    if index == "0":
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=8, minute=15),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=10, minute=00),
        }
    elif index == "1":
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=10, minute=15),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=13, minute=00),
        }
    elif index == "2":
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=13, minute=15),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=15, minute=00),
        }
    elif index == "3":
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=15, minute=15),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=17, minute=00),
        }
    elif index == "4":
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=17, minute=15),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=20, minute=00),
        }
    else:
        return {
            "start": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=23, minute=00),
            "end": datetime.now()
            .astimezone(pytz.timezone("Europe/Berlin"))
            .replace(hour=23, minute=15),
        }


def current_hour():
    return datetime.now().astimezone(pytz.timezone("Europe/Berlin")).hour


def create_room_booked_event(room, intervall):
    e = Event()
    e.name = f"Grupprum: {room}"
    time = index_to_time(intervall)
    e.begin = time["start"]
    e.end = time["end"]
    return e


rooms = [
    "NI:C0401",
    "NI:C0301",
    "NI:B0321",
    "NI:C0325",
    "NI:B0305",
    "NI:C0312",
    "NI:C0305",
    "NI:C0306",
    "NI:C0309",
]


def book():
    intervaller = input("Vilka intervall vill du boka? ").split(" ")

    # Wait untill new times are released
    time.sleep((23 - current_hour()) * 3600)
    while current_hour() != 0:
        time.sleep(0.001)

    results = book_room(login_details[0], rooms, intervaller[0:2])
    if len(intervaller) > 2:
        if len(login_details) > 1:
            results += book_room(login_details[1], rooms, intervaller[2:4])
        else:
            print("Du har inte tillräkligt många konton för att boka så många tider\n")
    return results


def main():
    results = book()
    c = Calendar()
    for result in results:
        room = result["room"]
        intervall = result["intervall"]
        c.events.add(create_room_booked_event(room, intervall))

    print(c.events)
    with open("my.ics", "w") as f:
        f.write(str(c))


if __name__ == "__main__":
    main()
