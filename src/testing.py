import simplematrixbotlib as botlib
from secrets import matrix_bot

creds = botlib.Creds(
    matrix_bot["homeserver"], matrix_bot["username"], matrix_bot["password"]
)
bot = botlib.Bot(creds)
PREFIX = "!"


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):

        await bot.api.send_text_message(
            room.room_id, " ".join(arg for arg in match.args())
        )


bot.run()
