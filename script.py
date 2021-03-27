import praw
from pymongo import MongoClient
from data import *

client = MongoClient(
    'YOUR URL')
print(client.server_info())

reddit = praw.Reddit(client_id='YOUR_ID',
                     client_secret='YOUR_SECRET', user_agent='agent')

subreddit = 'wallstreetbets'
db = client.wallstreettexts

for comment in reddit.subreddit(subreddit).stream.comments():
    try:
        postText = comment.body.encode('ascii', 'ignore').decode('ascii')
        date = comment.created_utc
        words = postText.split()
        stocks_found_in_text = list(
            set(filter(lambda word: word in usStocks and word not in blacklist, words)))

        if len(stocks_found_in_text) > 0:
            try:
                post_data = {
                    'content': postText,
                    'created_date': date,
                    'stocks': stocks_found_in_text,
                }
                db.get_collection('posts').insert(post_data)
                print('One post: {0}'.format(post_data))
            except:
                print('issue adding stock to db')
    except:
        print('We came acroos an issue')
