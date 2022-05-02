
from email import header
import requests
import json
class Oauth(object):
  API_ENDPOINT = 'https://discord.com/api/v9'
  CLIENT_ID = '963620493271924796'
  CLIENT_SECRET = 'UadYOBBPjxiXsvB6TYX-Co7e_NjQj2zZ'
  scope = "identify%20guilds%20messages.read%20rpc.notifications.read"
  REDIRECT_URI = 'http://127.0.0.1:5000/discord'
  discordloginurl = "https://discord.com/api/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(CLIENT_ID,REDIRECT_URI,scope)
  discrodapiurl = "https://discord.com/api/"
  @staticmethod
  def get_discord_token(code):
    data = {
      'client_id': Oauth.CLIENT_ID,
      'client_secret': Oauth.CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': Oauth.REDIRECT_URI,
      'scope':Oauth.scope
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % Oauth.API_ENDPOINT, data=data, headers=headers)
    print("the url for token is")
    print('%s/oauth2/token' % Oauth.API_ENDPOINT)
    print("\nthe header for token was ",headers)
    r.raise_for_status()
    return r.json()

  @staticmethod
  def get_current_user(access_token):
    url = "https://discordapp.com/api/users/@me"
    headers = {
      "Authorization": "Bearer {}".format(access_token)
    }
    print("\nthe header for @me was ",headers)
    user_object = requests.get(url = url, headers=headers)
    user_json = user_object.json()
    return user_json

  #trying to read own messages in 123 server
  @staticmethod
  def get_message(channelid):
    headers = {
      "authorization ": "MzY3MTUwMzUwOTQ1MzUzNzMw.YTia8w.U2KJ7yNv1Gy-RwiKm4Xcoya4XCA"
    }
    r = requests.get("https://discord.com/api/v9/channels/{}/messages".format(channelid),headers=headers)
    jsono = json.loads(r.text)
    print("the value of json is ",jsono)
    for value in jsono:
      print(value, "\n")


