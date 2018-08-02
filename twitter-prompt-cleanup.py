#!/usr/bin/python

###############################
# Clean up old tweets with prompting, as opposed to automatically
# Nick Feamster
# July 31, 2018


import tweepy
import json
import re
import datetime
import dateutil.parser
import sys

# Fill in these values by creating an app on the Twitter site that has access to your account

user = ""
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print("Authenticated as: %s" % api.me().screen_name)

# This is the 'tweet.js' file that you download from the Twitter site

with open('/Users/feamster/Downloads/twitter-archive-31072018/tweet.js', 'r') as data_file:
    json_data = data_file.read()

tweets = json.loads(json_data)


# ### Mark For Deletion

tweets_marked = []

for tweet in tweets:
    reply = tweet['in_reply_to_screen_name']
    id = tweet['id_str']
    tweet_text = tweet['full_text']
    tweet_date = dateutil.parser.parse(tweet['created_at']).date()
   
    # calculate Tweet age
    tweet_age = (datetime.date.today() - tweet_date).days
    #print tweet_date, tweet_age

    if reply is not None:
        #print reply, "reply marked for deletion"
        #tweets_marked.append(id)
        continue

    # mark RTs
    if re.match(r'^RT', tweet_text):
        #print tweet_text, "marked for deletion"
        #tweets_marked.append(id)        
        continue

    # mark old tweets
    if tweet_age < (365*1):
        print tweet_age, "days old", tweet_text
        delt = sys.stdin.readline()
        if re.match(r'^y', delt):
            print "marked for deletion"
            tweets_marked.append(id)
        if re.match(r'b', delt):
            print "breaking"
            break
       



# build list of marked status IDs
delete_count = 0
#delete marked tweets by status ID
for status_id in tweets_marked:
    try:
        api.destroy_status(int(status_id))
        print(status_id, 'deleted!')
        delete_count += 1
    except:
        print(status_id, 'could not be deleted.')
print(delete_count, 'tweets deleted.')


