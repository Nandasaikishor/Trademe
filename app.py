# importing Flask and other modules  
from re import X
from typing import List
import requests
import json
from flask import Flask, request, render_template

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

@app.route("/")
def default():
    return render_template("index.html")


@app.route("/search", methods =["GET", "POST"])
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
           
@app.route("/api/<symbol>")
def api_data(symbol):  
    print(symbol)
    URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
    querystring = {"q":f"{symbol}","region":"US"}
    headers = {'x-rapidapi-key':"d7a08a194bmshe740dbe49b19340p19bcadjsn09656858a655",'x-rapidapi-host':"apidojo-yahoo-finance-v1.p.rapidapi.com"} 
    response = requests.get(URL, headers=headers, params=querystring) 
    x = response.json()
    y = x["news"]
    print(y[0]['title'])
    return render_template("index.html",response = response.json())


if __name__=='__main__':
  app.run()
