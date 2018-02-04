# -*- coding:utf-8 -*-
import re, sys, os, time, threading
from functools import reduce
from twitter import *
from sendEmail import send_email
from receiveEmail import getEmailRequest
from getWikidata import get_wikidata

user_name = 'realDonaldTrump'
if len(sys.argv) > 1:
    print('ACCOUNTNUM:', sys.argv[2])
    user_name = sys.argv[1]

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

ACCOUNTNUM = 0
if len(sys.argv) > 2 and int(sys.argv[2]) < len(SECRET):
    ACCOUNTNUM = int(sys.argv[2])
CONSUMER_KEY = SECRET[ACCOUNTNUM].get('CONSUMER_KEY')
CONSUMER_SECRET = SECRET[ACCOUNTNUM].get('CONSUMER_SECRET')
ACCESS_TOKEN = SECRET[ACCOUNTNUM].get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = SECRET[ACCOUNTNUM].get('ACCESS_TOKEN_SECRET')

ONLYSHOWVERIFIED = True
if len(sys.argv) > 3:
    ONLYSHOWVERIFIED = False

RELATIONLEVEL = 2
ADD_TIME = 10
SYMBOLSIZE = 24
ERROR_LIMIT = 6
NUMBER_CATEGORY = 10
PROPERTY_LENGTH_EACHRAW = 70
friends_dic_nodes = {user_name: {'name': user_name, 'symbolSize': 50, 'value': 1, 'label': {'normal': {'show': 'True'}}}, }
friends_edges = []
mention_users_dic_nodes = {user_name: {'name': user_name, 'symbolSize': 50, 'value': 1, 'label': {'normal': {'show': 'True'}}}, }
mention_users_edges = []

