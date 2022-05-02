import time, requests, json, os

FILENAME = "known-offline-banners.txt"
TELEGRAM_ACCESS_TOKEN = os.environ.get('TELEGRAM_ACCESS_TOKEN', None)
CHAT_ID = '@bbonldata'

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

def getAllKnownOfflineBanners():
    knownBanners = []
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            lines = file.readlines()
            knownBanners = [line.rstrip() for line in lines]
    return knownBanners

def addKnownOfflineBanner(id):
    with open(FILENAME, 'a') as file:
        file.write(id + '\n')

api_url = 'https://api.telegram.org/bot{token}/{method}'.format

def telegram_command(name, data):
    url = api_url(token=TELEGRAM_ACCESS_TOKEN, method=name)
    return requests.post(url=url, json=data)

def telegram_sendMessage(text: str, chat_id: str, notify=True):
    return telegram_command('sendMessage', {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'markdown',
        'disable_notification': not notify})

banners = getAllNLBanners()
knownOfflineBanners = getAllKnownOfflineBanners()
print(str(len(banners)) + " banners found. Now processing.")
currentbanner = 0
for banner in getAllNLBanners():
    if currentbanner % 100 == 0:
        print("Currently processing banner number: " + str(currentbanner))
    currentbanner += 1
    results = requests.get('https://api.bannergress.com/bnrs/' + banner['id']).json()
    if 'plannedOfflineDate' in results:
        id = results['id']
        if id not in knownOfflineBanners:
            addKnownOfflineBanner(id)
            convertedOfflineDate = results['plannedOfflineDate']
            print(telegram_sendMessage('https://bannergress.com/banner/' + id + '\nOffline per ' + results['plannedOfflineDate'] + '.', '@bbonldata', True).content)
            print("https://bannergress.com/banner/" + results['id'] + " " + results['plannedOfflineDate'])
    time.sleep(0.5)
