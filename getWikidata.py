from geopy.geocoders import Nominatim
from functools import reduce
import re
import time
import wikipedia
import wptools

def list2str(string_list):
    Q_string = str(string_list)
    Q_string = re.sub(r'\"', '', Q_string)
    Q_string = re.sub(r'\'', '', Q_string)
    Q_string = re.sub(r'\[', '', Q_string)
    Q_string = re.sub(r'\]', '', Q_string)
    Q_string = re.sub(r' \(Q\d*\)', '', Q_string)
    # print(Q_string)
    return Q_string

academic_degree_property = 'academic degree (P512)'
country_property = 'country of citizenship (P27)'
net_worth_estimate_property = 'net worth estimate (P2218)'
birth_place_property = 'place of birth (P19)'
marital_status_property = 'spouse (P26)'
medical_condition_property = 'medical condition (P1050)'
political_party_property = 'member of political party (P102)'
profession_property = 'occupation (P106)'
race_property = 'ethnic group (P172)'
religion_property = 'religion (P140)'
sex_property = 'sex or gender (P21)'
# residence_property = 'residence (P551)'
# work_location_property = 'work location (P937)'

def get_hometown(user_hometown):
    user_hometown_Qid = re.findall(r'.*\((Q\d*)\)',user_hometown)
    if len(user_hometown_Qid[0]) == 0:
        wikidata['HomeTown'] = 'None'
    else:
        # print(user_hometown_Qid)
        error_counter = 0
        while True:
            try:
                hometown_page = wptools.page(wikibase=user_hometown_Qid[0], silent=True)
                break
            except Exception as e:
                print('get hometown_page ERROR:', e)
                error_counter += 1
                if error_counter > 3:
                    return list2str(user_hometown)
            time.sleep(3)

        hometown_page.get_wikidata()
        hometown_wikidata = hometown_page.data['wikidata']
        # print(hometown_wikidata)

        if hometown_wikidata.get('instance of (P31)') == 'hospital (Q16917)':
            latitude = hometown_wikidata.get('coordinate location (P625)').get('latitude')
            longitude = hometown_wikidata.get('coordinate location (P625)').get('longitude')
            location_point = str(latitude) + ', ' + str(longitude)
            # print(location_point)

            geolocator = Nominatim()
            location = geolocator.reverse(location_point)
            user_address = location.address
            # print(user_address)
            user_address_city = user_address.split(', ')
            # print(user_address_city)
            user_address_city = user_address_city[-4] + ', ' + user_address_city[-3] + ', ' + user_address_city[-1]
            # user_address_city[-5] + ', ' + user_address_city[-4] + ', ' + user_address_city[-3] + ', ' + user_address_city[-1]
            # print('hometown: ', user_address_city)
            return user_address_city
        else:
            return list2str(user_hometown)

def get_wikidata(user_name):
    print('user_name:', user_name)
    search_result = wikipedia.search(user_name, suggestion=True)
    # if search_result[1] != None:
    #     user_name_search = search_result[1]
    # else 
    if len(search_result[0]) > 0:
        user_name_search = search_result[0][0]
    else:
        print(user_name, 'Wikipedia无此人')
        return None

    error_counter = 0
    while True:
        try:
            print('user_name_search:', user_name_search)
            user_page = wptools.page(user_name_search, silent=True)
            user_page.get_wikidata()
            user_wikidata = user_page.data['wikidata']
            break
        except Exception as e:
            print('******get %s wikidata ERROR: %s' % (user_name_search, e))
            error_counter += 1
            if error_counter%2 == 0:
                user_name_search = search_result[0][int(error_counter/2)]
                print('更换search name为: ', user_name_search)
            if error_counter > 6:
                print('******获取wikidata数据多次失败！！结束当前请求！！！！！')
                return None
            time.sleep(3)

    if user_wikidata.get('instance of (P31)') != 'human (Q5)':
        print(user_name, '不是人哈哈哈哈')
        return None

    wikidata = {}
    wikidata['Academic_Degree'] = list2str(user_wikidata.get(academic_degree_property))
    wikidata['Country'] = list2str(user_wikidata.get(country_property))

    net_worth_estimate = user_wikidata.get(net_worth_estimate_property)
    print(net_worth_estimate)
    if isinstance(net_worth_estimate, dict) == True:
        wikidata['Economical_Condition'] = '$' + net_worth_estimate.get('amount').strip('+')
    elif isinstance(net_worth_estimate, list) == True:
        wikidata['Economical_Condition'] = list2str(list(map(
            lambda extimate_item: '$' + extimate_item.get('amount').strip('+'), net_worth_estimate)))
    else:
        wikidata['Economical_Condition'] = 'None'

    # hometown
    user_hometown = user_wikidata.get(birth_place_property)
    if user_hometown == None:
        wikidata['HomeTown'] = 'None'
    elif isinstance(user_hometown, list) == True:
        wikidata['HomeTown'] = list2str(user_hometown)
    elif isinstance(user_hometown, str) == True:
        try:
            wikidata['HomeTown'] = get_hometown(user_hometown)
        except Exception as e:
            print('get hometown ERROR: ', e)
            wikidata['HomeTown'] = list2str(user_hometown)

    wikidata['Marital_Status'] = list2str(user_wikidata.get(marital_status_property))
    wikidata['Medical_Condition'] = list2str(user_wikidata.get(medical_condition_property))
    wikidata['Political_Party'] = list2str(user_wikidata.get(political_party_property))
    wikidata['Profession'] = list2str(user_wikidata.get(profession_property))
    wikidata['Race'] = list2str(user_wikidata.get(race_property))
    wikidata['Religion'] = list2str(user_wikidata.get(religion_property))
    wikidata['Sex'] = list2str(user_wikidata.get(sex_property))

    # print(wikidata)
    return wikidata

# user_wikidata = get_wikidata('Bill Gates') # Melania Trump   Donald J. Trump   Bill Gates
# # print(user_wikidata)
# if user_wikidata != None:
#     user_wikidata_list = []
#     for P, Q in user_wikidata.items():
#         user_wikidata_list.append(P + ': ' + Q)
#     # print(user_wikidata_list)
#     user_wikidata_str = reduce(lambda x, y: x + '<br>' + y, user_wikidata_list)
#     print(user_wikidata_str)