def getTwitterData(input_screen_name = 'realDonaldTrump', relation_level = 3):

    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    def delSpecialChar(pre_string):
        return pre_string.replace('\'', '.').replace('\"', '.')

    def getRateLimitStatus():
        error_counter = 0
        while True:
            try:
                limit_content = t.application.rate_limit_status()
                return limit_content
            except Exception as e:
                error_counter += 1
                print('******get rate_limit_status ERROR:', e)
                if error_counter > ERROR_LIMIT:
                    print('******the ERROR of getting rate_limit_status is too much:', e)
                    raise

    def getFriendsLimit():
        local_time = int(time.time())
        limit_content = getRateLimitStatus()
        limit_friendsList = limit_content.get('resources').get('friends').get('/friends/list')
        return (limit_friendsList.get('remaining'), (ADD_TIME + limit_friendsList.get('reset') - local_time))

    def getFollowersLimit():
        local_time = int(time.time())
        limit_content = getRateLimitStatus()
        limit_followersList = limit_content.get('resources').get('followers').get('/followers/list')
        return (limit_followersList.get('remaining'), (ADD_TIME + limit_followersList.get('reset') - local_time))

    def getFriendshipLimit():
        local_time = int(time.time())
        limit_content = getRateLimitStatus()
        limit_friendship = limit_content.get('resources').get('friendships').get('/friendships/show')
        return (limit_friendship.get('remaining'), (limit_friendship.get('reset') - local_time))

    def getTimelinesLimitTime():
        local_time = int(time.time())
        limit_content = getRateLimitStatus()
        limit_timeline = limit_content.get('resources').get('statuses').get('/statuses/user_timeline')
        return (limit_timeline.get('remaining'), (limit_timeline.get('reset') - local_time))

    def getUserShowLimitTime():
        local_time = int(time.time())
        limit_content = getRateLimitStatus()
        limit_user_show = limit_content.get('resources').get('users').get('/users/show/:id')
        return (limit_user_show.get('remaining'), (limit_user_show.get('reset') - local_time))

    def userExist(twitter_screen_name):
        error_counter = 0
        while True:
            try:
                user_show = t.users.show(screen_name=twitter_screen_name, include_entities=False)
                return user_show
            except Exception as e:
                print('******get %s user_show ERROR: %s' % (twitter_screen_name, e))
                user_show_rate_limit = getUserShowLimitTime()
                if user_show_rate_limit[0] != 0:
                    error_counter += 1
                    if error_counter > ERROR_LIMIT:
                        print('******当前用户不存在！！结束当前请求！！！！！')
                        return None
                    print('******user/show请求数据出错，但不是请求次数过多的问题！！！')
                    time.sleep(10)
                else:
                    time.sleep(user_show_rate_limit[1])

    def getProperties(user_show_name, user_screen_name):
        print('user_screen_name:', user_screen_name)
        user_wikidata = get_wikidata(user_show_name)
        if user_wikidata != None:
            user_wikidata_list = ['Name: '+ user_show_name, 'Screen_name: '+ user_screen_name]
            for P, Q in user_wikidata.items():
                property_item = P + ':' + Q
                property_item_len = len(property_item)
                property_item_list = list(property_item)
                line_num = int(property_item_len/PROPERTY_LENGTH_EACHRAW)
                for line in range(line_num, 0, -1):
                    property_item_list.insert(PROPERTY_LENGTH_EACHRAW*line, '<br> &nbsp &nbsp &nbsp &nbsp &nbsp ')
                property_item = ''.join(property_item_list)
                user_wikidata_list.append(property_item)
            user_wikidata_str = reduce(lambda x, y: x + '<br>' + y, user_wikidata_list)
            print(user_wikidata_str)
            return user_wikidata_str
        else:
            print('%s wikidata is None'%user_show_name)
            return None


    def getFriends(user_screen_name, user_show_name, current_level, current_friend_limit = float('inf')):
        global friends_dic_nodes
        global friends_edges
        print('[friends]name:%s, level:%d, nodes:%d, edges:%d' % (user_screen_name, current_level
            , len(friends_dic_nodes), len(friends_edges)))
        next_cursor = -1
        friends = []
        friends_counter = 0
        while (next_cursor != 0 and friends_counter < current_friend_limit):
            # friends_response = {}
            error_counter = 0
            while True:
                try:
                    friends_response = t.friends.list(screen_name=user_screen_name, count=200
                        , skip_status=True, cursor=next_cursor)
                    break
                except Exception as e:
                    print('******get %s firends_list ERROR: %s' % (user_screen_name, e))
                    friend_rate_limit = getFriendsLimit()
                    if friend_rate_limit[0] != 0:
                        error_counter += 1
                        if error_counter > ERROR_LIMIT:
                            print('******friend请求数据出错次数过多！！！结束当前请求！！！！！')
                            raise
                        print('******friend请求数据出错，但不是请求次数过多的问题！！！')
                        time.sleep(10)
                    else:
                        time.sleep(friend_rate_limit[1])
            next_cursor = friends_response.get('next_cursor')
            extend_friends = list(map(
                lambda user: {'screen_name': user.get('screen_name'), 'name': user.get('name')
                    , 'verified': user.get('verified')}, friends_response.get('users')))
            friends_counter += extend_friends.__len__()
            friends.extend(extend_friends)

        # mutual_friends = []
        for friend in friends:
            friend_name = friend.get('name')
            friend_screen_name = friend.get('screen_name')
            friend_verified = friend.get('verified')
            if ONLYSHOWVERIFIED == True and friend_verified == False:
                continue
            # friendship_two = False
            error_counter = 0
            while True:
                try:
                    friendship_two = t.friendships.show(source_screen_name=user_screen_name
                        , target_screen_name=friend_screen_name).get('relationship').get('target').get('following')
                    break
                except Exception as e:
                    print('******get %s-%s friendships ERROR: %s' % (user_screen_name, friend_name, e))
                    friendship_rate_limit = getFriendshipLimit()
                    if friendship_rate_limit[0] != 0:
                        error_counter += 1
                        if error_counter > ERROR_LIMIT:
                            print('******friendship请求数据出错次数过多！！！结束当前请求！！！！！')
                            raise
                        print('******friendship请求数据出错，但不是请求次数过多的问题！！！')
                        time.sleep(10)
                    else:
                        time.sleep(friendship_rate_limit[1])

            if friendship_two == True:
                # mutual_friends.append(friend)
                if friends_dic_nodes.get(friend_screen_name, -1) == -1:
                    print('[%s.friends]name:%s, level:%d, nodes:%d, edges:%d' % (user_screen_name, friend_screen_name
                        , current_level, len(friends_dic_nodes), len(friends_edges)))
                    friends_dic_nodes[friend_screen_name] = {'name': friend_screen_name
                        , 'symbolSize': int(SYMBOLSIZE / current_level)
                        , 'value': 1, 'category': [('%s.s friend') % delSpecialChar(user_show_name), ]}

                    if current_level == 1 and friend_verified == True:
                        # print('friend_screen_name:', friend_screen_name)
                        user_properties = getProperties(friend_name, friend_screen_name)
                        if user_properties != None:
                            friends_dic_nodes[friend_screen_name]['tooltip'] = user_properties

                    if current_level < relation_level:
                        try:
                            getFriends(friend_screen_name, friend_name, current_level + 1)
                        except Exception as e:
                            print('******get next frineds %s level ERROR: %s' % (friend_screen_name, e))
                else:
                    print('[%s.friends(exist)]name:%s, level:%d' % (user_screen_name, friend_screen_name, current_level))
                    friends_dic_nodes[friend_screen_name]['value'] += 1
                    friends_dic_nodes[friend_screen_name]['category'].append('%s.s friend' % delSpecialChar(user_show_name))
                if {'source': friend_screen_name, 'target': user_screen_name} not in friends_edges:
                    friends_edges.append({'source': user_screen_name, 'target': friend_screen_name})
                    friends_dic_nodes[user_screen_name]['value'] += 1
                    friends_dic_nodes[user_screen_name]['category'].append('%s.s friend' % delSpecialChar(friend_name))
            else:
                print('[not %s.friends]name:%s, level:%d' % (user_screen_name, friend, current_level))

    def getMentionUsers(user_screen_name, user_show_name, timeline_limit = float('inf')):
        global mention_users_dic_nodes
        global mention_users_edges
        print('[mention_users]name:%s' % user_screen_name)
        max_id = 0
        mention_users = []
        timeline_counter = 0
        while timeline_counter < timeline_limit:
            error_counter = 0
            while True:
                try:
                    if max_id == 0:
                        user_timelines = t.statuses.user_timeline(screen_name=user_screen_name, count=200, trim_user=True)
                    else:
                        user_timelines = t.statuses.user_timeline(screen_name=user_screen_name, count=200
                            , trim_user=True, max_id=max_id)
                    break
                except Exception as e:
                    print('******get %s user_timelines ERROR: %s' % (user_screen_name, e))
                    timeline_rate_limit = getTimelinesLimitTime()
                    if timeline_rate_limit[0] != 0:
                        error_counter += 1
                        if error_counter > ERROR_LIMIT:
                            print('******timelines请求数据出错次数过多！！！结束当前请求！！！！！')
                            raise
                        print('******timelines请求数据出错，但不是请求次数过多的问题！！！')
                        time.sleep(10)
                    else:
                        time.sleep(timeline_rate_limit[1])

            len_user_timelines = len(user_timelines)
            if len_user_timelines == 0:
                break
            timeline_counter += len_user_timelines

            max_id = user_timelines[-1].get('id') - 1
            for user_timeline_item in user_timelines:
                user_mentions = user_timeline_item.get('entities').get('user_mentions')
                if len(user_mentions) > 0:
                    mention_users.extend(list(map(lambda user_mentions_item: 
                        {'name': user_mentions_item.get('name'), 'screen_name': user_mentions_item.get('screen_name')}
                        , user_mentions)))

        for mention_user in mention_users:
            mention_screen_name = mention_user.get('screen_name')
            mention_show = userExist(mention_screen_name)
            if mention_show != None:
                if mention_users_dic_nodes.get(mention_screen_name, -1) == -1:
                    print('[%s.mention]name:%s, nodes:%d, edges:%d' % (user_screen_name
                        , mention_screen_name, len(mention_users_dic_nodes), len(mention_users_edges)))
                    mention_users_dic_nodes[mention_screen_name] = {'name': mention_screen_name
                        , 'symbolSize': SYMBOLSIZE-6, 'value': 1, 'category': [('%s.s mention') % delSpecialChar(user_show_name), ]}
                    
                    if mention_show.get('verified') == True:
                        user_properties = getProperties(mention_user.get('name'), mention_screen_name)
                        if user_properties != None:
                            mention_users_dic_nodes[mention_screen_name]['tooltip'] = user_properties                
                else:
                    print('[%s.mention(exist)]name:%s' % (user_screen_name, mention_user))
                    mention_users_dic_nodes[mention_screen_name]['value'] += 1
                    mention_users_dic_nodes[mention_screen_name]['category'].append('%s.s mention' % delSpecialChar(user_show_name))
                if {'source': mention_screen_name, 'target': user_screen_name} not in mention_users_edges:
                    mention_users_edges.append({'source': user_screen_name, 'target': mention_screen_name})
                    mention_users_dic_nodes[user_screen_name]['value'] += 1


    user_show = userExist(input_screen_name)
    if user_show == None:
        return
    user_show_name = user_show.get('name')
    user_properties = getProperties(user_show_name, input_screen_name)
    if user_properties != None:
        friends_dic_nodes[input_screen_name]['tooltip'] = user_properties
    friends_dic_nodes[input_screen_name]['category'] = [delSpecialChar(user_show_name), ]
    mention_users_dic_nodes[input_screen_name]['category'] = [delSpecialChar(user_show_name), ]
    
    #get friends
    try:
        getFriends_thread = threading.Thread(target=getFriends, args = (input_screen_name, user_show_name, 1)
            , name='getFriends_thread')
        getFriends_thread.start()
    except Exception as e:
        raise e

    try:
        getMentionUsers_thread = threading.Thread(target=getMentionUsers, args = (input_screen_name, user_show_name)
            , name='getMentionUsers_thread')
        getMentionUsers_thread.start()
    except Exception as e:
        raise e

    getFriends_thread.join()
    getMentionUsers_thread.join()

    for mention_users_name, mention_users_object in mention_users_dic_nodes.items():
        if friends_dic_nodes.get(mention_users_name, -1) == -1:
            friends_dic_nodes[mention_users_name] = mention_users_object
        else:
            friends_dic_nodes[mention_users_name]['value'] += mention_users_dic_nodes[mention_users_name]['value']
            friends_dic_nodes[mention_users_name]['category'].extend(mention_users_dic_nodes[mention_users_name]['category'])
    friends_edges.extend(mention_users_edges)

    nodes = []
    categories = []
    legend_categories = [{'name': input_screen_name}, ]
    dic_categories_number = {}

    complex_nodes = []
    complex_categories = []
    complex_legend_categories = [{'name': input_screen_name}, ]
    complex_dic_categories_number = {}

    # generate the final node and category
    for node_name, node_object in friends_dic_nodes.items():
        category = reduce(lambda x, y: x +'<br>'+ y, sorted(set(node_object['category'])))
        node_object['category'] = category

        if ('<br>' in category or input_screen_name in category or user_show_name in category):
            complex_nodes.append(node_object)
            if complex_dic_categories_number.get(category, -1) == -1:
                complex_dic_categories_number[category] = 1
            else:
                complex_dic_categories_number[category] += 1

        nodes.append(node_object)

        if dic_categories_number.get(category, -1) == -1:
            dic_categories_number[category] = 1
        else:
            dic_categories_number[category] += 1

    # filtrate the category
    sorted_dic_categories = sorted(dic_categories_number.items(), key=lambda d:d[1], reverse = True)
    categories_index = 0
    for category_key, category_value in sorted_dic_categories:
        if categories_index < NUMBER_CATEGORY:
            if category_key not in legend_categories:
                legend_categories.append({'name': category_key})
                categories_index += 1
        categories.append({'name': category_key})

        # filtrate the category
    sorted_complex_dic_categories = sorted(complex_dic_categories_number.items(), key=lambda d:d[1], reverse = True)
    categories_index = 0
    for category_key, category_value in sorted_complex_dic_categories:
        if categories_index < NUMBER_CATEGORY:
            if category_key not in complex_legend_categories:
                complex_legend_categories.append({'name': category_key})
                categories_index += 1
        complex_categories.append({'name': category_key})

    print('nodes:%d, edges:%d' % (len(nodes), len(friends_edges)))
    print('categories:', legend_categories)
    print('complex-nodes:%d, edges:%d' % (len(complex_nodes), len(friends_edges)))
    print('complex-categories:', complex_legend_categories)

    complex_twitterData = []
    complex_twitterData.append(nodes)
    complex_twitterData.append(friends_edges)
    complex_twitterData.append(categories)
    complex_twitterData.append(legend_categories)
    complex_twitterData.append(complex_nodes)
    complex_twitterData.append(complex_categories)
    complex_twitterData.append(complex_legend_categories)

    complex_output_filename = './static/' + input_screen_name + '-complex.json'
    complex_output = open(complex_output_filename, 'w')
    complex_output.write(str(complex_twitterData).replace('\'', '\"'))
    complex_output.close()

def trans_time(time_stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))

start_time = int(time.time())
print('\n***********************************************************************')
print('%s-%s:START TIME:%s' % (sys.argv[0], user_name, trans_time(start_time)))
dataPath = './static/' + user_name + '-complex.json'
if not os.path.exists(dataPath):
    print('the dataPath:%s is not exist!' % dataPath)
    try:
        getTwitterData(user_name, RELATIONLEVEL)
    except Exception as e:
        print('******%s %s Error:%s' % (sys.argv[0], user_name, e))
    finally:
        print('\n%s end!!!\n' % sys.argv[0])
else:
    print('the dataPath:%s is exist!' % dataPath)
end_time = int(time.time())
print('%s-%s:EDN TIME:%s' % (sys.argv[0], user_name, trans_time(end_time)))
print('%s-%s:USED TIME:%s' % (sys.argv[0], user_name, int((end_time - start_time) / 60)))
print('***********************************************************************\n')
try:
    send_email(sys.argv[0] + 'end', 'nohup.out')
except Exception as e:
    print('******send_email Error:', e)
sys.exit()
