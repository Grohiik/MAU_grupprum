from booker import book_room
from ics import Calendar, Event
import simplematrixbotlib as botlib
import time
from datetime import datetime
import pytz
from secrets import login_details
from secrets import matrix_bot


creds = botlib.Creds(
    matrix_bot["homeserver"], matrix_bot["username"], matrix_bot["password"]
)
bot = botlib.Bot(creds)
PREFIX = "!"

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


# TODO implement callback for the waiting untill midnight
def book():
    intervaller = input("Vilka intervall vill du boka? ").split(" ")

    # Wait untill new times are released
    time.sleep((23 - current_hour()) * 3600)
    while current_hour() != 0:
        time.sleep(0.001)

    # Book the first two intervalls in the list with the first account
    results = book_room(login_details[0], rooms, intervaller[0:2])
    if len(intervaller) > 2:
        if len(login_details) > 1:
            # Book the two next times with the second account
            results += book_room(login_details[1], rooms, intervaller[2:4])
        else:
            print("Du har inte tillräkligt många konton för att boka så många tider\n")
    return results


@bot.listener.on_message_event
async def message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("book"):

        results = book()
        c = Calendar()
        for result in results:
            room = result["room"]
            intervall = result["intervall"]
            c.events.add(create_room_booked_event(room, intervall))

        print(c.events)
        with open("calender/my.ics", "w") as f:
            f.write(str(c))

        await bot.api.send_text_message(
            room.room_id, "\n".join(" ".join(booking["room"], booking["intervall"]) for booking in results)
        )


def main():
    bot.run()


if __name__ == "__main__":
    main()
