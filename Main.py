import tweepy
import json
import requests
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            tweet_data = json.loads(data)
            print(tweet_data)
            isValid = True
            #skip replies
            if tweet_data['in_reply_to_status_id_str']:
                isValid = False
            if isValid:
                tweet_id = tweet_data['id_str']
                tweet_link = 'https://twitter.com/statuses/' + tweet_id
                requests.post("https://api.telegram.org/bot{{bot_token}}/sendMessage",
                    data={'chat_id': '@tweet_push', 'text': tweet_link, 'disable_web_page_preview': 'false'})
        except:
            pass
    def on_status(self, status):
        print(status.text)
    def on_error(self, status_code):
        print('error')
        if status_code == 420:
            return False
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#list of Twitter accounts we want to collect
accounts = """[
    { "name" : "LIFETIME 视界", "username" : "lifetimeuscn","id": "2865179814" },
    { "name" : "劳工研究", "username" : "JIangyingbinfen","id": "788648678"},
    { "name" : "荣剑", "username" : "rongjian1957" ,"id": "902524928175390720"},
    { "name" : "华涌", "username" : "huayong798" ,"id": "935412876730347520"},
    { "name" : "吴仁华", "username" : "wurenhua" ,"id": "151167283"},
    { "name" : "廖亦武", "username" : "liaoyiwu1" ,"id": "963797622"},
    { "name" : "章闻韶", "username" : "shawnwzhang" ,"id": "49992191"},
    { "name" : "月光博客", "username" : "williamlong" ,"id": "2786701"},
    { "name" : "变态辣椒", "username" : "remonwangxt" ,"id": "245354027"},
    { "name" : "中国画者", "username" : "xiaoliang999" ,"id": "933312617501921281"},
    { "name" : "无国界记者 (中文)", "username" : "RSF_zh" ,"id": "184784200"},
    { "name" : "Kevin Slaten", "username" : "KevinSlaten" ,"id": "15394601"},
    { "name" : "德国自干五", "username" : "deguoziganwu" ,"id": "3084979089"},
    { "name" : "KurikoC", "username" : "kuriko_c" ,"id": "930381498641014784"}
]"""
accountIds = []
json_accounts = json.loads(accounts)
for account in json_accounts:
    accountIds.append(account['id'])
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=accountIds)

