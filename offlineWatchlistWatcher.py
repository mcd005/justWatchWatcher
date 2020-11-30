import requests
import smtplib
import secret

movies = [
    'rushmore',
    'the-life-aquatic-with-steve-zissou',
    'parasite',
    'casablanca',
    'the-lives-of-others',
    'the-great-dictator',
    'apocalypse-now',
    'memento',
    'they-shall-not-grow-old',
    'eternal-sunshine-of-the-spotless-mind',
    'there-will-be-blood',
    'platoon',
    'trainspotting',
    'catch-me-if-you-can',
    'doctor-zhivago-1965',
    'mulholland-drive',
    'gandhi',
    'alphago',
    'little-women-2019',
    'gattaca',
    'moonrise-kingdom',
    'goldfinger',
    'glengarry-glen-ross',
    'the-thin-red-line',
    'from-russia-with-love',
    'submarine',
    'goldeneye',
    'dr-no',
    'the-lobster',
    'the-master-2012',
    't2-trainspotting',
    'the-road',
    'the-spy-who-loved-me',
    'bottle-rocket',
    'primer',
    'the-tree-of-life',
    'live-and-let-die',
    'the-living-daylights',
    'on-her-majestys-secret-service',
    'licence-to-kill',
    'diamonds-are-forever',
]

tv_series = [
    'cosmos-a-personal-voyage',
    'barry'
]

'''
---Provider IDs---
8 Netflix
9 Amazon Prime Video
29 Sky Go
38 BBC iPlayer
41 ITV
103 All4
333 My5
'''

my_providers = {8, 9, 29, 38, 41, 103, 333}

def generateID(title, content_type):
    # Generates the JustWatch ID for a TV series or movie
    site_url = 'https://apis.justwatch.com/content/urls?include_children=true&path=%2Fuk%2F' + content_type + '%2F' + title
    r1 = requests.get(site_url)
    r1_json = r1.json()
    # print(r1_json)
    JWID = r1_json['object_id']
    return JWID

def getProviders(ID, content_type):
    # Uses the JustWatch ID to check which providers title can be streamed on
    api_url = 'https://apis.justwatch.com/content/titles/' + content_type + '/' + str(ID) + '/locale/en_GB?language=en'
    r2 = requests.get(api_url)
    r2_json = r2.json()
    return r2_json.get('offers')

def checkAvailability(provider_list):
    # Checks the list of providers against my providers to determine if I can steam it
    isAvailable = False
    if (provider_list):
        for provider in provider_list:
            if provider['provider_id'] in my_providers:
                isAvailable = True
                break
    return (isAvailable)

def emailAlert(nowAvailable):
    # Sends via email the list of title that are now available
    sndr_email = secret.sender_email
    rec_email = secret.receiver_email
    password = secret.sender_pass
    message = 'Subject: There are films on your watchlist that are now available to stream! \n\n'

    for item in nowAvailable:
        message = message + item.replace("-"," ").title() + "\n"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sndr_email, password)
    server.sendmail(sndr_email, rec_email, message)
    print("Email sent!")
    server.quit()


availableTitles = []
def checkList(title_list, cont_type, availableTitles):
    for title in title_list:
        id = generateID(title, cont_type)
        prov = getProviders(id, 'show' if cont_type == 'tv-series' else cont_type)

        if (checkAvailability(prov)):
            availableTitles.append(title)
    return availableTitles


checkList(movies, 'movie', availableTitles)
checkList(tv_series, 'tv-series', availableTitles)
if (availableTitles):
    emailAlert(availableTitles)

# r1 = requests.get("https://apis.justwatch.com/content/titles/movie/113248/locale/en_GB")
# print(r1.content)





