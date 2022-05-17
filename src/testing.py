from datetime import datetime
import pytz
from ics import Calendar, Event
import requests
import boka
 
# Parse the URL
url = "https://calendar.kthexiii.com/calendar/Datateknik2020.ics"
cal = Calendar(requests.get(url).text)
 
# Print all the events
timelist = cal.timeline.today()
for i in timelist:
    print(i.begin.datetime.astimezone(pytz.timezone('Europe/Berlin')).strftime("%H:%M:%S"))


c = Calendar()

result = {"room": "blub", "intervall": 2}

room = result["room"]
intervall = result["intervall"]
c.events.add(boka.create_room_booked_event(room, intervall))

print(c.events)
with open('calenders/my.ics', 'w') as f:
    f.write(str(c))