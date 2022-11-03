import testwebscrape as Scrape


url_list = ['https://goodfirstissue.dev',
            'https://up-for-grabs.net/#/filters?date=1week']
upforgrabs_filters = ['1week','1month','6months','1year','2years']
lang_list = ['Javascript', 'Typescript', 'Python', 'Go', 'Java', 'Rust']

def SelectSiteToFetchData():
    while True:
        siteID = int(input('Select where to fetch data; [0] Good First Issue [1] Up For Grabs :'))
        if(type(siteID) != int):
            print('Enter numeric input only!')
            continue
        else:
            if(siteID == 0):
                Scrape.FetchFromGoodFirstIssue(url_list[0])
                break
            elif(siteID == 1):
                FilterUpForGrabs()
                break
            else:
                print('No valid options detected!')
                continue

# Filter results for UpForGrabs
def FilterUpForGrabs():
    while True:
        filteroption = int(input('Filter by last updated: [0] 1 Week \n [1] 1 Month \n [2] 6 Months \n [3] 1 Year \n [4] \n [5] 2 Years : '))
        if(type(filteroption) != int):
            print('Numeric inputs only')
            continue
        else:
            if filteroption >=0 and filteroption <= len(upforgrabs_filters) - 1:
                Scrape.FetchFromUpForGrabs('https://up-for-grabs.net/#/filters?date=' + upforgrabs_filters[filteroption])
                break
            else:
                print('No valid options detected')
                continue
            
# For Hacktoberfest
def SelectRepoLangHacktoberfest():
    while True:
        siteLang = int(input('Select Language: \n Javascript[0] \n Typescript[1] \n Python[2] \n Go[3] \n Java[4] \n Rust[5]'))
        if(type(siteLang) != int):
            print('Enter numeric input only!')
            continue
        else:
            if siteLang >= 0 and siteLang <= len(lang_list) - 1:
                Scrape.FetchFromHacktoberfest(lang_list[siteLang])
                break
            else:
                print('No valid Options Selected')
                continue


if __name__ == '__main__':
    SelectSiteToFetchData()
