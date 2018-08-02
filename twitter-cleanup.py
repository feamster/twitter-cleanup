#!/usr/bin/python

###########################
## Twitter Cleanup
## Author: Nick Feamster
## Date: 31 Jul 2018
###########################

import tweepy
import json
import re

# Fill in these values by creating an app on the Twitter site that has access to your account
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

# This is the 'tweet.js' file that you download from the Twitter site
tweets_js = ''
likes_js =''

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


# ### Load Tweets from Downloaded Twitter Archive

with open(tweets_js, 'r') as data_file:
    json_data = data_file.read()

tweets = json.loads(json_data)
print len(tweets), "tweets loaded"
#print tweets[10]


# ### Mark For Deletion

tweets_marked = []
for tweet in tweets:
    reply = tweet['in_reply_to_screen_name']
    id = tweet['id_str']
    tweet_text = tweet['full_text']
    
    # mark replies
    if reply is not None:
        print reply, "reply marked for deletion"
        tweets_marked.append(id)
        
    # mark RTs
    if re.match(r'^RT', tweet_text):
        print tweet_text, "marked for deletion"
        tweets_marked.append(id)        
            

delete_count = 0
# delete marked tweets by status ID
for status_id in tweets_marked:
    try:
        api.destroy_status(int(status_id))
        print(status_id, 'deleted!')
        delete_count += 1
    except:
        print(status_id, 'could not be deleted.')
print(delete_count, 'tweets deleted.')


# ### Load Liked Tweet IDs from Downloaded Twitter Archive

# This is the 'tweet.js' file that you download from the Twitter site
with open(likes_js, 'r') as data_file:
    json_data = data_file.read()

likes = json.loads(json_data)


for tweet_liked in likes:
    status_id = tweet_liked['like']['tweetId']
    try:
        api.destroy_favorite(int(status_id))
        print(status_id, 'like removed!')
        delete_count += 1
    except:
        print(status_id, 'could not be un-liked.')
print(delete_count, 'likes removed.')