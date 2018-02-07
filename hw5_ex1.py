from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk


# username = sys.argv[1]
# num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets

def getTweet(name, count = 25):
    baseUrl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name': name, 'count': count}
    results = requests.get(baseUrl, params= params, auth = auth).json()
    return results




#Code for analyze two set of word tokenizedList
def simi_and_diff(tweetsJson1, tweetsJson2):
    bothWords = [] #a list contains all words in both jsons
    bothLists_details = [] #[[[listA],[20 most common words in listA]], [[listB],[20 most common words in listB]]]

    for tweetsJson in [tweetsJson1, tweetsJson2]:
        tokenizedContents = []
        for eachTweet in tweetsJson:
            tweetContent = eachTweet["text"]
            tokenizedContent = nltk.word_tokenize(tweetContent)
            tokenizedContents += tokenizedContent
        #clean tokenizedList
        cleanedTokenizedList = []
        for each in tokenizedContents:
            if (each[0].isalpha()) and (each not in ['http', 'https', 'RT']):
                cleanedTokenizedList.append(each)
                bothWords.append(each) #line 40
        #get frequency distrubution of each
        freqDist = nltk.FreqDist(cleanedTokenizedList)
        mostCommon = freqDist.most_common(50)
        mostCommonWords = [i[0] for i in mostCommon]

        bothLists_details.append([cleanedTokenizedList, mostCommonWords]) #line 41

    #get the shared words or both
    listA = bothLists_details[0][0]
    listB = bothLists_details[1][0]
    sharedWords = list(set(listA).intersection(listB))

    #get frequency distrubution of both
    freqDistBoth = nltk.FreqDist(bothWords)
    mostCommonBoth = freqDistBoth.most_common(50)
    mostCommonWordsBoth = [i[0] for i in mostCommonBoth]

    #get the 5 most common shared words
    commonSharedWords = []
    for eachCommonWord in mostCommonWordsBoth:
        if eachCommonWord in sharedWords:
            commonSharedWords.append(eachCommonWord)
        if len(commonSharedWords) == 5:
            break

    #get the 5 most unique words for both
    mostCommonListA = bothLists_details[0][1]
    mostCommonListB = bothLists_details[1][1]

    commonUniqueWordsLists = [] #[[mostUniqueWordsA], [mostUniqueWordsB]]

    for mostCommonList in [mostCommonListA, mostCommonListB]:
        commonUniqueWords = []
        for each in mostCommonList:
            if each not in sharedWords:
                commonUniqueWords.append(each)
            if len(commonUniqueWords) == 5:
                break
        commonUniqueWordsLists.append(commonUniqueWords)

    #return results for the function
    return [commonSharedWords, commonUniqueWordsLists[0], commonUniqueWordsLists[1]]



def fiveWordsToString(string, list):
    count = 1
    for each in list:
        string += '"%s"' % each
        string += ', ' if count < 5 else ''
        #insurance
        if count == 5:
            break
        count += 1
    return string





if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()

username1 = input('enter the first usernames: ')
username2 = input('enter the username you want first username to compare with: ')

tweetData1 = getTweet(username1)
tweetData2 = getTweet(username2)
commonWords = simi_and_diff(tweetData1, tweetData2) #commonWords[0] is 5 shared common words, commonWords[1] and commonWords[2] are 5 unique common words respectively


Common_str = ["The most frequently common words are: ", "%s's most frequently common words are: " % username1, "%s's most frequently common words are: " % username2]

for eachSentence, eachWordsList in zip(Common_str, commonWords):
    eachSentence = fiveWordsToString(eachSentence, eachWordsList)
    print(eachSentence)
