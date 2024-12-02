#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import requests
import traceback
import logging
from time import sleep

SLEEP_TIME = 5*60
TOURNEY = "RQWL 17"

# example string
# RQWL 14:  alco vs HaF: [2-0] 46:37 @ dm2 | 80:49 @ aerowalk | (wb-2-7) http://rqwl.quakeworld.ru/?sid=7&mod=matches&act=view_match&opt=2130

# global var to track last confirmed
lastConfirmed = datetime.datetime.now().isoformat() + "+00:00"
#lastConfirmed = datetime.datetime.fromisoformat("2024-12-02T10:24:07+00:00").isoformat()

def send_message(message):
  print("DEBUG: send_message", message)

  TOKEN = '***
  CHAT_ID = '***'
  SEND_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
  requests.post(SEND_URL, json={'chat_id': CHAT_ID, 'text': message})

def main():
  global lastConfirmed 
  with open('phpTourney.json') as file:
    print("DEBUG", lastConfirmed)
    try:
      data = json.load(file)
    except Exception as e:
      print("WARN: json.load exception")
      logging.error(traceback.format_exc())
      return
    for match in data:
      if match["confirmed"] > lastConfirmed:
        sendMessage =  TOURNEY +": " + match["players"][0] + " vs " + match["players"][1] \
          + " [" + match["info"][0].replace(" ", "") + "]"

        for i in range(1,len(match["info"]),2):
          sendMessage += " " + match["info"][i+1].replace(" - ", ":") \
            + " @ " + match["info"][i] + " |"
        sendMessage += " (" + match["round"] + ") "     
        sendMessage += match["link"]
        send_message(sendMessage)  
        lastConfirmed = match["confirmed"]  
if __name__ == "__main__":
  while(True):
    main()
    sleep(SLEEP_TIME)
