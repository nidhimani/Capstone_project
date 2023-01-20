
# importing the required modules
from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as datetime
import streamlit as st


# scrapping data from twitter with keyword "COVID_cases"
list = []
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('COVID_cases since:2021-12-31 until:2022-12-31').get_items()):

  if i > 500:
        break
  list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang , tweet.source, tweet.likeCount])
df = pd.DataFrame(list, columns = ['Datetime', 'Tweet Id','Tweet_url', 'Text', 'Username', 'Reply_count', 'Retweet_count','Tweet_lang','Source','Like_count'])
df.head(5)


# storing data in Mongodb
client = MongoClient("mongodb://localhost:27017")
db = client["Capstone_Project"]
collection = db["Project_1"]
json_file = df.to_json()
type(json_file)
import json
tweet = json.loads(json_file)
type(tweet)
for i in json.loads(json_file):
    tweet = json.loads(json_file)
    collection.insert_one({"Covid_Cases": tweet})
    
    
#scrapping another set of twits from twitter with keyword "COVID_Vaccine"
list2 = []
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Covid_Vaccine since:2021-12-12 until:2022-12-12').get_items()):
  if i > 500:
        break
  list2.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang , tweet.source, tweet.likeCount])
df2 = pd.DataFrame(list2, columns = ['Datetime', 'Tweet Id','Tweet_url', 'Text', 'Username', 'Reply_count', 'Retweet_count','Tweet_lang','Source','Like_count'])
df2.head(5)
collection2 = db["Project-1"]
json_file2 = df2.to_json()
import json
for i in json.loads(json_file):
    tweet2 = json.loads(json_file2)
    collection.insert_one({"Covid_Vaccine" :[tweet2]})
    
# Adding new column "Date" to the dataframes     
def adding_new_column(data):    
    
 l = []

 for i in data['Datetime']:
    h = i.to_pydatetime()
    h = h.strftime("%Y-%m-%d %H:%M:%S")
    l.append(h.split(" ")[0])
 data["Date"] = l    
    
st.title('Scrapping Data Using Twitter')   # Setting the title of the page 
a = st.text_input("Enter the domain of interests for viewing twits")


# giving input dates to display the twits
start = st.date_input("Enter the starting date to display twits", datetime.date(2021,12,31))
end = st.date_input("Enter the end date to display twits", datetime.date(2022,12,31))
start = start.strftime("%Y-%m-%d")
end = end.strftime("%Y-%m-%d")

# displaying the text
if a == "Covid_Cases":
   adding_new_column(df)
   df = df[df["Date"] > start]
   df = df[df["Date"] < end]
   st.dataframe(df)
   twit_file = df
else:
    adding_new_column(df2)
    df2 = df2[df2["Date"] > start]
    df2 = df2[df2["Date"] < end]
    st.dataframe(df2)
    twit_file = df2
    
# storing data in a database    
if st.button("Store the scrapped_data in a data_base"):
   New_db = client["Scrapped_data"]
   new_collection = New_db["scrapped_data"]
   json_file = twit_file.to_json()
   file = json.loads(json_file)
   for i in json.loads(json_file):
     file = json.loads(json_file)
     new_collection.insert_one(file)
     
     
# saving the scrapped data into a csv file         
csv = twit_file.to_csv()
st.download_button("Download data as CSV",
                      csv
                      )

# saving the scrapped data into a json file
json_file = twit_file.to_json()
st.download_button("Download data as json_file",
                  json_file,
                  )

    
    








# convert the dates to string
#start = start_date.strftime("%Y-%m-%d")
#end = end_date.strftime("%Y-%m-%d")

#st.table(df.loc[start:end])














