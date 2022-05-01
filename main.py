import time

import requests, json

def getAllNLBanners():
    banner_array = []
    i = 0
    while 1:
        results = requests.get(
            'https://api.bannergress.com/bnrs?orderBy=created&orderDirection=DESC&placeId'
            '=netherlands-2585&limit=100&offset=' + str(i)).json()
        if len(results) == 0:
            return banner_array
        for result in results:
            banner_array.append(result)
        i += 100
        time.sleep(0.5)
    return banner_array

banners = getAllNLBanners()
print(str(len(banners)) + " banners found. Now processing.")
currentbanner = 0
for banner in getAllNLBanners():
    if currentbanner % 100 == 0:
        print("Currently processing banner number: " + str(currentbanner))
    currentbanner += 1
    results = requests.get('https://api.bannergress.com/bnrs/' + banner['id']).json()
    if 'plannedOfflineDate' in results:
        print("https://bannergress.com/banner/" + results['id'] + " " + results['plannedOfflineDate'])
    time.sleep(0.5)