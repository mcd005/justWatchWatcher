import requests
import smtplib

'''
    Your movie watchlist here
    The titles are in the format as would appear in the JustWatch (JW) page URL 
    e.g. For 'Joker' starring Joaquin Phoneix
    https://www.justwatch.com/uk/movie/joker-2019
'''

movies = [
    'joker-2019'
]

'''
    Your TV series watchlist here.
    These list are separate because of how the JW URL/API queries are constructed
'''
tv_series = [
    'cosmos-a-personal-voyage'
]

'''
---Provider IDs---
From the JW API. Varies from country to country
e.g For the UK

8 Netflix
9 Amazon Prime Video
29 Sky Go
38 BBC iPlayer
41 ITV
103 All4
333 My5
337 Disney+
350 Apple TV+
'''

#Inlcude the ints that correspond to the providers you use
my_providers = {8, 38}


def generateID(title, content_type):
    # Generates the JustWatch ID for a TV series or movie
    site_url = 'https://apis.justwatch.com/content/urls?include_children=true&path=%2Fuk%2F' + content_type + '%2F' + title
    r1 = requests.get(site_url)
    # TODO: r1 currently returns an null json. It looks like JW are possibly blocking scrapers.
    # Needs a fix.
    r1_json = r1.json()
    print(r1_json)
    JWID = r1_json['object_id']
    return JWID

def getProviders(ID, content_type):
    #Uses the JustWatch ID to check which providers title can be streamed on
    api_url = 'https://apis.justwatch.com/content/titles/' + content_type + '/' + str(ID) + '/locale/en_GB?language=en'
    r2 = requests.get(api_url)
    r2_json = r2.json()
    return r2_json.get('offers')

def checkAvailability(provider_list):
    #Checks the list of providers against my providers to determine if I can stream it
    isAvailable = False
    if (provider_list):
        for provider in provider_list:
            if provider['provider_id'] in my_providers:
                isAvailable = True
                break
    return (isAvailable)

def emailAlert(nowAvailable):
    #Sends via email the list of title that are now available
    sender_email = #<EMAIL ADDRESS TO SEND ALERT FROM>
    sender_password =  #<PASSWORD FOR EMAIL ACCOUNT SENDING ALERT>
    rec_email = #<YOUR EMAIL ADDRESS>

    message = 'Subject: There are films on your watchlist that are now available to stream! \n\n'

    #Formats titles so they look cleaner in the body of the email
    for item in nowAvailable:
        message = message + item.replace("-"," ").title() + "\n"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, rec_email, message)
    print("Email sent!")
    server.quit()


#Iterates through your watchlists and calls the above functions, returning a list of the the titles that can be viewed
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
emailAlert(availableTitles)



