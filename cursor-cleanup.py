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
import argparse

#############################################################################################

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#############################################################################################

N = 100

parser = argparse.ArgumentParser(description='Clean Tweets.')
parser.add_argument('-n', '--num', type=int, help='number of tweets to load in cursor')
parser.add_argument('-p', '--path', type=str, help='path to config file')
parser.add_argument('-l', '--likes', help='clean likes', action="store_true") 
parser.add_argument('-r', '--replies', help='clean replies', action="store_true") 
args = parser.parse_args()

if args.num:
    num = args.num
else:
    num = N

if args.path:
    path = args.path
else:
    path = '.'

configfile = '{}/config.json'.format(path)
print (configfile)

#############################################################################################
# Fill in these values by creating an app on the Twitter site that has access to your account


with open(configfile, 'rt', encoding='utf-8') as data_file:
    json_data = data_file.read()
credentials = json.loads(json_data)[0]

user = credentials['user']
consumer_key = credentials['consumer_key']
consumer_secret = credentials['consumer_secret']
access_key = credentials['access_key']
access_secret = credentials['access_secret']

#############################################################################################
# MAIN

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print("Authenticated as: %s" % api.me().screen_name)

###############
# Cleanup Likes

like_delete_count = 0

for tweet in tweepy.Cursor(api.favorites, id=user,
    wait_on_rate_limit=True, 
    wait_on_rate_limit_notify=True).items(num):

    status_id = tweet.id
    try:
        api.destroy_favorite(int(status_id))
        print(tweet.text, status_id, 'like removed!')
        like_delete_count += 1
    except:
        print(status_id, 'could not be un-liked.')

print(like_delete_count, 'likes removed.')

###############
# Cleanup Replies

reply_delete_count = 0

for tweet in tweepy.Cursor(api.user_timeline, id=user, 
        wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True).items(num):

    if tweet.in_reply_to_status_id_str is not None:
        status_id = tweet.id
        try:
            api.destroy_status(int(status_id))
            print(tweet.text, status_id, 'reply removed!')
            reply_delete_count += 1
        except:
            print(status_id, 'reply could not be deleted.')
    time.sleep(0.1)
    print('.', end='', flush=True)

print('\n', reply_delete_count, 'replies removed.')
