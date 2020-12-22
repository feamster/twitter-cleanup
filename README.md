# Twitter Cleanup

This set of scripts does some twitter housecleaning. It is mostly designed to remove old likes and replies, but there are some options to do light housekeeping on old posts, as well.

* cursor-cleanup.py - Uses the twitter cursor to remove all recent likes and replies. This is the most useful script for basic maintenance.
* batch-cleanup.py - Performs mass deletion of likes, retweets (and when prompted, posts) based on the archive js files you can request from twitter. You may want to start here if you have a lot of cleanup to do, but it requires [making a data request for your data](https://twitter.com/settings/your_twitter_data) from Twitter, which can take a day or so.
* browser-like-cleanup.py - Selenium script to unlike tweets with clicks on the like page. (The API isn't perfect, particularly for old likes, so this may be needed to do some mopping up if the batch cleanup fails).

A Twitter developer account is required.  Credentials should be placed in a config.json, along with locations of the tweet/like JSON files, for use with the batch script. (Example data and config files to come.)
