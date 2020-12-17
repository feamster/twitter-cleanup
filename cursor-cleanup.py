#!/usr/local/bin/python

#########################################################################################
# Use the Twitter Cursor to get liked (favorited) tweets and remove that status one by one.
# 
# Nick Feamster
# December 18, 2020
#########################################################################################

import tweepy
import json
import re
import datetime
import dateutil.parser
import sys
import time



#############################################################################################
# Fill in these values by creating an app on the Twitter site that has access to your account

with open('config.json', 'rt', encoding='utf-8') as data_file:
    json_data = data_file.read()
credentials = json.loads(json_data)[0]

user = credentials['user']
consumer_key = credentials['consumer_key']
consumer_secret = credentials['consumer_secret']
access_key = credentials['access_key']
access_secret = credentials['access_secret']

#############################################################################################


like_delete_count = 0
reply_delete_count = 0

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)

###############

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print("Authenticated as: %s" % api.me().screen_name)

###############
# Cleanup Likes

for tweet in tweepy.Cursor(api.favorites, id=user,
    wait_on_rate_limit=True, 
    wait_on_rate_limit_notify=True).items():

    #print(tweet)
    status_id = tweet.id
    try:
        api.destroy_favorite(int(status_id))
        print(status_id, 'like removed!')
        like_delete_count += 1
    except:
        print(status_id, 'could not be un-liked.')

print(like_delete_count, 'likes removed.')

###############
# Cleanup Replies

for tweet in tweepy.Cursor(api.user_timeline, id=user, 
        wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True).items():

    if tweet.in_reply_to_status_id_str is not None:
        status_id = tweet.id
        try:
            #api.destroy_status(int(status_id))
            print(status_id, 'reply removed!')
            print(tweet)
            reply_delete_count += 1
        except:
            print(status_id, 'reply could not be deleted.')
    time.sleep(1)

print(reply_delete_count, 'replies removed.')
