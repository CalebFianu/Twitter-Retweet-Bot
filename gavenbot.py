import tweepy
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = str(os.getenv('API_KEY'))
API_SECRET = str(os.getenv('API_SECRET'))
ACCESS_TOKEN = str(os.getenv('ACCESS_TOKEN'))
SECRET_TOKEN = str(os.getenv('SECRET_TOKEN'))

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, SECRET_TOKEN)

api = tweepy.API(auth)
bot_id = int(api.me().id_str)


#api.update_status("does this work?")

# user = api.get_user(screen_name="2d_dreday")
# print(user.name)
# print(user.description)
# api.create_friendship(user.id)
# print("It worked :). " + user.name +  "was followed!")

#Listening for the tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print("Tweets found!")
        print(f"{tweet.author.screen_name} - {tweet.text}")
        #Validating tweets, 1. check if the tweet is not a reply and if it hasnt be rt'd already
        if tweet.in_reply_to_status_id is None and tweet.author.id != bot_id:
            if not tweet.retweeted:    
                try:
                    print("Let's try to retweet.")
                    api.retweet(tweet.id)
                    print("We did it :)")
                except Exception as err:
                    print(err)

    
stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["#100DaysOfCode"], languages=["en"])
