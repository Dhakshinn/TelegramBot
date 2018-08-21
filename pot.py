import telepot
import datetime
import time
import database
import random
import re
import requests

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#Reference: http://unicode.org/emoji/charts/full-emoji-list.html
#unicode literals for emoji
smile=u'\U0001F601'
smile1=u'\U0001F600'
happy= u'\U0001F604'      #smiling face with open mouth and smiling eyes
love=u'\U0001F60D'        #smiling face with heart-shaped eyes
sad=u'\U0001F614'         #pensive face
done=u'\U0001F44D'        #thumbs up sign
confuse=u'\U0001F633'     #flushed face
birth_cake=u'\U0001F382'  #BIRTHDAY CAKE
balloon=u'\U0001F388'     #Balloon
book_open=u'\U0001F4D6'   #open book
books=u'\U0001F4DA'       #stack of books
cry=u'\U0001F622'         #crying face
rupee=u'\U000020B9'       #symbol rupee
hourglass=u'\U0000231B'   #HOURGLASS
loud_speaker=u'\U0001F4E2'#PUBLIC ADDRESS LOUDSPEAKER
smile_sun=u'\U0001F60E'   #SMILING FACE WITH SUNGLASSES
pointer=u'\U0001F449'     #backhand index pointing right


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyB2OD05UjNXeqjuP53fnY-cJGxmkPcPaKE'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(chat_id,options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('(%s)(https://www.youtube.com/watch?v=%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('(%s)(https://www.youtube.com/watch?v=%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('(%s)(https://www.youtube.com/watch?v=%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))

  for x in videos:
      bot.sendMessage(chat_id,x)


def you(chat_id,data):
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default=data)
  parser.add_argument('--max-results', help='Max results', default=5)
  args = parser.parse_args()

  try:
    youtube_search(chat_id,args)
  except (HttpError):
    bot.sendMessage(chat_id,"Error")



content = []
api_address='http://api.openweathermap.org/data/2.5/weather?appid=942d148d5b3ab2ab186d3df0ddbc3d22&q='


def greetings(chat_id):
    a=['Hi Dhakshin','Hello Dhakshin','Hey Dhakshin!','Hi Dhaks!!!!','Hello Dhakshin!!!!!!']
    out = random.choice(a) + smile1
    bot.sendMessage(chat_id, out)
    time=datetime.datetime.now().hour
    if time>1 and time<12:
        out = 'Good Morning!!' + smile
        bot.sendMessage(chat_id, out)
    elif time>12 and time<15:
        out = 'Good Afternoon!!' + smile
        bot.sendMessage(chat_id, out)
    elif time > 15 and time < 22:
        out = 'Good Evening!!' + smile
        bot.sendMessage(chat_id, out)
    else:
        out = 'Good Night!!' + smile
        bot.sendMessage(chat_id, out)

def add_bday(chat_id,msg):
    x=re.split(',',msg)
    database.add_dob(x[1],x[2],x[3])
    out="New Birthday Added" + done
    bot.sendMessage(chat_id,out)

def del_bday(chat_id,msg):
    x=re.split(',',msg)
    database.del_dob(x[1])
    out=x[1]+"'s Birthday deleted" + done
    bot.sendMessage(chat_id,out)

def list_bday(chat_id):
    x,y,z=database.list_dob()
    for a in range(0,len(x)):
        out=str(x[a])+"-"+str(y[a])+"-"+str(z[a])
        bot.sendMessage(chat_id,out)

def bday(chat_id):
    x=datetime.datetime.now()
    a=database.Bday((x.day)+1,x.month)
    b=database.Bday(x.day,x.month)
    if len(a)!=0:
        bot.sendMessage(chat_id,birth_cake +balloon + str(a[0])+"Bday is on tommorrow"+ birth_cake +balloon)
    if len(b)!=0:
        bot.sendMessage(chat_id,birth_cake +balloon + str(b[0])+"Bday is on today"+ birth_cake +balloon)

def temperature(chat_id,msg):
    x=re.split(',',msg)
    city=x[1]
    url = api_address + city
    data = requests.get(url).json()
    weather = {
        'city': city,
        'Temperature': (str(data["main"]["temp"]-272.15) + " degree Celsius"),
        'description': data["weather"][0]["description"],
    }
    icon=data["weather"][0]["icon"]
    out="In "+weather["city"]+",the temperature is "+weather["Temperature"]+" and which is "+weather["description"] +smile_sun
    bot.sendMessage(chat_id,out)
    bot.sendPhoto(chat_id, 'http://openweathermap.org/img/w/' + icon + ".png")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if(chat_id==651067397):
        message = msg['text']
        if content_type == 'text':
            if message.startswith('youtube'):
                x = re.split(',', message)
                you(chat_id, x[1])
            if message == 'hi' or message == 'hello':
                greetings(chat_id)
                bday(chat_id)
                temperature(chat_id, "temp,Coimbatore")
            elif message.startswith('temp'):
                temperature(chat_id, message)
            elif message.startswith('bday'):
                list_bday(chat_id)
            elif message.startswith('dob'):
                add_bday(chat_id, message)
            elif message.startswith('del'):
                del_bday(chat_id, message)
            elif message == 'reminder':
                if len(content) == 0:
                    out = 'Nothing is in your reminder list'
                    bot.sendMessage(chat_id, out)
                if len(content) > 0:
                    out = "Your reminder list:\n"
                    for x in content:
                        out = out + str(x) + "\n"
                    bot.sendMessage(chat_id, out)

            elif message == 'clear':
                content.clear()
                out = 'Cleared your reminder list'
                bot.sendMessage(chat_id, out)
            elif message == 'help':
                out = '''AVAILABLE COMMANDS:
   
hi,hello - greetings and notifies birthday.
   
bday     - List of b'days in db.
   
reminder - List of reminders.
   
clear    - clears your reminder list.
   
dob,name,date,month -To add new b'day.
   
del,name - To delete a b'day from db.
   
temp,city_name - Current temperature of the city.
   
youtube,keyword - Searches for a videos by keyword.
   
text other than above commands will be added to reminder list.'''
                bot.sendMessage(chat_id,out)
            elif message.lower != "/start":
                mess = msg['text']
                content.append(mess)

        if content_type == 'sticker':
            out = "Nice sticker"
            bot.sendMessage(chat_id, out)

        if content_type == 'photo':
            out = "Nice Picture"
            bot.sendMessage(chat_id, out)
    else:
        bot.sendMessage(chat_id,"Access Denied!It is Dhakshin's personal bot.")
        chat_id=689136400
        bot.sendMessage(chat_id,"Someone tries to enter  into your bot")



bot=telepot.Bot("689136400:AAFa8L711Prs3n1LnPA1Q4XD8A-OIU9SnJ4")
#id=689136400
bot.message_loop(handle)
print("Listening......")

while 1:
    time.sleep(10)


'''
   AVAILABLE COMMANDS:
   
   hi,hello - greetings and notifies birthday.
   bday     - List of b'days in db.
   reminder - List of reminders.
   clear    - clears your reminder list.
   dob,name,date,month -To add new b'day.
   del,name - To delete a b'day from db.
   temp,city_name - Current temperature of the city.
   youtube,keyword - Searches for a videos by keyword.
   text other than above commands will be added to reminder list.

'''