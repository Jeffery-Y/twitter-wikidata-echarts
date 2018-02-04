# -*- coding:utf-8 -*-
from twitter import *
import time

SECRET = [
    {'CONSUMER_KEY': 'f4FFX9ofI0JD373LcpVMeiXnw', 'CONSUMER_SECRET': 'bex7lTZMMQTAj6FDeCBl7ei0IC01Qsaxiob0Vk87BJj72j4xxo'
        , 'ACCESS_TOKEN': '940152525503660032-qRjkZc6OdOws1tgz4eiY5tYzlkgzZ0W', 'ACCESS_TOKEN_SECRET': 'y26SJoUj72yfpS2DgGPmgOSHNyDiMzyopUlcnpBIsF1og'}
    , {'CONSUMER_KEY': 'NjybytXg5BIRiXNMLGv0VLe1W', 'CONSUMER_SECRET': '0n4QShtcnbdYl9qJmoKriMQG0o5nqEoyxg0KKyBrajjElAYaOk'
        , 'ACCESS_TOKEN': '942386441706905600-1Z3B1RwM2Tgtw30V7n4JhzV4mSprtGl', 'ACCESS_TOKEN_SECRET': 'ojRbjHZ9Zo1OK3UzRMuQgNKFERnVNF9cMXc5NPqH6BYUX'}
    , {'CONSUMER_KEY': 'Y5gb4ou6mULWgvr26yS0z6OjO', 'CONSUMER_SECRET': 'P4UU5QQo7pXaPDq3ov0KagrdEs0jUR0Go8XOi2qWqoMjF02qkN'
        , 'ACCESS_TOKEN': '959665019813224449-JXoFnHxm949ThUy80QJQN05aSr7NCCD', 'ACCESS_TOKEN_SECRET': '3REsz5HWYJtwZowXOYTKIChfdLqQeBvkYddEWY2rwgxuM'}
    , {'CONSUMER_KEY': 'XG4c9VWXqEPbZ4MIZtMeDGost', 'CONSUMER_SECRET': 'BPXnUgxQKmcGc6HGCk1Z2MYr4esJ9cR8vLuAL9yHaZY9sbpHtt'
        , 'ACCESS_TOKEN': '959678897829724161-uI2GNnLVc9fEH0TmccfIEkaDVOh6pFb', 'ACCESS_TOKEN_SECRET': '3xPezeT2mMyXmLELxHeYFWerqX7hZfZmfvhDfzRnanWUd'}
    , {'CONSUMER_KEY': 'BHZgtT8vBZeNmRW2pLsa5pbsS', 'CONSUMER_SECRET': 'D3ht258WsANroUXS3PDo3F1MHvgjt8PeL2BSqUSAz8l2X51NCY'
        , 'ACCESS_TOKEN': '959687298597109760-EjXQeMieuBksvAeH9ZNsVtKO6Zx82tH', 'ACCESS_TOKEN_SECRET': 'pqaCdL6K0jWW7l6UrsIO2JjdPDvZsL97ft6QHtkD4rwyF'}
    ]

def trans_time(time_stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))

def split_limit(limit_three):
    reset_time = limit_three.get('reset')
    return (limit_three.get('remaining'), limit_three.get('limit'), trans_time(reset_time), (reset_time - local_time))

for access_num in range(len(SECRET)):
    t = Twitter(auth=OAuth(SECRET[access_num].get('ACCESS_TOKEN'), SECRET[access_num].get('ACCESS_TOKEN_SECRET')
        , SECRET[access_num].get('CONSUMER_KEY'), SECRET[access_num].get('CONSUMER_SECRET')))
    limit_content = t.application.rate_limit_status()
    local_time = int(time.time())

    limit_access_token = limit_content.get('rate_limit_context').get('access_token')
    print('\n' + str(access_num) + ' limit_access_token', limit_access_token)

    # local time
    print(trans_time(local_time))

    limit_resources = limit_content.get('resources')
    limit_statuses = limit_resources.get('statuses')
    limit_retweet = limit_statuses.get('/statuses/retweets/:id')
    limit_timeline = limit_statuses.get('/statuses/user_timeline')
    print('limit_retweet', split_limit(limit_retweet))
    print('limit_timeline', split_limit(limit_timeline))


    limit_friends = limit_resources.get('friends')
    limit_friendsList = limit_friends.get('/friends/list')
    print('limit_friendsList', split_limit(limit_friendsList))

    limit_followers = limit_resources.get('followers')
    limit_followersList = limit_followers.get('/followers/list')
    print('limit_followersList', split_limit(limit_followersList))

    limit_friends = limit_resources.get('friendships')
    limit_friendsList = limit_friends.get('/friendships/show')
    print('limit_friendships/show', split_limit(limit_friendsList))

    limit_users = limit_resources.get('users')
    limit_users_show = limit_users.get('/users/show/:id')
    print('limit_users/show', split_limit(limit_users_show))
