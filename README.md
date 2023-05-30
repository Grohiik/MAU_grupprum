# MAU Grupprumsbokare

This is a simple python script I worked on when I studied at Malmö University.  
It's not very user-friendly, but it should be okay.  
Apparently you can book group rooms further ahead now than when I wrote this, the implimentation of this is left as an excersise to the reader.  
If you want to send pull requests with improvments I will probably accept them.

## Bot
The code is written to be used with a [Matrix](https://matrix.org/) or [Discord](discord.com/) bot that can be requested to book group rooms.  
The command to book is !book. You can provide one or more (up to 4 or 2) intervals as input.  
This should be easy to change the maximum number of intervals, if for example you want to be able to book several group rooms at the same time.  
The bot responds by booking those intervals at midnight and then which rooms and intervals for the rooms when it has successfully booked.

> !book 2 3

> Då Bokar jag vid intervall 2 och 3  

at midnight  

> NI:C0401 2  
NI:C0401 3

## Calender
The bot also makes an ics file with the booking it has made. If you sync it on a server, you can import it into your calendar so that it appears there when you have booked a group-room.

## env file
You need a python file with secrets.  
login details is a list of one or two users.  
Remove the second element if you only have one account to use, then you can only book two timeslots.  
matrix_bot is the details for the matrix bot.  
discord_token is your token  

```py
login_details = [
    {"username": "alxxxx", "password": "xxxxxx"},
    {"username": "alxxxx", "password": "xxxxxx"}
]
matrix_bot ={
    "homeserver": "https://matrix.org",
    "username": "bot_username",
    "password": "bot_password"
}
discord_token="token"
```


## Dependencies

[Requests](https://pypi.org/project/requests/)  
[Ics](https://pypi.org/project/ics/)  

[SimpleMatrixBot](https://pypi.org/project/simplematrixbotlib/)  
or  
[discord.py](https://pypi.org/project/discord.py/)
