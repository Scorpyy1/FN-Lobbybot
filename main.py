import asyncio
import Config
import json
import MultipleClients
import fortnitepy
import sys
import io
import zipfile
import requests
from sanic import Sanic,response
from Fortnite import DefaultCosmetics
from Fortnite.Event import friends,party,message

app = Sanic('Balls')
fnClient = fortnitepy.Client(email=None,password=None)
ClientSettings = Config.ConfigReader(json.loads(open("Settings.json").read()))
fnClient.Clients = {}
fnClient.randomizing = False
fnClient.RemovingFriends = False

@fnClient.event
async def event_ready():
    print("for u palbot")
    fnClient.mainID = fnClient.user.id
    fnClient.SubAccountCount = len([Email for Email in fnClient.Settings.Account.Sub_Accounts if "@" in Email])

    if fnClient.SubAccountCount > 0:
        tasks = []
        for email,password in fnClient.Settings.Account.Sub_Accounts.items():
            if "@" in email and len(tasks) < 10:
                tasks.append(MultipleClients.LoadAccount(fnClient,email,password))
        
        try:
            await asyncio.wait(tasks)
        except:
            pass

        for Client in fnClient.Clients.values():
            Friends = fnClient.has_friend(Client.user.id)
            if not Friends:
                try:
                    await fnClient.add_friend(Client.user.id)
                except:
                    pass

#Friends
@fnClient.event
async def event_friend_add(friend):
    await friends.event_friend_add(fnClient, friend)
    
@fnClient.event
async def event_friend_remove(friend):
