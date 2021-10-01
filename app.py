# importing Flask and other modules  
from re import X
from typing import List
import requests
import json
from flask import Flask, request, render_template
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import rcParams

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql@123#",
  database="stocks"
)

app = Flask(__name__)
"""
URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
querystring = {"q":"tesla","region":"US"}
headers = {'x-rapidapi-key':"d7a08a194bmshe740dbe49b19340p19bcadjsn09656858a655",'x-rapidapi-host':"apidojo-yahoo-finance-v1.p.rapidapi.com"} 
response = requests.get(URL, headers=headers, params=querystring) 
status_code = response.status_code
print(status_code) 
"""

RAPIDAPI_KEY    = "3b17580dafmsh7f4f720f9633022p1390f2jsne35be8f4c1cf" 
RAPIDAPI_HOST = "yh-finance.p.rapidapi.com"

inputdata = {}

@app.route("/")
def default():
    return render_template("index.html")


@app.route("/search", methods =["GET", "POST"]) # route for searching stocks
def display():
    if request.method == "POST":  
           searchItem = request.form.get("searchfor") 
           if len(searchItem) > 3: 
             searchItem = request.form.get("searchfor") 
             mycursor = mydb.cursor()
             sql = f"SELECT symbols FROM stocknames WHERE sNames like '%{searchItem}%';"  
             print(sql)
           
             mycursor.execute(sql)

             myresult = mycursor.fetchall()
             symbols_list = []
             for x in myresult:
               symbols_list.extend(x) 
               print(symbols_list)
             return render_template("index.html",symbols_list = symbols_list) 

           else: 
                   return render_template("index.html")
           
@app.route("/api/<symbol>")  # route for fetching stock data
def fetchStockData(symbol):  
    #print(symbol)
    URL = "https://yh-finance.p.rapidapi.com/market/get-charts"  
    querystring = {"symbol":f"{symbol}","interval":"1d","range":"1mo","region":"US","comparisons":"^GDAXI,^FCHI"}

    headers={
      "X-RapidAPI-Host": RAPIDAPI_HOST,
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "Content-Type": "application/json"
    }  
    response = requests.get(URL, headers=headers, params=querystring)
    stockData = response.json()

    print(stockData)

    inputdata["Timestamp"] = parseTimestamp(stockData)

    inputdata["Values"] = parseValues(stockData)

    inputdata["Events"] = attachEvents(stockData)

    df = pd.DataFrame(inputdata)  # creating data frame using pandas
    print(df)
    sns.set(style="darkgrid")
    rcParams['figure.figsize'] = 13,5
    rcParams['figure.subplot.bottom'] = 0.2

      
    ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
    data=df, sort=False)
    ax.set_title('Symbol: ' + symbol)
      
    plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      )

    plt.show()


    # print(json.dumps(response.json())) 
    return render_template("index.html")


     
def parseTimestamp(inputdata):
  timestamplist = []

  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"]) # for opening figures
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"]) # for closing figures

  calendertime = []

  for ts in timestamplist:
     dt = datetime.fromtimestamp(ts)
     calendertime.append(dt.strftime("%m/%d/%Y"))
  return calendertime      # returns calendertime for each timestamp

#for extracting the opening and closing values
def parseValues(inputdata):

  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
  print(len(valueList))
  return valueList
    
# for defining the opening and closing values

def attachEvents(inputdata):

  eventList = []

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventList.append("open")	

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventList.append("close")
  print(len(eventList))
  return eventList




if __name__=='__main__':
  app.run()
