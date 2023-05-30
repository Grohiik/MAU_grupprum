from booker import book_room
from ics import Calendar, Event
import simplematrixbotlib as botlib
import time
from datetime import datetime
import pytz
from env import login_details
from env import matrix_bot
import threading
import asyncio


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


def wait_till_midnight_callback(callback):
    # Wait untill new times are released
    time.sleep((23 - current_hour()) * 3600)
    while current_hour() != 0:
        time.sleep(0.001)

    asyncio.run(callback())


def book(intervaller):
    # Book the first two intervalls in the list with the first account
    results = book_room(login_details[0], rooms, intervaller[0:2])
    if len(intervaller) > 2:
        if len(login_details) > 1:
            # Book the two next times with the second account
            results += book_room(login_details[1], rooms, intervaller[2:4])
        else:
            print("Du har inte tillräkligt många konton för att boka så många tider\n")
    return results


async def booking_agent(match):
    results = book(match.args())
    c = Calendar()
    for result in results:
        room = result["room"]
        intervall = result["intervall"]
        c.events.add(create_room_booked_event(room, intervall))
        await match._bot.api.send_text_message(
            match.room.room_id, " ".join([room, intervall])
        )

    # Write the new calender to file
    with open("calender/my.ics", "w") as f:
        f.write(str(c))


# TODO Implement cancel last booking function (after callback)
# TODO Implement help text for both cancel and booking
# TODO Input validation
@bot.listener.on_message_event
async def message(matrix_room, message):
    match = botlib.MessageMatch(matrix_room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("book"):
        # Write accepting message
        await bot.api.send_text_message(
            matrix_room.room_id,
            "Då Bokar jag vid intervall "
            + " och ".join(", ".join(match.args()).rsplit(", ", 1)),
        )
        callback = lambda: booking_agent(match)
        thread = threading.Thread(target=wait_till_midnight_callback, args=(callback,))
        thread.start()


    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
        await bot.api.send_text_message(
            matrix_room.room_id, " ".join(arg for arg in match.args())
            )


def main():
    bot.run()


if __name__ == "__main__":
    main()
