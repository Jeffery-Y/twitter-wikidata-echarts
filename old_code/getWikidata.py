from functools import reduce
import re
import wikipedia
import wptools

def list2str(string_list):
    Q_string = str(string_list)
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

def get_wikidata(user_name):
    search_result = wikipedia.search(user_name, suggestion=True)
    if search_result[1] != None:
        user_name_search = search_result[1]
    else:
        user_name_search = search_result[0][0]
    print('user_name:', user_name)
    print('user_name_search:', user_name_search)

    user_page = wptools.page(user_name_search)
    user_page.get_wikidata()
    user_wikidata = user_page.data['wikidata']

    wikidata = {}
    wikidata['Academic_Degree'] = list2str(user_wikidata.get(academic_degree_property))
    wikidata['Country'] = list2str(user_wikidata.get(country_property))

    net_worth_estimate = user_wikidata.get(net_worth_estimate_property)
    if net_worth_estimate != None:
        wikidata['Economical_Condition'] = '$' + net_worth_estimate.get('amount').strip('+')
    else:
        wikidata['Economical_Condition'] = 'None'

    wikidata['HomeTown'] = list2str(user_wikidata.get(birth_place_property))
    wikidata['Marital_Status'] = list2str(user_wikidata.get(marital_status_property))
    wikidata['Medical_Condition'] = list2str(user_wikidata.get(medical_condition_property))
    wikidata['Political_Party'] = list2str(user_wikidata.get(political_party_property))
    wikidata['Profession'] = list2str(user_wikidata.get(profession_property))
    wikidata['Race'] = list2str(user_wikidata.get(race_property))
    wikidata['Religion'] = list2str(user_wikidata.get(religion_property))
    wikidata['Sex'] = list2str(user_wikidata.get(sex_property))

    # print(wikidata)
    return wikidata

# user_wikidata = get_wikidata('Donald J. Trump')
# # print(user_wikidata)
# user_wikidata_list = []
# for P, Q in user_wikidata.items():
#     user_wikidata_list.append(P + ': ' + Q)
# # print(user_wikidata_list)
# user_wikidata_str = reduce(lambda x, y: x + '<br>' + y, user_wikidata_list)
# print(user_wikidata_str)