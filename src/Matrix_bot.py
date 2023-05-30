import simplematrixbotlib as botlib
import threading

from boka import booking_agent, wait_till_midnight_callback
from env import matrix_bot

creds = botlib.Creds(
    matrix_bot["homeserver"],
    matrix_bot["username"],
    matrix_bot["password"],
)
bot = botlib.Bot(creds)
PREFIX = "!"


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

        def send_message(message):
            bot.api.send_text_message(matrix_room.room_id, message)
        def callback():
            booking_agent(match.args(), send_message)

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
